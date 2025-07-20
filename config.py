# 🌸 Nanali Music Bot v3.0 - Configuración Avanzada
# Configuraciones personalizables para optimizar la experiencia

import discord
from typing import Dict, List, Tuple

# ═══════════════════════════════════════════════════════════════
# 🎵 CONFIGURACIÓN DE AUDIO PREMIUM
# ═══════════════════════════════════════════════════════════════

# Configuraciones de calidad de audio
AUDIO_QUALITY = {
    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'force-ipv4': True,
    'cachedir': False,
    'youtube_include_dash_manifest': False,
    'extractaudio': True,
    'audioformat': 'opus',
    'audioquality': '320K',
    'prefer_ffmpeg': True,
    'geo_bypass': True,
    'age_limit': 18,
    'retries': 3,
    'fragment_retries': 3,
    'skip_unavailable_fragments': True,
    'keep_fragments': False,
    'buffersize': 1024,
    'http_chunk_size': 10485760,
}

# Opciones FFmpeg optimizadas para máxima calidad
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
    'options': '-vn -b:a 320k -bufsize 512k -ar 48000 -ac 2 -acodec libopus -compression_level 10 -frame_duration 60 -application audio'
}

# ═══════════════════════════════════════════════════════════════
# 🎌 PLAYLISTS TEMÁTICAS OTAKU
# ═══════════════════════════════════════════════════════════════

# Openings de anime épicos
ANIME_OPENINGS = [
    "Attack on Titan OP 1 Guren no Yumiya",
    "Demon Slayer OP 1 Gurenge",
    "Jujutsu Kaisen OP 1 Kaikai Kitan",
    "My Hero Academia OP 1 The Day",
    "One Piece OP 1 We Are",
    "Naruto OP 1 Rocks",
    "Dragon Ball Z OP Rock the Dragon",
    "Death Note OP 1 The World",
    "Tokyo Ghoul OP 1 Unravel",
    "Fullmetal Alchemist OP 1 Again",
    "One Punch Man OP 1 The Hero",
    "Mob Psycho 100 OP 1 99",
    "Hunter x Hunter OP 1 Departure",
    "Bleach OP 1 Asterisk",
    "Fairy Tail OP 1 Snow Fairy",
    "Sword Art Online OP 1 Crossing Field",
    "Code Geass OP 1 Colors",
    "Evangelion OP Cruel Angel's Thesis",
    "Cowboy Bebop OP Tank",
    "JoJo's Bizarre Adventure OP 1 Sono Chi no Sadame"
]

# Endings emotivos de anime
ANIME_ENDINGS = [
    "Your Name ED Nandemonaiya",
    "Demon Slayer ED 1 from the edge",
    "Attack on Titan ED 1 Utsukushiki Zankoku na Sekai",
    "Violet Evergarden ED Michishirube",
    "Clannad ED Dango Daikazoku",
    "Angel Beats ED Ichiban no Takaramono",
    "Anohana ED Secret Base",
    "Your Lie in April ED Orange",
    "Spirited Away ED Always With Me",
    "Grave of the Fireflies ED Home Sweet Home",
    "Tokyo Ghoul ED Saints",
    "Naruto ED 1 Wind",
    "Fullmetal Alchemist ED 1 Kesenai Tsumi",
    "Death Note ED 1 Alumina",
    "Bleach ED 1 Life is Like a Boat",
    "One Piece ED 1 Memories",
    "Hunter x Hunter ED 1 Just Awake",
    "Code Geass ED 1 Yuukyou Seishunka",
    "Evangelion ED Fly Me to the Moon",
    "Cowboy Bebop ED The Real Folk Blues"
]

# Música Vocaloid
VOCALOID_SONGS = [
    "Hatsune Miku Senbonzakura",
    "Hatsune Miku World is Mine",
    "Hatsune Miku Tell Your World",
    "Kagamine Rin Len Servant of Evil",
    "Megurine Luka Just Be Friends",
    "Hatsune Miku Rolling Girl",
    "Hatsune Miku Love is War",
    "Kagamine Rin Kokoro",
    "Hatsune Miku Disappearance of Hatsune Miku",
    "IA Kagerou Days",
    "Gumi Matryoshka",
    "Hatsune Miku Two-Faced Lovers",
    "Kagamine Len Spice",
    "Megurine Luka Double Lariat",
    "Hatsune Miku Miracle Paint",
    "GUMI Mozaik Role",
    "Hatsune Miku Ghost Rule",
    "Kagamine Rin Tokyo Teddy Bear",
    "Hatsune Miku Sand Planet",
    "IA Six Trillion Years and Overnight Story"
]

# J-Pop y música kawaii
KAWAII_JPOP = [
    "Kyary Pamyu Pamyu PONPONPON",
    "Perfume Polyrhythm",
    "AKB48 Heavy Rotation",
    "Babymetal Gimme Chocolate",
    "Kyary Pamyu Pamyu Fashion Monster",
    "Perfume Chocolate Disco",
    "Morning Musume Love Machine",
    "Momoiro Clover Z Saraba Itoshiki Kanashimi-tachi yo",
    "BiSH Orchestra",
    "Babymetal Karate",
    "Kyary Pamyu Pamyu Ninja Re Bang Bang",
    "Perfume Flash",
    "AKB48 Koisuru Fortune Cookie",
    "Nogizaka46 Influencer",
    "Keyakizaka46 Silent Majority",
    "Little Glee Monster Sekai wa Anata ni Waraikaketeiru",
    "E-girls Follow Me",
    "Twice TT Japanese Version",
    "BLACKPINK DDU-DU DDU-DU Japanese Version",
    "Red Velvet Psycho Japanese Version"
]

# OSTs épicos de anime
EPIC_ANIME_OST = [
    "Attack on Titan YouSeeBIGGIRL",
    "Demon Slayer Kamado Tanjiro no Uta",
    "Naruto Strong and Strike",
    "Dragon Ball Z Ultimate Battle",
    "One Piece Overtaken",
    "Bleach Number One",
    "Fullmetal Alchemist Brothers",
    "Death Note L's Theme",
    "Tokyo Ghoul Licht und Schatten",
    "Hunter x Hunter Kingdom of Predators",
    "My Hero Academia You Say Run",
    "Jujutsu Kaisen Domain Expansion",
    "One Punch Man Seigi Shikkou",
    "Mob Psycho 100 Explosion",
    "Code Geass Madder Sky",
    "Evangelion Decisive Battle",
    "Cowboy Bebop Rush",
    "JoJo's Bizarre Adventure Giorno's Theme",
    "Fairy Tail Dragon Force",
    "Sword Art Online Swordland"
]

# ═══════════════════════════════════════════════════════════════
# 🎨 CONFIGURACIÓN VISUAL
# ═══════════════════════════════════════════════════════════════

# Colores temáticos para embeds
COLORS = {
    'primary': 0xFF69B4,      # Rosa kawaii principal
    'success': 0x00FF7F,      # Verde éxito
    'warning': 0xFFD700,      # Amarillo advertencia
    'error': 0xFF4444,        # Rojo error
    'info': 0x87CEEB,         # Azul información
    'music': 0xFF1493,        # Rosa música
    'queue': 0xDA70D6,        # Orquídea cola
    'otaku': 0xFF6347,        # Tomate otaku
    'premium': 0xFFD700,      # Oro premium
    'nanali': 0xFF69B4        # Rosa Nanali
}

# Emojis temáticos
EMOJIS = {
    'music': '🎵',
    'play': '▶️',
    'pause': '⏸️',
    'stop': '⏹️',
    'skip': '⏭️',
    'queue': '📋',
    'shuffle': '🔀',
    'repeat': '🔁',
    'volume': '🔊',
    'mute': '🔇',
    'search': '🔍',
    'loading': '⏳',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'kawaii': '🌸',
    'anime': '🎌',
    'otaku': '👺',
    'heart': '💖',
    'star': '⭐',
    'sparkles': '✨',
    'notes': '🎶',
    'headphones': '🎧',
    'microphone': '🎤',
    'guitar': '🎸',
    'drum': '🥁',
    'trumpet': '🎺'
}

# ═══════════════════════════════════════════════════════════════
# ⚙️ CONFIGURACIÓN DEL BOT
# ═══════════════════════════════════════════════════════════════

# Configuraciones generales
BOT_CONFIG = {
    'command_prefix': '!',
    'case_insensitive': True,
    'strip_after_prefix': True,
    'max_queue_size': 100,
    'max_search_results': 5,
    'auto_disconnect_delay': 300,  # 5 minutos
    'search_timeout': 30,  # 30 segundos
    'max_song_duration': 3600,  # 1 hora
    'volume_default': 50,
    'volume_max': 150,
    'bass_boost_levels': 5,
    'reaction_timeout': 30
}

# Intents necesarios
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.voice_states = True
INTENTS.guilds = True
INTENTS.guild_messages = True
INTENTS.guild_reactions = True

# Actividad del bot
ACTIVITY = discord.Activity(
    type=discord.ActivityType.listening,
    name="música kawaii con !help_music 🌸"
)

# ═══════════════════════════════════════════════════════════════
# 🔧 CONFIGURACIÓN AVANZADA
# ═══════════════════════════════════════════════════════════════

# Configuración de bass boost
BASS_BOOST_FILTERS = {
    0: '',  # Sin filtro
    1: '-af "bass=g=2"',
    2: '-af "bass=g=4"',
    3: '-af "bass=g=6"',
    4: '-af "bass=g=8"'
}

# Configuración de loop
LOOP_MODES = {
    'off': 0,
    'song': 1,
    'queue': 2
}

# Mensajes de estado
STATUS_MESSAGES = {
    'connecting': 'Conectando al canal de voz... 🎵',
    'loading': 'Cargando canción... ⏳',
    'playing': 'Reproduciendo música kawaii 🌸',
    'paused': 'Música pausada ⏸️',
    'stopped': 'Reproducción detenida ⏹️',
    'disconnected': 'Desconectado del canal de voz 👋',
    'error': 'Error en la reproducción ❌',
    'queue_empty': 'Cola vacía 📋',
    'search_timeout': 'Tiempo de búsqueda agotado ⏰'
}

# Configuración de permisos requeridos
REQUIRED_PERMISSIONS = [
    'connect',
    'speak',
    'send_messages',
    'embed_links',
    'attach_files',
    'add_reactions',
    'read_message_history',
    'use_external_emojis'
]

# ═══════════════════════════════════════════════════════════════
# 📊 CONFIGURACIÓN DE ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════

# Comandos más populares (para estadísticas)
POPULAR_COMMANDS = [
    '!play', '!queue', '!skip', '!volume', '!search',
    '!anime_op', '!vocaloid', '!kawaii', '!help_music', '!nanali'
]

# Información técnica del bot
BOT_INFO = {
    'version': '3.0',
    'codename': 'Premium Otaku Edition',
    'author': 'Nanali Development Team',
    'description': 'Bot de música kawaii con temática otaku',
    'features': [
        'Audio 320kbps',
        'Búsqueda interactiva',
        'Comandos temáticos anime',
        'Ecualizador integrado',
        'Modo boost hasta 150%',
        'Playlists curadas',
        'Interfaz kawaii'
    ]
}

# ═══════════════════════════════════════════════════════════════
# 🌟 FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════

def get_random_song(playlist_type: str) -> str:
    """Obtiene una canción aleatoria de la playlist especificada"""
    import random
    
    playlists = {
        'anime_op': ANIME_OPENINGS,
        'anime_ed': ANIME_ENDINGS,
        'vocaloid': VOCALOID_SONGS,
        'kawaii': KAWAII_JPOP,
        'epic': EPIC_ANIME_OST
    }
    
    if playlist_type in playlists:
        return random.choice(playlists[playlist_type])
    return None

def get_embed_color(embed_type: str) -> int:
    """Obtiene el color apropiado para el tipo de embed"""
    return COLORS.get(embed_type, COLORS['primary'])

def get_emoji(emoji_type: str) -> str:
    """Obtiene el emoji apropiado para el tipo especificado"""
    return EMOJIS.get(emoji_type, '🎵')

def format_duration(seconds: int) -> str:
    """Formatea la duración en formato MM:SS o HH:MM:SS"""
    if seconds < 3600:
        return f"{seconds // 60:02d}:{seconds % 60:02d}"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def create_volume_bar(volume: int, length: int = 10) -> str:
    """Crea una barra visual de volumen"""
    filled = int((volume / 100) * length)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {volume}%"

def validate_url(url: str) -> bool:
    """Valida si una URL es válida para reproducción"""
    import re
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return bool(youtube_regex.match(url))

# ═══════════════════════════════════════════════════════════════
# 🎯 CONFIGURACIÓN DE DESARROLLO
# ═══════════════════════════════════════════════════════════════

# Configuración para desarrollo/debug
DEBUG_CONFIG = {
    'enable_logging': True,
    'log_level': 'INFO',
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'enable_debug_commands': False,
    'performance_monitoring': True
}

# Límites de rate limiting
RATE_LIMITS = {
    'commands_per_minute': 30,
    'searches_per_hour': 100,
    'queue_additions_per_minute': 10
}

print("🌸 Configuración de Nanali Music Bot v3.0 cargada exitosamente! ✨")