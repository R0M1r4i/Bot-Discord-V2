#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración optimizada de audio para Nanali Music Bot
"""

import os
import platform

# Detectar sistema operativo para optimizaciones específicas
OS_TYPE = platform.system().lower()

# Configuración optimizada de yt-dlp
YTDL_OPTIONS_OPTIMIZED = {
    'format': 'bestaudio/best',
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
    # Optimizaciones adicionales
    'extract_flat': False,
    'writethumbnail': False,
    'writeinfojson': False,
    'writesubtitles': False,
    'writeautomaticsub': False,
    'socket_timeout': 30,
    'retries': 3,
    'fragment_retries': 3,
    'skip_unavailable_fragments': True,
    'keep_fragments': False,
    'buffersize': 1024,
    'http_chunk_size': 10485760,  # 10MB chunks
}

# Configuración de FFmpeg optimizada por sistema operativo
if OS_TYPE == 'windows':
    FFMPEG_OPTIONS_OPTIMIZED = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin -loglevel error',
        'options': '-vn -filter:a "volume=0.7" -ac 2 -ar 48000 -b:a 128k -bufsize 64k'
    }
else:  # Linux/macOS
    FFMPEG_OPTIONS_OPTIMIZED = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin -loglevel error',
        'options': '-vn -filter:a "volume=0.7" -ac 2 -ar 48000 -b:a 128k -bufsize 64k'
    }

# Configuración de depuración
DEBUG_CONFIG = {
    'log_audio_urls': True,
    'log_ffmpeg_errors': True,
    'log_extraction_time': True,
    'max_url_display_length': 100,
    'verbose_errors': True
}

# Configuración de rendimiento
PERFORMANCE_CONFIG = {
    'max_queue_size': 50,
    'auto_disconnect_delay': 300,  # 5 minutos
    'extraction_timeout': 30,
    'playback_timeout': 10,
    'max_retries': 3
}

# Mensajes de error personalizados
ERROR_MESSAGES = {
    'no_audio_url': "❌ No se pudo obtener la URL de audio del video",
    'extraction_failed': "❌ Error al extraer información del video",
    'ffmpeg_failed': "❌ Error de FFmpeg durante la reproducción",
    'connection_failed': "❌ Error de conexión al canal de voz",
    'invalid_url': "❌ URL no válida o video no disponible",
    'timeout': "❌ Tiempo de espera agotado",
    'permission_denied': "❌ Sin permisos para reproducir en este canal"
}

# Configuración de calidad de audio por defecto
AUDIO_QUALITY_PRESETS = {
    'low': {
        'bitrate': '96k',
        'sample_rate': '44100',
        'channels': '2',
        'volume': '0.6'
    },
    'medium': {
        'bitrate': '128k',
        'sample_rate': '48000',
        'channels': '2',
        'volume': '0.7'
    },
    'high': {
        'bitrate': '192k',
        'sample_rate': '48000',
        'channels': '2',
        'volume': '0.8'
    }
}

# Configuración actual (medium por defecto)
CURRENT_QUALITY = 'medium'

def get_ffmpeg_options(quality='medium'):
    """Obtiene las opciones de FFmpeg según la calidad especificada"""
    preset = AUDIO_QUALITY_PRESETS.get(quality, AUDIO_QUALITY_PRESETS['medium'])
    
    return {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin -loglevel error',
        'options': f'-vn -filter:a "volume={preset["volume"]}" -ac {preset["channels"]} -ar {preset["sample_rate"]} -b:a {preset["bitrate"]} -bufsize 64k'
    }

def get_ytdl_options(debug=False):
    """Obtiene las opciones de yt-dlp con configuración de depuración opcional"""
    options = YTDL_OPTIONS_OPTIMIZED.copy()
    
    if debug:
        options.update({
            'quiet': False,
            'no_warnings': False,
            'verbose': True
        })
    
    return options

def log_debug(message, debug_type='general'):
    """Función de logging para depuración"""
    if DEBUG_CONFIG.get('verbose_errors', False):
        print(f"[DEBUG-{debug_type.upper()}] {message}")

def format_duration(seconds):
    """Formatea la duración en formato mm:ss"""
    if not seconds:
        return "Desconocida"
    
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def validate_audio_url(url):
    """Valida que la URL de audio sea accesible"""
    if not url:
        return False
    
    # Verificaciones básicas
    if not url.startswith(('http://', 'https://')):
        return False
    
    # Verificar que no sea una URL de playlist
    if 'playlist' in url.lower():
        return False
    
    return True

# Configuración de reconexión automática
RECONNECT_CONFIG = {
    'max_attempts': 3,
    'delay_between_attempts': 2,
    'exponential_backoff': True
}

# Filtros de audio disponibles
AUDIO_FILTERS = {
    'bass_boost': 'bass=g=5',
    'treble_boost': 'treble=g=3',
    'normalize': 'loudnorm',
    'noise_reduction': 'afftdn=nf=-25',
    'echo': 'aecho=0.8:0.9:1000:0.3',
    'reverb': 'afreqshift=shift=0.1'
}

def get_filter_string(filters_list):
    """Genera string de filtros para FFmpeg"""
    if not filters_list:
        return 'volume=0.7'
    
    filter_strings = []
    for filter_name in filters_list:
        if filter_name in AUDIO_FILTERS:
            filter_strings.append(AUDIO_FILTERS[filter_name])
    
    if not filter_strings:
        return 'volume=0.7'
    
    return ','.join(filter_strings)