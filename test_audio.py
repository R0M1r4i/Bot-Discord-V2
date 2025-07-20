#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la configuración de audio del bot
"""

import yt_dlp
import discord
import asyncio
from discord.ext import commands

# Configuración de prueba simplificada
YTDL_OPTIONS_TEST = {
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
    'youtube_include_dash_manifest': False
}

FFMPEG_OPTIONS_TEST = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
    'options': '-vn -filter:a "volume=0.5"'
}

def test_ytdl_extraction():
    """Prueba la extracción de información con yt-dlp"""
    print("🔍 Probando extracción de yt-dlp...")
    
    # URL de prueba (video corto de YouTube)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - video conocido
    
    try:
        ydl = yt_dlp.YoutubeDL(YTDL_OPTIONS_TEST)
        data = ydl.extract_info(test_url, download=False)
        
        if 'entries' in data:
            data = data['entries'][0]
        
        audio_url = data.get('url')
        title = data.get('title', 'Título desconocido')
        duration = data.get('duration')
        uploader = data.get('uploader', 'Canal desconocido')
        
        print(f"✅ Extracción exitosa:")
        print(f"   Título: {title}")
        print(f"   Canal: {uploader}")
        print(f"   Duración: {duration} segundos")
        print(f"   URL de audio: {audio_url[:100] if audio_url else 'No disponible'}...")
        
        return audio_url is not None
        
    except Exception as e:
        print(f"❌ Error en extracción: {e}")
        return False

def test_ffmpeg_compatibility():
    """Prueba la compatibilidad de FFmpeg"""
    print("\n🔧 Probando compatibilidad de FFmpeg...")
    
    try:
        # Intentar crear un objeto FFmpegPCMAudio con una URL de prueba
        test_url = "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"  # URL de audio simple
        
        # Solo verificar que se puede crear el objeto (no reproducir)
        source = discord.FFmpegPCMAudio(test_url, **FFMPEG_OPTIONS_TEST)
        print("✅ FFmpeg configurado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en FFmpeg: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🎵 Iniciando pruebas de configuración de audio...\n")
    
    # Prueba 1: yt-dlp
    ytdl_ok = test_ytdl_extraction()
    
    # Prueba 2: FFmpeg
    ffmpeg_ok = test_ffmpeg_compatibility()
    
    # Resumen
    print("\n📊 Resumen de pruebas:")
    print(f"   yt-dlp: {'✅ OK' if ytdl_ok else '❌ FALLO'}")
    print(f"   FFmpeg: {'✅ OK' if ffmpeg_ok else '❌ FALLO'}")
    
    if ytdl_ok and ffmpeg_ok:
        print("\n🎉 ¡Todas las pruebas pasaron! El bot debería funcionar correctamente.")
    else:
        print("\n⚠️  Hay problemas de configuración que necesitan ser resueltos.")
        if not ytdl_ok:
            print("   - Verifica tu conexión a internet")
            print("   - Asegúrate de que yt-dlp esté actualizado: pip install --upgrade yt-dlp")
        if not ffmpeg_ok:
            print("   - Verifica que FFmpeg esté instalado y en el PATH")
            print("   - En Windows: descarga FFmpeg desde https://ffmpeg.org/download.html")

if __name__ == "__main__":
    main()