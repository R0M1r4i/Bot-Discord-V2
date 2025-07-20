# 🌸 Nanali Music Bot v3.0 - Documentación Técnica

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Estructura de Archivos](#estructura-de-archivos)
3. [Configuración Avanzada](#configuración-avanzada)
4. [API y Funciones](#api-y-funciones)
5. [Optimizaciones de Audio](#optimizaciones-de-audio)
6. [Sistema de Comandos](#sistema-de-comandos)
7. [Gestión de Errores](#gestión-de-errores)
8. [Monitoreo y Estadísticas](#monitoreo-y-estadísticas)
9. [Contribución](#contribución)
10. [Troubleshooting Avanzado](#troubleshooting-avanzado)

---

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Discord.py    │────│   Nanali Bot    │────│   yt-dlp        │
│   (Interface)   │    │   (Core Logic)  │    │   (Audio Source)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Voice Client  │    │   Queue System  │    │   FFmpeg        │
│   (Audio Out)   │    │   (Management)  │    │   (Processing)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Flujo de Datos

1. **Comando de Usuario** → Discord.py → Bot Command Handler
2. **Procesamiento** → yt-dlp → Extracción de metadata
3. **Audio Pipeline** → FFmpeg → Optimización de calidad
4. **Reproducción** → Voice Client → Canal de voz
5. **Feedback** → Embed Generator → Usuario

### Patrones de Diseño Utilizados

- **Singleton**: Instancia única del bot
- **Observer**: Sistema de eventos de Discord
- **Command Pattern**: Manejo de comandos
- **Factory**: Creación de embeds
- **Strategy**: Diferentes fuentes de audio

---

## 📁 Estructura de Archivos

```
nanali-music-bot/
├── 📄 bot.py                 # Archivo principal del bot
├── ⚙️ config.py             # Configuraciones y constantes
├── 🛠️ utils.py              # Utilidades y funciones auxiliares
├── 🚀 setup.py              # Instalador automático
├── 📋 requirements.txt      # Dependencias de Python
├── 🔒 .env                  # Variables de entorno (sensible)
├── 🚫 .gitignore           # Archivos a ignorar en Git
├── 🖼️ nanali.jpg           # Imagen del bot
├── 📖 README.md            # Documentación principal
├── 📚 TECHNICAL_DOCS.md    # Este archivo
└── 🎬 start.bat/start.sh   # Scripts de inicio
```

### Descripción de Archivos

#### `bot.py` - Core del Bot
- **Líneas 1-50**: Imports y configuración inicial
- **Líneas 51-100**: Configuración de audio y yt-dlp
- **Líneas 101-200**: Sistema de cola y reproducción
- **Líneas 201-300**: Comandos básicos de música
- **Líneas 301-400**: Comandos de gestión de cola
- **Líneas 401-500**: Comandos otaku temáticos
- **Líneas 501-546**: Comandos avanzados y utilidades

#### `config.py` - Configuraciones
- **Audio Quality**: Configuraciones de yt-dlp y FFmpeg
- **Playlists**: Listas curadas de música otaku
- **Visual Config**: Colores, emojis y estilos
- **Bot Settings**: Límites, timeouts y comportamiento

#### `utils.py` - Utilidades
- **MusicUtils**: Funciones de audio y duración
- **EmbedUtils**: Creación de embeds consistentes
- **SearchUtils**: Búsqueda interactiva
- **StatsUtils**: Estadísticas y monitoreo
- **ValidationUtils**: Validación de entrada
- **PerformanceUtils**: Monitoreo de rendimiento

---

## ⚙️ Configuración Avanzada

### Variables de Entorno

```env
# Configuración básica
DISCORD_TOKEN=your_bot_token_here
COMMAND_PREFIX=!

# Configuración de audio
MAX_QUEUE_SIZE=100
DEFAULT_VOLUME=50
MAX_VOLUME=150
AUTO_DISCONNECT_DELAY=300

# Configuración de búsqueda
MAX_SEARCH_RESULTS=5
SEARCH_TIMEOUT=30
REACTION_TIMEOUT=30

# Configuración de desarrollo
DEBUG_MODE=False
LOG_LEVEL=INFO
PERFORMANCE_MONITORING=True
```

### Configuración de Audio Premium

```python
# yt-dlp options para máxima calidad
YTDL_OPTIONS = {
    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
    'audioquality': '320K',
    'audioformat': 'opus',
    'prefer_ffmpeg': True,
    'geo_bypass': True,
    'retries': 3,
    'fragment_retries': 3
}

# FFmpeg options optimizadas
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 320k -bufsize 512k -ar 48000 -ac 2 -acodec libopus'
}
```

---

## 🔧 API y Funciones

### Funciones Principales

#### `get_audio_source(url: str) -> discord.FFmpegPCMAudio`
```python
"""
Extrae y procesa audio de una URL

Args:
    url (str): URL del video/audio
    
Returns:
    discord.FFmpegPCMAudio: Fuente de audio procesada
    
Raises:
    Exception: Si no se puede procesar el audio
"""
```

#### `search_and_play(query: str, ctx) -> bool`
```python
"""
Busca y reproduce música automáticamente

Args:
    query (str): Término de búsqueda
    ctx: Contexto del comando
    
Returns:
    bool: True si se encontró y agregó música
"""
```

#### `create_search_embed(results: List[Dict]) -> Tuple[discord.Embed, List[str]]`
```python
"""
Crea embed de búsqueda interactiva

Args:
    results (List[Dict]): Lista de resultados de búsqueda
    
Returns:
    Tuple[discord.Embed, List[str]]: Embed y lista de reacciones
"""
```

### Sistema de Cola

```python
class QueueSystem:
    def __init__(self):
        self.queue = []           # Cola principal
        self.current_song = None  # Canción actual
        self.loop_mode = 0        # 0=off, 1=song, 2=queue
        self.volume = 50          # Volumen actual
        self.bass_boost = 0       # Nivel de bass boost
    
    def add_song(self, song_info: Dict) -> int:
        """Agrega canción a la cola"""
        
    def get_next_song(self) -> Optional[Dict]:
        """Obtiene la siguiente canción"""
        
    def shuffle_queue(self) -> None:
        """Mezcla la cola aleatoriamente"""
```

---

## 🎵 Optimizaciones de Audio

### Pipeline de Procesamiento

1. **Extracción** (yt-dlp)
   ```python
   # Prioriza formatos de alta calidad
   format_selector = 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio'
   ```

2. **Procesamiento** (FFmpeg)
   ```bash
   # Opciones optimizadas
   -vn                    # Sin video
   -b:a 320k             # Bitrate 320kbps
   -bufsize 512k         # Buffer grande
   -ar 48000             # Sample rate 48kHz
   -ac 2                 # Estéreo
   -acodec libopus       # Codec Opus
   -compression_level 10  # Máxima compresión
   ```

3. **Streaming** (Discord.py)
   ```python
   # Configuración de voice client
   discord.FFmpegPCMAudio(
       source=url,
       before_options=before_opts,
       options=ffmpeg_opts
   )
   ```

### Bass Boost Implementation

```python
BASS_BOOST_FILTERS = {
    0: '',                    # Sin filtro
    1: '-af "bass=g=2"',     # Boost ligero
    2: '-af "bass=g=4"',     # Boost moderado
    3: '-af "bass=g=6"',     # Boost fuerte
    4: '-af "bass=g=8"'      # Boost máximo
}
```

### Gestión de Volumen

```python
def apply_volume(volume: int) -> str:
    """
    Aplica volumen con soporte para boost
    
    0-100: Volumen normal
    101-150: Modo boost con amplificación
    """
    if volume <= 100:
        return f'-filter:a "volume={volume/100}"
    else:
        boost_factor = 1 + ((volume - 100) / 100)
        return f'-filter:a "volume={boost_factor}"
```

---

## 🎮 Sistema de Comandos

### Estructura de Comandos

```python
@bot.command(name='comando', aliases=['alias1', 'alias2'])
async def comando_function(ctx, *, args=None):
    """
    Descripción del comando
    
    Args:
        ctx: Contexto del comando
        args: Argumentos opcionales
    """
    # 1. Validación de permisos
    if not validate_permissions(ctx):
        return
    
    # 2. Procesamiento de argumentos
    processed_args = process_arguments(args)
    
    # 3. Lógica principal
    result = await execute_command_logic(processed_args)
    
    # 4. Respuesta al usuario
    embed = create_response_embed(result)
    await ctx.send(embed=embed, file=discord.File('nanali.jpg'))
    
    # 5. Logging y estadísticas
    stats.log_command_usage(ctx.command.name)
```

### Categorías de Comandos

#### 🎵 Comandos Básicos
- `!play` - Reproducción principal
- `!search` - Búsqueda interactiva
- `!skip` - Saltar canción
- `!stop` - Detener reproducción
- `!leave` - Desconectar bot

#### 📋 Gestión de Cola
- `!queue` - Mostrar cola
- `!nowplaying` - Canción actual
- `!shuffle` - Mezclar cola
- `!clear` - Limpiar cola
- `!remove` - Eliminar canción
- `!loop` - Modo repetición

#### 🌸 Comandos Otaku
- `!weeb` - Menú otaku
- `!anime_op` - Openings de anime
- `!anime_ed` - Endings de anime
- `!vocaloid` - Música Vocaloid
- `!kawaii` - J-Pop kawaii
- `!epic_anime` - OSTs épicos
- `!character` - Por personaje

#### ⚙️ Comandos Avanzados
- `!volume` - Control de volumen
- `!bass_boost` - Ecualizador
- `!stats` - Estadísticas
- `!nanali` - Info del bot
- `!help_music` - Ayuda completa

---

## 🛡️ Gestión de Errores

### Jerarquía de Errores

```python
class NanaliError(Exception):
    """Clase base para errores de Nanali"""
    pass

class AudioError(NanaliError):
    """Errores relacionados con audio"""
    pass

class QueueError(NanaliError):
    """Errores de gestión de cola"""
    pass

class PermissionError(NanaliError):
    """Errores de permisos"""
    pass
```

### Manejo de Errores

```python
async def handle_error(ctx, error: Exception):
    """
    Maneja errores de forma elegante
    """
    if isinstance(error, AudioError):
        embed = create_error_embed(
            "Error de Audio",
            "No se pudo procesar el audio. Verifica la URL."
        )
    elif isinstance(error, QueueError):
        embed = create_error_embed(
            "Error de Cola",
            "Problema con la gestión de la cola de reproducción."
        )
    else:
        embed = create_error_embed(
            "Error Inesperado",
            "Ocurrió un error inesperado. Contacta al administrador."
        )
    
    await ctx.send(embed=embed, file=discord.File('nanali.jpg'))
    
    # Log del error para debugging
    logger.error(f"Error en {ctx.command}: {error}", exc_info=True)
```

### Recuperación Automática

```python
async def auto_recovery():
    """
    Sistema de recuperación automática
    """
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Intentar reconectar
            await reconnect_voice_client()
            break
        except Exception as e:
            retry_count += 1
            await asyncio.sleep(2 ** retry_count)  # Backoff exponencial
    
    if retry_count >= max_retries:
        # Notificar fallo crítico
        await notify_critical_failure()
```

---

## 📊 Monitoreo y Estadísticas

### Métricas Recopiladas

```python
class MetricsCollector:
    def __init__(self):
        self.command_usage = {}      # Uso de comandos
        self.songs_played = 0        # Canciones reproducidas
        self.total_playtime = 0      # Tiempo total de reproducción
        self.error_count = 0         # Errores ocurridos
        self.uptime_start = datetime.utcnow()
        self.latency_history = []    # Historial de latencia
    
    def record_command(self, command: str):
        """Registra uso de comando"""
        self.command_usage[command] = self.command_usage.get(command, 0) + 1
    
    def record_song(self, duration: int):
        """Registra canción reproducida"""
        self.songs_played += 1
        self.total_playtime += duration
    
    def record_error(self, error_type: str):
        """Registra error"""
        self.error_count += 1
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas completas"""
        uptime = datetime.utcnow() - self.uptime_start
        avg_latency = sum(self.latency_history) / len(self.latency_history) if self.latency_history else 0
        
        return {
            'uptime': uptime,
            'commands_executed': sum(self.command_usage.values()),
            'songs_played': self.songs_played,
            'total_playtime': self.total_playtime,
            'error_rate': self.error_count / max(sum(self.command_usage.values()), 1),
            'avg_latency': avg_latency,
            'most_used_commands': sorted(self.command_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        }
```

### Dashboard de Estadísticas

```python
def create_stats_dashboard(stats: Dict) -> discord.Embed:
    """
    Crea un dashboard visual de estadísticas
    """
    embed = discord.Embed(
        title="📊 Dashboard de Nanali Music Bot",
        color=COLORS['premium'],
        timestamp=datetime.utcnow()
    )
    
    # Métricas principales
    embed.add_field(
        name="⏱️ Tiempo Activo",
        value=format_timedelta(stats['uptime']),
        inline=True
    )
    
    embed.add_field(
        name="🎵 Canciones Reproducidas",
        value=f"{stats['songs_played']:,}",
        inline=True
    )
    
    embed.add_field(
        name="📡 Latencia Promedio",
        value=f"{stats['avg_latency']:.1f}ms",
        inline=True
    )
    
    # Gráfico de uso de comandos
    command_chart = create_command_usage_chart(stats['most_used_commands'])
    embed.add_field(
        name="📈 Comandos Más Usados",
        value=command_chart,
        inline=False
    )
    
    return embed
```

---

## 🤝 Contribución

### Guías de Desarrollo

#### Estilo de Código

```python
# Usar type hints
def process_song(song_info: Dict[str, Any]) -> Optional[AudioSource]:
    pass

# Documentar funciones
def complex_function(param1: str, param2: int = 10) -> bool:
    """
    Descripción breve de la función
    
    Args:
        param1 (str): Descripción del parámetro
        param2 (int, optional): Parámetro opcional. Defaults to 10.
    
    Returns:
        bool: Descripción del valor de retorno
    
    Raises:
        ValueError: Cuando param1 está vacío
    """
    pass

# Usar constantes para valores mágicos
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
```

#### Testing

```python
import unittest
from unittest.mock import Mock, patch

class TestMusicUtils(unittest.TestCase):
    def test_format_duration(self):
        """Test duration formatting"""
        self.assertEqual(MusicUtils.format_duration(65), "1:05")
        self.assertEqual(MusicUtils.format_duration(3661), "1:01:01")
    
    @patch('yt_dlp.YoutubeDL')
    def test_audio_extraction(self, mock_ytdl):
        """Test audio extraction"""
        # Setup mock
        mock_ytdl.return_value.extract_info.return_value = {
            'url': 'test_url',
            'title': 'Test Song'
        }
        
        # Test
        result = extract_audio_info('https://youtube.com/watch?v=test')
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], 'Test Song')
```

#### Pull Request Template

```markdown
## 🌸 Descripción
Breve descripción de los cambios realizados.

## 🔧 Tipo de Cambio
- [ ] Bug fix (cambio que corrige un problema)
- [ ] Nueva funcionalidad (cambio que añade funcionalidad)
- [ ] Breaking change (cambio que rompe compatibilidad)
- [ ] Documentación

## 🧪 Testing
- [ ] He probado mis cambios localmente
- [ ] He añadido tests para nuevas funcionalidades
- [ ] Todos los tests existentes pasan

## 📋 Checklist
- [ ] Mi código sigue el estilo del proyecto
- [ ] He realizado una auto-revisión de mi código
- [ ] He comentado mi código, especialmente en áreas complejas
- [ ] He actualizado la documentación correspondiente
```

---

## 🔧 Troubleshooting Avanzado

### Problemas Comunes y Soluciones

#### 1. Audio Distorsionado

**Síntomas:**
- Audio entrecortado o con ruido
- Calidad de audio baja

**Diagnóstico:**
```python
# Verificar configuración de FFmpeg
print(f"FFmpeg options: {FFMPEG_OPTIONS}")

# Verificar bitrate
print(f"Audio bitrate: {YTDL_OPTIONS.get('audioquality')}")

# Verificar latencia de red
latency = await measure_network_latency()
print(f"Network latency: {latency}ms")
```

**Soluciones:**
```python
# Aumentar buffer size
FFMPEG_OPTIONS['options'] += ' -bufsize 1024k'

# Reducir bitrate si hay problemas de red
YTDL_OPTIONS['audioquality'] = '192K'

# Usar reconexión automática
FFMPEG_OPTIONS['before_options'] += ' -reconnect 1'
```

#### 2. Bot No Responde

**Diagnóstico:**
```python
# Verificar estado del bot
print(f"Bot status: {bot.status}")
print(f"Latency: {bot.latency * 1000:.1f}ms")

# Verificar conexiones
print(f"Voice clients: {len(bot.voice_clients)}")
for vc in bot.voice_clients:
    print(f"Guild: {vc.guild.name}, Connected: {vc.is_connected()}")

# Verificar permisos
for guild in bot.guilds:
    perms = guild.me.guild_permissions
    print(f"Guild {guild.name}: Send messages: {perms.send_messages}")
```

**Soluciones:**
```python
# Reiniciar conexión
await bot.close()
await bot.start(TOKEN)

# Limpiar cache
bot.clear()

# Verificar intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
```

#### 3. Memoria Alta

**Diagnóstico:**
```python
import psutil
import gc

# Verificar uso de memoria
process = psutil.Process()
memory_info = process.memory_info()
print(f"RSS: {memory_info.rss / 1024 / 1024:.1f} MB")
print(f"VMS: {memory_info.vms / 1024 / 1024:.1f} MB")

# Verificar objetos en memoria
print(f"Objects in memory: {len(gc.get_objects())}")
```

**Soluciones:**
```python
# Limpiar cola periódicamente
if len(song_queue) > MAX_QUEUE_SIZE:
    song_queue = song_queue[:MAX_QUEUE_SIZE//2]

# Forzar garbage collection
import gc
gc.collect()

# Limpiar cache de yt-dlp
ytdl.cache.remove()
```

### Logging Avanzado

```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('nanali.log', maxBytes=10*1024*1024, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('nanali')

# Logging personalizado
class NanaliLogger:
    @staticmethod
    def log_command(ctx, command_name: str, success: bool):
        user = f"{ctx.author.name}#{ctx.author.discriminator}"
        guild = ctx.guild.name if ctx.guild else "DM"
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"COMMAND {status}: {command_name} by {user} in {guild}")
    
    @staticmethod
    def log_audio_event(event: str, details: str = ""):
        logger.info(f"AUDIO {event}: {details}")
    
    @staticmethod
    def log_error(error: Exception, context: str = ""):
        logger.error(f"ERROR in {context}: {error}", exc_info=True)
```

### Monitoreo en Tiempo Real

```python
import asyncio
from datetime import datetime, timedelta

class HealthMonitor:
    def __init__(self, bot):
        self.bot = bot
        self.last_heartbeat = datetime.utcnow()
        self.error_count = 0
        self.warning_threshold = 5
    
    async def start_monitoring(self):
        """Inicia el monitoreo de salud"""
        while True:
            await self.check_health()
            await asyncio.sleep(60)  # Check every minute
    
    async def check_health(self):
        """Verifica la salud del bot"""
        now = datetime.utcnow()
        
        # Verificar latencia
        if self.bot.latency > 1.0:  # > 1 segundo
            logger.warning(f"High latency detected: {self.bot.latency:.2f}s")
        
        # Verificar conexiones de voz
        for vc in self.bot.voice_clients:
            if not vc.is_connected():
                logger.warning(f"Voice client disconnected in {vc.guild.name}")
                await self.attempt_reconnect(vc)
        
        # Verificar errores recientes
        if self.error_count > self.warning_threshold:
            logger.critical(f"High error rate: {self.error_count} errors")
            await self.notify_admin()
        
        self.last_heartbeat = now
    
    async def attempt_reconnect(self, voice_client):
        """Intenta reconectar un cliente de voz"""
        try:
            await voice_client.disconnect()
            # Lógica de reconexión aquí
            logger.info(f"Reconnected to {voice_client.guild.name}")
        except Exception as e:
            logger.error(f"Failed to reconnect: {e}")
```

---

## 📈 Roadmap de Desarrollo

### v3.1 - Mejoras de Estabilidad
- [ ] Sistema de cache mejorado
- [ ] Reconexión automática más robusta
- [ ] Optimizaciones de memoria
- [ ] Logging estructurado

### v3.2 - Funcionalidades Sociales
- [ ] Sistema de favoritos por usuario
- [ ] Playlists compartidas
- [ ] Votación para saltar canciones
- [ ] Ranking de canciones populares

### v3.3 - Integración Avanzada
- [ ] Comandos slash de Discord
- [ ] Integración con Spotify
- [ ] API REST para control externo
- [ ] Dashboard web

### v4.0 - AI Integration
- [ ] Recomendaciones con IA
- [ ] Reconocimiento de voz
- [ ] Análisis de sentimientos
- [ ] Generación automática de playlists

---

## 📞 Soporte y Contacto

### Canales de Soporte

- **GitHub Issues**: Para bugs y feature requests
- **Discord Server**: Para soporte en tiempo real
- **Email**: Para consultas privadas
- **Documentation**: Para guías y tutoriales

### Información de Contacto

- **Desarrollador Principal**: Nanali Development Team
- **Email**: support@nanali-bot.com
- **Discord**: NanaliBot#1234
- **GitHub**: https://github.com/nanali-music-bot

---

**🌸 ¡Arigatou gozaimasu por contribuir al desarrollo de Nanali Music Bot! 🎵**

*Esta documentación está en constante evolución. Última actualización: v3.0*