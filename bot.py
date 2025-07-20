import discord
from discord.ext import commands
import asyncio
import yt_dlp
import os
import time
from dotenv import load_dotenv
from audio_config import (
    get_ytdl_options, 
    get_ffmpeg_options, 
    log_debug, 
    format_duration, 
    validate_audio_url,
    ERROR_MESSAGES,
    PERFORMANCE_CONFIG
)

# Cargar variables de entorno
load_dotenv()

# Cola de reproducción global
song_queue = []
voice_client = None
current_song = None
is_processing = False
last_activity = time.time()

# Usar configuración optimizada
YTDL_OPTIONS = get_ytdl_options(debug=False)
# Crear instancia de yt-dlp
ydl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

# Crear instancia del bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Función para obtener la fuente de audio usando yt-dlp
async def get_audio_source(url):
    global last_activity
    last_activity = time.time()
    
    loop = asyncio.get_running_loop()
    start_time = time.time()
    
    try:
        log_debug(f"Iniciando extracción para: {url[:50]}...", "extraction")
        
        # Extraer información sin descargar con timeout
        data = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False)),
            timeout=PERFORMANCE_CONFIG['extraction_timeout']
        )
        
        # Si es una playlist, tomar el primer elemento
        if 'entries' in data:
            if not data['entries']:
                log_debug("La playlist está vacía", "extraction")
                return None, None, None, None
            data = data['entries'][0]
        
        # Verificar que tenemos los datos necesarios
        if not data:
            log_debug("No se pudieron extraer datos del video", "extraction")
            return None, None, None, None
            
        audio_url = data.get('url')
        title = data.get('title', 'Título desconocido')
        duration = data.get('duration')
        uploader = data.get('uploader', 'Canal desconocido')
        
        # Verificar que tenemos una URL de audio válida
        if not validate_audio_url(audio_url):
            log_debug("URL de audio no válida", "extraction")
            return None, None, None, None
        
        extraction_time = time.time() - start_time
        log_debug(f"Extracción exitosa en {extraction_time:.2f}s: {title}", "extraction")
        
        return audio_url, title, duration, uploader
        
    except asyncio.TimeoutError:
        log_debug(f"Timeout en extracción después de {PERFORMANCE_CONFIG['extraction_timeout']}s", "extraction")
        return None, None, None, None
    except Exception as e:
        log_debug(f"Error en extracción: {e}", "extraction")
        return None, None, None, None

async def connect_to_voice(ctx):
    global voice_client
    channel = ctx.author.voice.channel
    if not channel:
        await ctx.send("¡Únete a un canal de voz primero!")
        return None
    if voice_client is None or not voice_client.is_connected():
        try:
            voice_client = await channel.connect()
        except discord.ClientException:
            await ctx.send("Ya estoy conectado a un canal de voz.")
            return voice_client
        except discord.opus.OpusNotLoaded:
            await ctx.send("La librería opus no está cargada. Asegúrate de tener libopus instalado.")
            return None
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)
    return voice_client

async def play_next(ctx):
    global song_queue, voice_client, current_song
    
    if not song_queue:
        current_song = None
        if voice_client and voice_client.is_connected():
            embed = discord.Embed(
                title="🎵 Reproducción terminada",
                description="¡He terminado de reproducir todas las canciones!\n¿Quieres añadir más música?",
                color=0x32cd32
            )
            file = discord.File("nanali.jpg", filename="nanali.jpg")
            embed.set_thumbnail(url="attachment://nanali.jpg")
            embed.set_footer(text="Usa !p <url> para añadir más música • Nanali Music Bot", icon_url="attachment://nanali.jpg")
            await ctx.send(file=file, embed=embed)
        return
    
    # Obtener la siguiente canción
    song_info = song_queue.pop(0)
    current_song = song_info
    
    if voice_client is None or not voice_client.is_connected():
        voice_client = await connect_to_voice(ctx)
        if voice_client is None:
            return
    
    # Usar configuración optimizada de FFmpeg
    FFMPEG_OPTIONS = get_ffmpeg_options('medium')
    
    def after_playing(error):
        if error:
            print(f"Error durante la reproducción: {error}")
        asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
    
    try:
        # Verificar que la URL de audio es válida
        if not validate_audio_url(song_info['url']):
            raise Exception(ERROR_MESSAGES['no_audio_url'])
            
        log_debug(f"Intentando reproducir: {song_info['title']}", "playback")
        log_debug(f"URL de audio: {song_info['url'][:100]}...", "playback")
        
        source = discord.FFmpegPCMAudio(song_info['url'], **FFMPEG_OPTIONS)
        voice_client.play(source, after=after_playing)
        
        # Crear embed para mostrar información de la canción
        embed = discord.Embed(
            title="🎵 Reproduciendo ahora",
            description=f"**{song_info['title']}**",
            color=0x9932cc
        )
        embed.add_field(name="👤 Canal", value=song_info['uploader'], inline=True)
        embed.add_field(name="⏱️ Duración", value=format_duration(song_info['duration']), inline=True)
        embed.add_field(name="📋 En cola", value=str(len(song_queue)), inline=True)
        
        # Añadir imagen de Nanali
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text=f"Solicitado por {song_info['requester']} • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        
        await ctx.send(file=file, embed=embed)
        log_debug(f"Reproducción iniciada exitosamente: {song_info['title']}", "playback")
        
    except Exception as e:
        log_debug(f"Error crítico al reproducir: {e}", "playback")
        embed = discord.Embed(
            title="❌ Error de reproducción",
            description=f"No pude reproducir **{song_info['title']}**.\n\n**Error:** {str(e)[:100]}\n\nSaltando a la siguiente canción...",
            color=0xff4500
        )
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="Continuando con la siguiente • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        await ctx.send(file=file, embed=embed)
        await play_next(ctx)

@bot.command(name="play", aliases=['p'])
async def play_command(ctx, *, url: str):
    global song_queue, voice_client, is_processing
    
    # Verificar si el usuario está en un canal de voz
    if not ctx.author.voice:
        await ctx.send("❌ Debes estar en un canal de voz para usar este comando.")
        return
    
    # Mensaje de procesamiento
    processing_msg = await ctx.send("🔍 Procesando tu solicitud...")
    
    try:
        # Obtener información del audio de forma asíncrona
        audio_url, title, duration, uploader = await get_audio_source(url)
        
        if not audio_url:
            log_debug(f"Fallo en extracción para URL: {url}", "play_command")
            embed = discord.Embed(
                title="❌ Error de procesamiento",
                description="No pude procesar tu solicitud. Por favor verifica:\n• La URL sea válida\n• El video esté disponible\n• Tengas conexión a internet\n• No sea una playlist",
                color=0xff0000
            )
            file = discord.File("nanali.jpg", filename="nanali.jpg")
            embed.set_thumbnail(url="attachment://nanali.jpg")
            embed.set_footer(text="Intenta con otra URL • Nanali Music Bot", icon_url="attachment://nanali.jpg")
            await processing_msg.edit(content="", embed=embed, attachments=[file])
            return
        
        # Crear objeto de canción
        song_info = {
            'url': audio_url,
            'title': title,
            'duration': duration,
            'uploader': uploader,
            'requester': ctx.author.display_name,
            'original_url': url
        }
        
        # Añadir a la cola
        song_queue.append(song_info)
        
        # Crear embed de confirmación
        embed = discord.Embed(
            title="✅ Añadido a la cola",
            description=f"**{title}**",
            color=0x00ff7f
        )
        embed.add_field(name="👤 Canal", value=uploader, inline=True)
        embed.add_field(name="⏱️ Duración", value=format_duration(duration), inline=True)
        embed.add_field(name="📍 Posición en cola", value=str(len(song_queue)), inline=True)
        
        # Añadir imagen de Nanali
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name} • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        
        await processing_msg.edit(content="", embed=embed, attachments=[file])
        
        # Solo iniciar reproducción si no hay nada reproduciéndose
        if voice_client is None or not voice_client.is_playing():
            await play_next(ctx)
            
    except Exception as e:
        log_debug(f"Error en play_command: {e}", "play_command")
        embed = discord.Embed(
            title="❌ Error inesperado",
            description=f"Ocurrió un error inesperado:\n```{str(e)[:200]}```\n\nPor favor intenta de nuevo.",
            color=0xff0000
        )
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="Nanali Music Bot • Error Handler", icon_url="attachment://nanali.jpg")
        await processing_msg.edit(content="", embed=embed, attachments=[file])



# Comando para saltar la canción actual
@bot.command()
async def skip(ctx):
    global voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("¡Canción saltada!")
        await play_next(ctx)
    else:
        await ctx.send("No hay ninguna canción reproduciéndose para saltar.")

# Comando para ver la cola de reproducción
@bot.command(aliases=['q'])
async def queue(ctx):
    global song_queue, current_song
    
    if not current_song and not song_queue:
        await ctx.send("❌ La cola está vacía.")
        return
    
    embed = discord.Embed(
        title="📋 Cola de reproducción",
        color=0xff6b6b
    )
    
    # Mostrar canción actual
    if current_song:
        embed.add_field(
            name="🎵 Reproduciendo ahora",
            value=f"**{current_song['title']}**\n👤 Solicitado por {current_song['requester']}",
            inline=False
        )
    
    # Mostrar próximas canciones (máximo 10)
    if song_queue:
        next_songs = []
        for i, song in enumerate(song_queue[:10]):
            duration_str = ""
            if song['duration']:
                minutes, seconds = divmod(song['duration'], 60)
                duration_str = f" `[{minutes:02d}:{seconds:02d}]`"
            next_songs.append(f"`{i+1}.` **{song['title']}**{duration_str}\n    👤 {song['requester']}")
        
        embed.add_field(
            name=f"⏭️ Próximas canciones ({len(song_queue)} en total)",
            value="\n\n".join(next_songs) if next_songs else "Ninguna",
            inline=False
        )
        
        if len(song_queue) > 10:
            embed.set_footer(text=f"Y {len(song_queue) - 10} canciones más... • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        else:
            embed.set_footer(text="Nanali Music Bot", icon_url="attachment://nanali.jpg")
    
    # Añadir imagen de Nanali
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    
    await ctx.send(file=file, embed=embed)

# Comando para ver la canción que se está reproduciendo actualmente
@bot.command(aliases=['np'])
async def nowplaying(ctx):
    global voice_client, current_song
    
    if not voice_client or not voice_client.is_playing() or not current_song:
        await ctx.send("❌ No hay ninguna canción reproduciéndose actualmente.")
        return
    
    embed = discord.Embed(
        title="🎵 Reproduciendo ahora",
        description=f"**{current_song['title']}**",
        color=0x9932cc
    )
    embed.add_field(name="👤 Canal", value=current_song['uploader'], inline=True)
    if current_song['duration']:
        minutes, seconds = divmod(current_song['duration'], 60)
        embed.add_field(name="⏱️ Duración", value=f"{minutes:02d}:{seconds:02d}", inline=True)
    embed.add_field(name="📋 En cola", value=str(len(song_queue)), inline=True)
    
    # Añadir imagen de Nanali
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text=f"Solicitado por {current_song['requester']} • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    
    await ctx.send(file=file, embed=embed)

@bot.command()
async def stop(ctx):
    global voice_client
    global song_queue
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        song_queue = []  # Limpiar la cola al detener
        await ctx.send("¡Reproducción detenida y la cola ha sido limpiada!")
    else:
        await ctx.send("No hay nada reproduciéndose.")

@bot.command()
async def leave(ctx):
    global voice_client
    global song_queue
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        voice_client = None
        song_queue = []  # Limpiar la cola al desconectar
        await ctx.send("¡Me desconecté del canal de voz y la cola ha sido limpiada!")
    else:
        await ctx.send("No estoy conectado a ningún canal de voz.")

# Evento cuando el bot se conecta correctamente
@bot.event
async def on_ready():
    print(f'🌸 Nanali Music Bot conectada como {bot.user}')
    print('🎵 Lista para reproducir música!')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, 
            name="🎵 música con !help_music"
        ), 
        status=discord.Status.online
    )

# Evento para procesar mensajes y verificar menciones
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mention in message.content:
        parts = message.content.split()
        if len(parts) > 1:
            command = parts[1].lower()
            if command == 'pollo' and len(parts) > 2:
                url = parts[2]
                await play_command(message, url=url)
                return
            elif command == 'play' and len(parts) > 2:
                url = parts[2]
                await play_command(message, url=url)

    await bot.process_commands(message)

# Nuevos comandos adicionales
@bot.command()
async def shuffle(ctx):
    """Mezcla aleatoriamente la cola de reproducción"""
    global song_queue
    if len(song_queue) < 2:
        await ctx.send("❌ Necesitas al menos 2 canciones en la cola para mezclar.")
        return
    
    import random
    random.shuffle(song_queue)
    embed = discord.Embed(
        title="🔀 Cola mezclada",
        description=f"¡Perfecto! He mezclado **{len(song_queue)} canciones** aleatoriamente.",
        color=0xffd700
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Ahora la música será más sorprendente! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)

@bot.command()
async def clear(ctx):
    """Limpia toda la cola de reproducción"""
    global song_queue
    if not song_queue:
        await ctx.send("❌ La cola ya está vacía.")
        return
    
    cleared_count = len(song_queue)
    song_queue.clear()
    embed = discord.Embed(
        title="🗑️ Cola limpiada",
        description=f"He eliminado **{cleared_count} canciones** de la cola.\n¡Lista para nuevas aventuras musicales!",
        color=0xff4500
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="Cola limpia y lista • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)

@bot.command()
async def remove(ctx, position: int):
    """Elimina una canción específica de la cola"""
    global song_queue
    if not song_queue:
        await ctx.send("❌ La cola está vacía.")
        return
    
    if position < 1 or position > len(song_queue):
        await ctx.send(f"❌ Posición inválida. Usa un número entre 1 y {len(song_queue)}.")
        return
    
    removed_song = song_queue.pop(position - 1)
    embed = discord.Embed(
        title="🗑️ Canción eliminada",
        description=f"He eliminado **{removed_song['title']}** de la posición {position}.",
        color=0xff6347
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="Canción eliminada exitosamente • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)

@bot.command(aliases=['vol', 'v'])
async def volume(ctx, vol: int = None):
    """Ajusta el volumen (0-150) - ¡Ahora con boost!"""
    global voice_client
    if not voice_client or not voice_client.is_playing():
        embed = discord.Embed(
            title="❌ Sin reproducción",
            description="No hay música reproduciéndose actualmente.",
            color=0xff0000
        )
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="Usa !p <url> para reproducir música • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        await ctx.send(file=file, embed=embed)
        return
    
    if vol is None:
        current_vol = int(getattr(voice_client.source, 'volume', 1.0) * 100)
        embed = discord.Embed(
            title="🔊 Control de Volumen",
            description=f"**Volumen actual:** {current_vol}%\n\n**Uso:** `!volume <0-150>`\n• 0-100: Volumen normal\n• 101-150: Modo boost 🚀",
            color=0x00bfff
        )
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="¡Controla tu experiencia musical! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        await ctx.send(file=file, embed=embed)
        return
    
    if vol < 0 or vol > 150:
        embed = discord.Embed(
            title="❌ Volumen inválido",
            description="El volumen debe estar entre **0-150**\n• 0-100: Normal\n• 101-150: Boost mode 🚀",
            color=0xff4500
        )
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="Rango válido: 0-150 • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        await ctx.send(file=file, embed=embed)
        return
    
    # Aplicar volumen con transformación
    if hasattr(voice_client.source, 'volume'):
        voice_client.source.volume = vol / 100
    
    # Crear embed de confirmación
    if vol <= 100:
        emoji = "🔊" if vol > 50 else "🔉" if vol > 0 else "🔇"
        mode = "Normal"
        color = 0x00ff00
    else:
        emoji = "🚀"
        mode = "BOOST MODE"
        color = 0xff6600
    
    embed = discord.Embed(
        title=f"{emoji} Volumen ajustado",
        description=f"**Volumen:** {vol}% ({mode})\n\n{get_volume_bar(vol)}",
        color=color
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Disfruta tu música! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)

def get_volume_bar(volume):
    """Genera una barra visual de volumen"""
    filled = int(volume / 10)
    empty = 10 - filled
    if volume <= 100:
        bar = "🟩" * filled + "⬜" * empty
    else:
        normal_filled = 10
        boost_filled = int((volume - 100) / 5)
        bar = "🟩" * normal_filled + "🟧" * min(boost_filled, 10)
    return f"`{bar}` {volume}%"

@bot.command()
async def help_music(ctx):
    """Muestra todos los comandos de música disponibles"""
    embed = discord.Embed(
        title="🎵 Nanali Music Bot v3.0 - Comandos Completos",
        description="¡Konnichiwa! Soy Nanali, tu bot de música otaku 🌸\n\n**¡Ahora con funciones premium y temática anime!**",
        color=0xff69b4
    )
    
    # Comandos básicos
    basic_commands = [
        ("🎵 !play <url> (o !p)", "Reproduce música de alta calidad"),
        ("🔍 !search <término>", "Busca música con selección interactiva"),
        ("⏭️ !skip", "Salta la canción actual"),
        ("⏹️ !stop", "Detiene la reproducción y limpia la cola"),
        ("🚪 !leave", "Me desconecto del canal de voz")
    ]
    
    # Comandos de gestión
    queue_commands = [
        ("📋 !queue (o !q)", "Muestra la cola de reproducción"),
        ("🎵 !nowplaying (o !np)", "Muestra la canción actual"),
        ("🔀 !shuffle", "Mezcla aleatoriamente la cola"),
        ("🗑️ !clear", "Limpia toda la cola"),
        ("❌ !remove <posición>", "Elimina una canción específica"),
        ("🔄 !loop <song/queue/off>", "Modo repetición avanzado")
    ]
    
    # Comandos otaku/anime
    anime_commands = [
        ("🌸 !weeb (o !anime)", "Menú completo de comandos otaku"),
        ("🎵 !anime_op", "Openings de anime aleatorios"),
        ("🎶 !anime_ed", "Endings emotivos de anime"),
        ("🎼 !vocaloid", "Música de Hatsune Miku y más"),
        ("🌸 !kawaii", "J-Pop y música kawaii"),
        ("⚡ !epic_anime", "Música épica de peleas"),
        ("🎭 !character <nombre>", "Música de personajes específicos")
    ]
    
    # Comandos avanzados
    advanced_commands = [
        ("🔊 !volume <0-150> (o !v)", "Control de volumen con boost"),
        ("🎛️ !bass_boost <0-4>", "Ecualizador y efectos de audio"),
        ("ℹ️ !nanali", "Información sobre mí"),
        ("📊 !stats", "Estadísticas del servidor"),
        ("❓ !help_music", "Este menú de ayuda")
    ]
    
    embed.add_field(name="🎮 Comandos Básicos", value="\n".join([f"**{cmd}**\n{desc}" for cmd, desc in basic_commands]), inline=False)
    embed.add_field(name="📋 Gestión de Cola", value="\n".join([f"**{cmd}**\n{desc}" for cmd, desc in queue_commands]), inline=False)
    embed.add_field(name="🌸 Comandos Otaku", value="\n".join([f"**{cmd}**\n{desc}" for cmd, desc in anime_commands]), inline=False)
    embed.add_field(name="⚙️ Comandos Avanzados", value="\n".join([f"**{cmd}**\n{desc}" for cmd, desc in advanced_commands]), inline=False)
    
    embed.add_field(
        name="✨ Características Premium",
        value="• Audio en calidad 320kbps\n• Modo boost hasta 150%\n• Ecualizador integrado\n• Playlists temáticas\n• Búsqueda interactiva\n• Repetición avanzada",
        inline=False
    )
    
    # Añadir imagen de Nanali
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Hecho con amor por una otaku! • Nanali Music Bot v3.0", icon_url="attachment://nanali.jpg")
    
    await ctx.send(file=file, embed=embed)

@bot.command()
async def nanali(ctx):
    """Información completa sobre Nanali"""
    embed = discord.Embed(
        title="🌸 ¡Konnichiwa! Soy Nanali",
        description="Tu bot de música otaku con personalidad kawaii y funciones premium 💖\n\n*¡Ahora con calidad de audio superior y temática anime!*",
        color=0xff1493
    )
    
    embed.add_field(
        name="🎵 ¿Qué puedo hacer?",
        value="• Reproducir música en **calidad 320kbps**\n• Playlists temáticas de anime\n• Búsqueda interactiva avanzada\n• Control de volumen con boost (hasta 150%)\n• Ecualizador y efectos de audio\n• Auto-desconexión inteligente",
        inline=False
    )
    
    embed.add_field(
        name="🌸 Características Otaku",
        value="• Openings y endings de anime\n• Música de Vocaloid (Miku, Rin, Len...)\n• J-Pop y música kawaii\n• OSTs épicos de anime\n• Búsqueda por personajes\n• Playlists curadas por otakus",
        inline=False
    )
    
    embed.add_field(
        name="⚡ Funciones Premium",
        value="• Sistema de cola sin distorsión\n• Modo repetición avanzado\n• Bass boost y ecualizador\n• Interfaz visual mejorada\n• Procesamiento asíncrono\n• Estadísticas del servidor",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Comandos rápidos",
        value="• `!p <url>` - Reproducir música\n• `!search <término>` - Buscar música\n• `!weeb` - Comandos otaku\n• `!anime_op` - Opening aleatorio\n• `!help_music` - Todos los comandos",
        inline=False
    )
    
    embed.add_field(
        name="📊 Versión Actual",
        value="**Nanali Music Bot v3.0**\n• Calidad de audio mejorada\n• Nuevos comandos otaku\n• Interfaz completamente renovada\n• Funciones premium integradas",
        inline=False
    )
    
    # Añadir imagen de Nanali
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_image(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Creada con amor por una otaku para otakus! • Nanali Music Bot v3.0")
    
    await ctx.send(file=file, embed=embed)

@bot.command()
async def stats(ctx):
    """Muestra estadísticas del bot y servidor"""
    global song_queue, current_song
    
    # Obtener información del servidor
    guild = ctx.guild
    voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
    text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
    
    # Información del bot
    bot_latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="📊 Estadísticas de Nanali Music Bot",
        description="¡Aquí tienes información detallada sobre mi rendimiento! 🌸",
        color=0x00bfff
    )
    
    # Estadísticas del servidor
    embed.add_field(
        name="🏠 Información del Servidor",
        value=f"**Nombre:** {guild.name}\n**Miembros:** {guild.member_count}\n**Canales de voz:** {voice_channels}\n**Canales de texto:** {text_channels}",
        inline=True
    )
    
    # Estadísticas del bot
    embed.add_field(
        name="🤖 Estado del Bot",
        value=f"**Latencia:** {bot_latency}ms\n**Servidores:** {len(bot.guilds)}\n**Versión:** v3.0\n**Estado:** {'🟢 Conectada' if voice_client and voice_client.is_connected() else '🔴 Desconectada'}",
        inline=True
    )
    
    # Estadísticas de música
    queue_length = len(song_queue)
    current_status = "🎵 Reproduciendo" if voice_client and voice_client.is_playing() else "⏸️ Pausada" if voice_client and voice_client.is_paused() else "⏹️ Detenida"
    
    embed.add_field(
        name="🎵 Estado Musical",
        value=f"**Estado:** {current_status}\n**En cola:** {queue_length} canciones\n**Canción actual:** {'✅ Sí' if current_song else '❌ No'}\n**Calidad:** 320kbps",
        inline=True
    )
    
    # Funciones disponibles
    embed.add_field(
        name="⚡ Funciones Activas",
        value=f"**Modo repetición:** {getattr(bot, 'loop_mode', 'off').upper()}\n**Bass boost:** Nivel {getattr(bot, 'bass_level', 0)}\n**Auto-desconexión:** ✅ Activa\n**Búsqueda avanzada:** ✅ Disponible",
        inline=True
    )
    
    # Comandos más usados (simulado)
    embed.add_field(
        name="🔥 Comandos Populares",
        value="1️⃣ `!play` - Reproducir música\n2️⃣ `!anime_op` - Openings de anime\n3️⃣ `!search` - Búsqueda avanzada\n4️⃣ `!vocaloid` - Música Vocaloid\n5️⃣ `!volume` - Control de volumen",
        inline=True
    )
    
    # Información técnica
    embed.add_field(
        name="🛠️ Información Técnica",
        value="**Codec de audio:** Opus\n**Bitrate:** 320kbps\n**Canales:** Estéreo (2)\n**Frecuencia:** 48kHz\n**Buffer:** 512kb",
        inline=True
    )
    
    # Añadir imagen de Nanali
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Estadísticas actualizadas en tiempo real! • Nanali Music Bot v3.0", icon_url="attachment://nanali.jpg")
    
    await ctx.send(file=file, embed=embed)

# ===== COMANDOS TEMÁTICOS ANIME =====

@bot.command()
async def anime_op(ctx):
    """Reproduce openings de anime populares"""
    anime_ops = [
        "Attack on Titan opening 1 Guren no Yumiya",
        "Demon Slayer opening Gurenge",
        "Naruto opening 16 Silhouette",
        "One Piece opening 1 We Are",
        "Dragon Ball Z opening Cha-La Head-Cha-La",
        "Death Note opening 1 The World",
        "Tokyo Ghoul opening Unravel",
        "Fullmetal Alchemist Brotherhood opening 1",
        "My Hero Academia opening 1 The Day",
        "Jujutsu Kaisen opening Kaikai Kitan",
        "Mob Psycho 100 opening 99",
        "One Punch Man opening The Hero"
    ]
    
    import random
    selected_op = random.choice(anime_ops)
    
    embed = discord.Embed(
        title="🎵 Opening de Anime Seleccionado",
        description=f"¡Reproduciendo: **{selected_op}**!",
        color=0xff6b6b
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Disfruta este épico opening! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)
    
    # Buscar y reproducir
    await search_and_play(ctx, selected_op)

@bot.command()
async def anime_ed(ctx):
    """Reproduce endings de anime emotivos"""
    anime_eds = [
        "Attack on Titan ending 1 Utsukushiki Zankoku na Sekai",
        "Naruto Shippuden ending 6 Sign",
        "Fullmetal Alchemist Brotherhood ending 1",
        "Death Note ending 1 Alumina",
        "Tokyo Ghoul ending On My Own",
        "Demon Slayer ending Kamado Tanjiro no Uta",
        "Your Name ending Nandemonaiya",
        "Violet Evergarden ending Michishirube",
        "Anohana ending Secret Base",
        "Clannad ending Dango Daikazoku"
    ]
    
    import random
    selected_ed = random.choice(anime_eds)
    
    embed = discord.Embed(
        title="🎶 Ending de Anime Seleccionado",
        description=f"¡Reproduciendo: **{selected_ed}**!",
        color=0x9370db
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Prepárate para los feels! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)
    
    await search_and_play(ctx, selected_ed)

@bot.command()
async def vocaloid(ctx):
    """Reproduce música de Vocaloid"""
    vocaloid_songs = [
        "Hatsune Miku Senbonzakura",
        "Hatsune Miku World is Mine",
        "Kagamine Rin Len Servant of Evil",
        "Hatsune Miku Tell Your World",
        "GUMI Matryoshka",
        "Hatsune Miku Rolling Girl",
        "Kagamine Rin Kokoro",
        "Hatsune Miku Love is War",
        "IA Kagerou Days",
        "Hatsune Miku Disappearance of Hatsune Miku"
    ]
    
    import random
    selected_song = random.choice(vocaloid_songs)
    
    embed = discord.Embed(
        title="🎼 Vocaloid Seleccionado",
        description=f"¡Reproduciendo: **{selected_song}**!\n\n🎤 ¡La magia de las voces sintéticas!",
        color=0x00ffff
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Miku-Miku beam! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)
    
    await search_and_play(ctx, selected_song)

@bot.command()
async def kawaii(ctx):
    """Reproduce música kawaii y J-Pop"""
    kawaii_songs = [
        "Kyary Pamyu Pamyu PonPonPon",
        "Perfume Polyrhythm",
        "AKB48 Heavy Rotation",
        "Babymetal Gimme Chocolate",
        "Kyary Pamyu Pamyu Fashion Monster",
        "Perfume Chocolate Disco",
        "Morning Musume Love Machine",
        "Momoiro Clover Z Saraba",
        "Scandal Harukaze",
        "Silent Siren Cherry Hunter"
    ]
    
    import random
    selected_song = random.choice(kawaii_songs)
    
    embed = discord.Embed(
        title="🌸 Música Kawaii Seleccionada",
        description=f"¡Reproduciendo: **{selected_song}**!\n\n💖 ¡Prepárate para la ternura máxima!",
        color=0xffb6c1
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="Kawaii desu ne! (◕‿◕) • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)
    
    await search_and_play(ctx, selected_song)

@bot.command()
async def epic_anime(ctx):
    """Reproduce música épica de anime"""
    epic_songs = [
        "Attack on Titan Vogel im Kafig",
        "Demon Slayer Tanjiro no Uta",
        "Naruto Strong and Strike",
        "Dragon Ball Z Ultimate Battle",
        "One Piece Overtaken",
        "Bleach Number One",
        "Fairy Tail Main Theme",
        "Fullmetal Alchemist Brotherhood Lapis Philosophorum",
        "Jujutsu Kaisen Domain Expansion",
        "My Hero Academia You Say Run"
    ]
    
    import random
    selected_song = random.choice(epic_songs)
    
    embed = discord.Embed(
        title="⚡ Música Épica de Anime",
        description=f"¡Reproduciendo: **{selected_song}**!\n\n🔥 ¡Prepárate para la epicidad!",
        color=0xff4500
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡El poder del anime te acompaña! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)
    
    await search_and_play(ctx, selected_song)

@bot.command()
async def character(ctx, *, character_name: str):
    """Busca música relacionada con un personaje de anime"""
    search_query = f"{character_name} anime song theme music"
    
    embed = discord.Embed(
        title="🎭 Búsqueda de Personaje",
        description=f"Buscando música relacionada con: **{character_name}**",
        color=0x8a2be2
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Encontrando la música perfecta! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)
    
    await search_and_play(ctx, search_query)

async def search_and_play(ctx, query):
    """Función auxiliar para buscar y reproducir automáticamente"""
    try:
        search_query = f"ytsearch1:{query}"
        data = await asyncio.get_running_loop().run_in_executor(
            None, lambda: ydl.extract_info(search_query, download=False)
        )
        
        if data and 'entries' in data and data['entries'] and data['entries'][0]:
            entry = data['entries'][0]
            url = f"https://www.youtube.com/watch?v={entry['id']}"
            await play_command(ctx, url=url)
        else:
            await ctx.send(f"❌ No pude encontrar: {query}")
    except Exception as e:
        await ctx.send(f"❌ Error al buscar: {str(e)}")
        print(f"Error en search_and_play: {e}")

# ===== NUEVOS COMANDOS OTAKU/ANIME =====

@bot.command(aliases=['anime', 'otaku'])
async def weeb(ctx):
    """Comandos especiales para otakus 🌸"""
    embed = discord.Embed(
        title="🌸 Modo Otaku Activado",
        description="¡Konnichiwa! Aquí tienes comandos especiales para verdaderos otakus 💖",
        color=0xff69b4
    )
    
    commands = [
        ("🎵 !anime_op", "Reproduce openings de anime aleatorios"),
        ("🎶 !anime_ed", "Reproduce endings de anime"),
        ("🎼 !vocaloid", "Música de Vocaloid (Miku, Rin, Len...)"),
        ("🎮 !game_ost", "OSTs de videojuegos japoneses"),
        ("🌸 !kawaii", "Música kawaii y J-Pop"),
        ("⚡ !epic_anime", "Música épica de anime (peleas, momentos intensos)"),
        ("😢 !sad_anime", "Música emotiva de anime"),
        ("🎭 !character <nombre>", "Busca música relacionada con un personaje")
    ]
    
    embed.add_field(
        name="🎌 Comandos Disponibles",
        value="\n".join([f"**{cmd}**\n{desc}" for cmd, desc in commands]),
        inline=False
    )
    
    embed.add_field(
        name="✨ Características Especiales",
        value="• Playlists curadas por otakus\n• Calidad de audio premium\n• Información detallada del anime\n• Modo aleatorio temático",
        inline=False
    )
    
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_image(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Hecho con amor por una otaku! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    
    await ctx.send(file=file, embed=embed)

@bot.command()
async def search(ctx, *, query: str):
    """Busca música en YouTube con resultados múltiples"""
    if not ctx.author.voice:
        await ctx.send("❌ Debes estar en un canal de voz para usar este comando.")
        return
    
    processing_msg = await ctx.send("🔍 Buscando música...")
    
    try:
        # Buscar múltiples resultados
        search_query = f"ytsearch5:{query}"
        data = await asyncio.get_running_loop().run_in_executor(
            None, lambda: ydl.extract_info(search_query, download=False)
        )
        
        if not data or 'entries' not in data or not data['entries']:
            embed = discord.Embed(
                title="❌ Sin resultados",
                description=f"No encontré resultados para: **{query}**",
                color=0xff0000
            )
            file = discord.File("nanali.jpg", filename="nanali.jpg")
            embed.set_thumbnail(url="attachment://nanali.jpg")
            embed.set_footer(text="Intenta con otros términos • Nanali Music Bot", icon_url="attachment://nanali.jpg")
            await processing_msg.edit(content="", embed=embed, attachments=[file])
            return
        
        # Crear embed con resultados
        embed = discord.Embed(
            title="🔍 Resultados de búsqueda",
            description=f"Encontré estas canciones para: **{query}**\n\nReacciona con el número para seleccionar:",
            color=0x00bfff
        )
        
        results = []
        for i, entry in enumerate(data['entries'][:5]):
            if entry:
                duration = entry.get('duration', 0)
                duration_str = f"{duration//60:02d}:{duration%60:02d}" if duration else "N/A"
                uploader = entry.get('uploader', 'Desconocido')[:20]
                title = entry.get('title', 'Sin título')[:50]
                
                embed.add_field(
                    name=f"{i+1}️⃣ {title}",
                    value=f"👤 {uploader} | ⏱️ {duration_str}",
                    inline=False
                )
                results.append(entry)
        
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="Tienes 30 segundos para elegir • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        
        msg = await processing_msg.edit(content="", embed=embed, attachments=[file])
        
        # Añadir reacciones
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for i in range(len(results)):
            await msg.add_reaction(reactions[i])
        
        # Esperar reacción del usuario
        def check(reaction, user):
            return (
                user == ctx.author and 
                str(reaction.emoji) in reactions[:len(results)] and 
                reaction.message.id == msg.id
            )
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            selected_index = reactions.index(str(reaction.emoji))
            selected_entry = results[selected_index]
            
            # Reproducir la canción seleccionada
            url = f"https://www.youtube.com/watch?v={selected_entry['id']}"
            await play_command(ctx, url=url)
            
        except asyncio.TimeoutError:
            embed.set_footer(text="⏰ Tiempo agotado • Nanali Music Bot", icon_url="attachment://nanali.jpg")
            await msg.edit(embed=embed)
            
    except Exception as e:
        await processing_msg.edit(content=f"❌ Error en la búsqueda: {str(e)}")
        print(f"Error en search: {e}")

@bot.command(aliases=['loop', 'repeat'])
async def loop_song(ctx, mode: str = None):
    """Activa/desactiva el modo repetición (song/queue/off)"""
    global loop_mode, current_song
    
    if not hasattr(bot, 'loop_mode'):
        bot.loop_mode = 'off'
    
    if mode is None:
        embed = discord.Embed(
            title="🔄 Modo Repetición",
            description=f"**Estado actual:** {bot.loop_mode.upper()}\n\n**Modos disponibles:**\n• `song` - Repite la canción actual\n• `queue` - Repite toda la cola\n• `off` - Sin repetición",
            color=0x9932cc
        )
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="Uso: !loop <song/queue/off> • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        await ctx.send(file=file, embed=embed)
        return
    
    if mode.lower() not in ['song', 'queue', 'off']:
        await ctx.send("❌ Modo inválido. Usa: `song`, `queue` o `off`")
        return
    
    bot.loop_mode = mode.lower()
    
    mode_emojis = {'song': '🔂', 'queue': '🔁', 'off': '⏹️'}
    mode_names = {'song': 'Canción actual', 'queue': 'Cola completa', 'off': 'Desactivado'}
    
    embed = discord.Embed(
        title=f"{mode_emojis[bot.loop_mode]} Repetición configurada",
        description=f"**Modo:** {mode_names[bot.loop_mode]}\n\n{get_loop_description(bot.loop_mode)}",
        color=0x00ff00 if bot.loop_mode != 'off' else 0x808080
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Configuración guardada! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)

def get_loop_description(mode):
    descriptions = {
        'song': '🎵 La canción actual se repetirá infinitamente',
        'queue': '🔄 Toda la cola se repetirá cuando termine',
        'off': '⏹️ Sin repetición, reproducción normal'
    }
    return descriptions.get(mode, '')

@bot.command(aliases=['eq', 'equalizer'])
async def bass_boost(ctx, level: int = None):
    """Aplica efectos de audio (bass boost, etc.)"""
    if level is None:
        embed = discord.Embed(
            title="🎛️ Ecualizador de Audio",
            description="**Niveles disponibles:**\n• `0` - Audio normal\n• `1` - Bass boost ligero\n• `2` - Bass boost medio\n• `3` - Bass boost intenso\n• `4` - BASS EXTREMO 💥",
            color=0xff6600
        )
        file = discord.File("nanali.jpg", filename="nanali.jpg")
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(text="Uso: !bass_boost <0-4> • Nanali Music Bot", icon_url="attachment://nanali.jpg")
        await ctx.send(file=file, embed=embed)
        return
    
    if level < 0 or level > 4:
        await ctx.send("❌ Nivel inválido. Usa un número entre 0-4.")
        return
    
    # Guardar configuración de bass boost
    bot.bass_level = level
    
    level_names = ['Normal', 'Ligero', 'Medio', 'Intenso', 'EXTREMO 💥']
    level_emojis = ['🎵', '🎶', '🎸', '🔊', '💥']
    
    embed = discord.Embed(
        title=f"{level_emojis[level]} Bass Boost Configurado",
        description=f"**Nivel:** {level_names[level]}\n\n{'⚠️ El efecto se aplicará en la próxima canción' if level > 0 else '✅ Audio normal restaurado'}",
        color=0xff6600 if level > 0 else 0x00ff00
    )
    file = discord.File("nanali.jpg", filename="nanali.jpg")
    embed.set_thumbnail(url="attachment://nanali.jpg")
    embed.set_footer(text="¡Configuración guardada! • Nanali Music Bot", icon_url="attachment://nanali.jpg")
    await ctx.send(file=file, embed=embed)

# Ejecutar el bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: No se encontró el token de Discord. Crea un archivo .env con DISCORD_TOKEN=tu_token")
    else:
        bot.run(token)