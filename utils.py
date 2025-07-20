# 🌸 Nanali Music Bot v3.0 - Utilidades Avanzadas
# Funciones auxiliares y herramientas para mejorar la experiencia

import discord
import asyncio
import aiohttp
import json
import re
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, Union
from config import COLORS, EMOJIS, BOT_CONFIG

# ═══════════════════════════════════════════════════════════════
# 🎵 UTILIDADES DE MÚSICA
# ═══════════════════════════════════════════════════════════════

class MusicUtils:
    """Utilidades relacionadas con música y audio"""
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Formatea la duración en formato legible"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}:{secs:02d}"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            return f"{hours}:{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def create_progress_bar(current: int, total: int, length: int = 20) -> str:
        """Crea una barra de progreso visual"""
        if total == 0:
            return "[" + "░" * length + "] 0%"
        
        progress = current / total
        filled = int(progress * length)
        bar = "█" * filled + "░" * (length - filled)
        percentage = int(progress * 100)
        return f"[{bar}] {percentage}%"
    
    @staticmethod
    def create_volume_bar(volume: int, max_volume: int = 150, length: int = 15) -> str:
        """Crea una barra de volumen con indicador de boost"""
        if volume <= 100:
            filled = int((volume / 100) * length)
            bar = "🔊" + "█" * filled + "░" * (length - filled)
            return f"{bar} {volume}%"
        else:
            # Modo boost
            base_filled = length
            boost_filled = int(((volume - 100) / 50) * 5)  # 5 caracteres para boost
            bar = "🔊" + "█" * base_filled + "🔥" * boost_filled
            return f"{bar} {volume}% (BOOST)"
    
    @staticmethod
    def validate_youtube_url(url: str) -> bool:
        """Valida si una URL de YouTube es válida"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([\w-]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([\w-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([\w-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/([\w-]+)'
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extrae el ID del video de una URL de YouTube"""
        patterns = [
            r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed/)([0-9A-Za-z_-]{11})',
            r'(?:youtu\.be/)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

# ═══════════════════════════════════════════════════════════════
# 🎨 UTILIDADES DE EMBEDS
# ═══════════════════════════════════════════════════════════════

class EmbedUtils:
    """Utilidades para crear embeds atractivos y consistentes"""
    
    @staticmethod
    def create_music_embed(
        title: str,
        description: str = None,
        color: str = 'music',
        thumbnail: bool = True,
        footer: bool = True
    ) -> discord.Embed:
        """Crea un embed estándar para música"""
        embed = discord.Embed(
            title=f"{EMOJIS['music']} {title}",
            description=description,
            color=COLORS.get(color, COLORS['music']),
            timestamp=datetime.utcnow()
        )
        
        if thumbnail:
            embed.set_thumbnail(url="attachment://nanali.jpg")
        
        if footer:
            embed.set_footer(
                text="Nanali Music Bot v3.0 • ¡Hecho con amor por otakus!",
                icon_url="attachment://nanali.jpg"
            )
        
        return embed
    
    @staticmethod
    def create_error_embed(message: str, details: str = None) -> discord.Embed:
        """Crea un embed de error"""
        embed = discord.Embed(
            title=f"{EMOJIS['error']} Error",
            description=message,
            color=COLORS['error'],
            timestamp=datetime.utcnow()
        )
        
        if details:
            embed.add_field(name="Detalles", value=details, inline=False)
        
        embed.add_field(
            name="💡 Sugerencia",
            value="Usa `!help_music` para ver todos los comandos disponibles",
            inline=False
        )
        
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(
            text="Nanali Music Bot v3.0 • Si el problema persiste, contacta al administrador",
            icon_url="attachment://nanali.jpg"
        )
        
        return embed
    
    @staticmethod
    def create_success_embed(message: str, details: str = None) -> discord.Embed:
        """Crea un embed de éxito"""
        embed = discord.Embed(
            title=f"{EMOJIS['success']} ¡Éxito!",
            description=message,
            color=COLORS['success'],
            timestamp=datetime.utcnow()
        )
        
        if details:
            embed.add_field(name="Información", value=details, inline=False)
        
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(
            text="Nanali Music Bot v3.0 • ¡Disfruta tu música kawaii!",
            icon_url="attachment://nanali.jpg"
        )
        
        return embed
    
    @staticmethod
    def create_queue_embed(
        queue: List[Dict],
        current_song: Dict = None,
        page: int = 1,
        per_page: int = 10
    ) -> discord.Embed:
        """Crea un embed para mostrar la cola de reproducción"""
        total_pages = (len(queue) + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        embed = discord.Embed(
            title=f"{EMOJIS['queue']} Cola de Reproducción",
            color=COLORS['queue'],
            timestamp=datetime.utcnow()
        )
        
        if current_song:
            embed.add_field(
                name=f"{EMOJIS['play']} Reproduciendo Ahora",
                value=f"**{current_song.get('title', 'Desconocido')}**\n"
                      f"Duración: {MusicUtils.format_duration(current_song.get('duration', 0))}\n"
                      f"Solicitado por: {current_song.get('requester', 'Desconocido')}",
                inline=False
            )
        
        if queue:
            queue_text = ""
            for i, song in enumerate(queue[start_idx:end_idx], start=start_idx + 1):
                duration = MusicUtils.format_duration(song.get('duration', 0))
                queue_text += f"`{i}.` **{song.get('title', 'Desconocido')}** [{duration}]\n"
            
            embed.add_field(
                name=f"{EMOJIS['notes']} Próximas Canciones (Página {page}/{total_pages})",
                value=queue_text or "No hay canciones en cola",
                inline=False
            )
            
            total_duration = sum(song.get('duration', 0) for song in queue)
            embed.add_field(
                name="📊 Estadísticas",
                value=f"Canciones en cola: **{len(queue)}**\n"
                      f"Tiempo total: **{MusicUtils.format_duration(total_duration)}**",
                inline=True
            )
        else:
            embed.add_field(
                name=f"{EMOJIS['info']} Cola Vacía",
                value="No hay canciones en la cola.\nUsa `!play <url>` para agregar música.",
                inline=False
            )
        
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(
            text="Nanali Music Bot v3.0 • Usa !queue <página> para navegar",
            icon_url="attachment://nanali.jpg"
        )
        
        return embed

# ═══════════════════════════════════════════════════════════════
# 🔍 UTILIDADES DE BÚSQUEDA
# ═══════════════════════════════════════════════════════════════

class SearchUtils:
    """Utilidades para búsqueda y selección de música"""
    
    @staticmethod
    async def create_search_embed(
        results: List[Dict],
        query: str
    ) -> Tuple[discord.Embed, List[str]]:
        """Crea un embed de resultados de búsqueda con reacciones"""
        embed = discord.Embed(
            title=f"{EMOJIS['search']} Resultados de Búsqueda",
            description=f"Búsqueda: **{query}**\n"
                       f"Selecciona una opción reaccionando con el número correspondiente:",
            color=COLORS['info'],
            timestamp=datetime.utcnow()
        )
        
        reactions = []
        number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        
        for i, result in enumerate(results[:5]):
            duration = MusicUtils.format_duration(result.get('duration', 0))
            uploader = result.get('uploader', 'Desconocido')[:30]
            
            embed.add_field(
                name=f"{number_emojis[i]} Opción {i + 1}",
                value=f"**{result.get('title', 'Sin título')[:50]}**\n"
                      f"📺 Canal: {uploader}\n"
                      f"⏱️ Duración: {duration}\n"
                      f"👀 Vistas: {result.get('view_count', 'N/A')}",
                inline=True
            )
            reactions.append(number_emojis[i])
        
        embed.add_field(
            name="⏰ Tiempo Límite",
            value="Tienes 30 segundos para seleccionar una opción.\n"
                  "Reacciona con ❌ para cancelar.",
            inline=False
        )
        
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(
            text="Nanali Music Bot v3.0 • Búsqueda interactiva",
            icon_url="attachment://nanali.jpg"
        )
        
        reactions.append('❌')  # Opción de cancelar
        return embed, reactions
    
    @staticmethod
    async def wait_for_reaction(
        bot,
        message: discord.Message,
        user: discord.User,
        valid_reactions: List[str],
        timeout: int = 30
    ) -> Optional[str]:
        """Espera por una reacción específica del usuario"""
        def check(reaction, reaction_user):
            return (
                reaction_user == user and
                str(reaction.emoji) in valid_reactions and
                reaction.message.id == message.id
            )
        
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=timeout, check=check)
            return str(reaction.emoji)
        except asyncio.TimeoutError:
            return None

# ═══════════════════════════════════════════════════════════════
# 📊 UTILIDADES DE ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════

class StatsUtils:
    """Utilidades para estadísticas y monitoreo"""
    
    def __init__(self):
        self.command_usage = {}
        self.start_time = datetime.utcnow()
        self.songs_played = 0
        self.total_playtime = 0
    
    def log_command_usage(self, command: str):
        """Registra el uso de un comando"""
        self.command_usage[command] = self.command_usage.get(command, 0) + 1
    
    def log_song_played(self, duration: int):
        """Registra una canción reproducida"""
        self.songs_played += 1
        self.total_playtime += duration
    
    def get_uptime(self) -> str:
        """Obtiene el tiempo de actividad del bot"""
        uptime = datetime.utcnow() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"
    
    def get_most_used_commands(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Obtiene los comandos más utilizados"""
        return sorted(self.command_usage.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def create_stats_embed(self, bot, guild: discord.Guild) -> discord.Embed:
        """Crea un embed con estadísticas completas"""
        embed = discord.Embed(
            title=f"{EMOJIS['star']} Estadísticas de Nanali Music Bot",
            color=COLORS['premium'],
            timestamp=datetime.utcnow()
        )
        
        # Estadísticas del bot
        embed.add_field(
            name="🤖 Estado del Bot",
            value=f"Tiempo activo: **{self.get_uptime()}**\n"
                  f"Latencia: **{round(bot.latency * 1000)}ms**\n"
                  f"Versión: **v3.0 Premium**\n"
                  f"Servidores: **{len(bot.guilds)}**",
            inline=True
        )
        
        # Estadísticas del servidor
        embed.add_field(
            name="🏠 Servidor Actual",
            value=f"Nombre: **{guild.name}**\n"
                  f"Miembros: **{guild.member_count}**\n"
                  f"Canales: **{len(guild.channels)}**\n"
                  f"Roles: **{len(guild.roles)}**",
            inline=True
        )
        
        # Estadísticas de música
        avg_duration = self.total_playtime // max(self.songs_played, 1)
        embed.add_field(
            name="🎵 Estadísticas Musicales",
            value=f"Canciones reproducidas: **{self.songs_played}**\n"
                  f"Tiempo total: **{MusicUtils.format_duration(self.total_playtime)}**\n"
                  f"Duración promedio: **{MusicUtils.format_duration(avg_duration)}**\n"
                  f"Comandos ejecutados: **{sum(self.command_usage.values())}**",
            inline=False
        )
        
        # Comandos más populares
        popular_commands = self.get_most_used_commands()
        if popular_commands:
            commands_text = "\n".join([
                f"`{cmd}`: **{count}** usos" for cmd, count in popular_commands
            ])
            embed.add_field(
                name="📈 Comandos Más Populares",
                value=commands_text,
                inline=True
            )
        
        # Funciones activas
        embed.add_field(
            name="⚙️ Funciones Premium Activas",
            value="✅ Audio 320kbps\n"
                  "✅ Búsqueda interactiva\n"
                  "✅ Comandos otaku\n"
                  "✅ Ecualizador bass boost\n"
                  "✅ Volumen boost 150%\n"
                  "✅ Modo repetición avanzado",
            inline=True
        )
        
        embed.set_thumbnail(url="attachment://nanali.jpg")
        embed.set_footer(
            text="Nanali Music Bot v3.0 • Estadísticas en tiempo real",
            icon_url="attachment://nanali.jpg"
        )
        
        return embed

# ═══════════════════════════════════════════════════════════════
# 🛡️ UTILIDADES DE VALIDACIÓN
# ═══════════════════════════════════════════════════════════════

class ValidationUtils:
    """Utilidades para validación y seguridad"""
    
    @staticmethod
    def validate_volume(volume: str) -> Tuple[bool, int, str]:
        """Valida el valor de volumen"""
        try:
            vol = int(volume)
            if 0 <= vol <= BOT_CONFIG['volume_max']:
                return True, vol, None
            else:
                return False, 0, f"El volumen debe estar entre 0 y {BOT_CONFIG['volume_max']}"
        except ValueError:
            return False, 0, "El volumen debe ser un número válido"
    
    @staticmethod
    def validate_queue_position(position: str, queue_length: int) -> Tuple[bool, int, str]:
        """Valida la posición en la cola"""
        try:
            pos = int(position)
            if 1 <= pos <= queue_length:
                return True, pos - 1, None  # Convertir a índice base 0
            else:
                return False, 0, f"La posición debe estar entre 1 y {queue_length}"
        except ValueError:
            return False, 0, "La posición debe ser un número válido"
    
    @staticmethod
    def validate_bass_boost(level: str) -> Tuple[bool, int, str]:
        """Valida el nivel de bass boost"""
        try:
            boost = int(level)
            if 0 <= boost <= BOT_CONFIG['bass_boost_levels'] - 1:
                return True, boost, None
            else:
                return False, 0, f"El nivel debe estar entre 0 y {BOT_CONFIG['bass_boost_levels'] - 1}"
        except ValueError:
            return False, 0, "El nivel debe ser un número válido"
    
    @staticmethod
    def check_user_permissions(member: discord.Member, voice_channel: discord.VoiceChannel) -> Tuple[bool, str]:
        """Verifica los permisos del usuario"""
        if not voice_channel:
            return False, "Debes estar en un canal de voz para usar este comando"
        
        permissions = voice_channel.permissions_for(member)
        if not permissions.connect:
            return False, "No tienes permisos para conectarte a este canal de voz"
        
        if not permissions.speak:
            return False, "No tienes permisos para hablar en este canal de voz"
        
        return True, None
    
    @staticmethod
    def check_bot_permissions(bot_member: discord.Member, voice_channel: discord.VoiceChannel) -> Tuple[bool, str]:
        """Verifica los permisos del bot"""
        permissions = voice_channel.permissions_for(bot_member)
        
        missing_perms = []
        if not permissions.connect:
            missing_perms.append("Conectar")
        if not permissions.speak:
            missing_perms.append("Hablar")
        if not permissions.use_voice_activation:
            missing_perms.append("Usar activación por voz")
        
        if missing_perms:
            return False, f"El bot necesita los siguientes permisos: {', '.join(missing_perms)}"
        
        return True, None

# ═══════════════════════════════════════════════════════════════
# 🎯 UTILIDADES DE PERFORMANCE
# ═══════════════════════════════════════════════════════════════

class PerformanceUtils:
    """Utilidades para monitoreo de rendimiento"""
    
    @staticmethod
    async def measure_latency(bot) -> Dict[str, float]:
        """Mide diferentes tipos de latencia"""
        # Latencia de WebSocket
        websocket_latency = bot.latency * 1000
        
        # Latencia de API (simulada con un ping a Discord)
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://discord.com/api/v10/gateway') as response:
                    await response.json()
            api_latency = (time.time() - start_time) * 1000
        except:
            api_latency = -1
        
        return {
            'websocket': round(websocket_latency, 2),
            'api': round(api_latency, 2) if api_latency > 0 else None
        }
    
    @staticmethod
    def get_memory_usage() -> Dict[str, str]:
        """Obtiene información de uso de memoria (simplificado)"""
        import psutil
        import os
        
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            return {
                'rss': f"{memory_info.rss / 1024 / 1024:.1f} MB",
                'vms': f"{memory_info.vms / 1024 / 1024:.1f} MB",
                'percent': f"{process.memory_percent():.1f}%"
            }
        except ImportError:
            return {
                'rss': "N/A (psutil no instalado)",
                'vms': "N/A",
                'percent': "N/A"
            }

# ═══════════════════════════════════════════════════════════════
# 🌟 INSTANCIA GLOBAL DE ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════

# Instancia global para estadísticas
stats = StatsUtils()

print("🌸 Utilidades de Nanali Music Bot v3.0 cargadas exitosamente! ✨")