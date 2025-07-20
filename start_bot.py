#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicio mejorado para Nanali Music Bot
Incluye verificaciones de dependencias y configuración automática
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_banner():
    """Muestra el banner del bot"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🎵 NANALI MUSIC BOT v3.0 🎵                ║
    ║                                                              ║
    ║                    Bot de música premium con                 ║
    ║                    tema otaku y alta calidad                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_dependencies():
    """Verifica las dependencias de Python"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = {
        'discord': 'discord.py',
        'yt_dlp': 'yt-dlp',
        'dotenv': 'python-dotenv',
        'aiohttp': 'aiohttp',
        'psutil': 'psutil'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {pip_name} - Instalado")
        except ImportError:
            print(f"❌ {pip_name} - Faltante")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n⚠️  Faltan {len(missing_packages)} dependencias")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def check_ffmpeg():
    """Verifica si FFmpeg está instalado"""
    print("\n🎵 Verificando FFmpeg...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg no encontrado")
    print("💡 Instrucciones de instalación:")
    
    os_type = platform.system().lower()
    if os_type == 'windows':
        print("   • Descarga FFmpeg desde: https://ffmpeg.org/download.html")
        print("   • Extrae y añade al PATH del sistema")
    elif os_type == 'darwin':  # macOS
        print("   • brew install ffmpeg")
    else:  # Linux
        print("   • sudo apt install ffmpeg (Ubuntu/Debian)")
        print("   • sudo yum install ffmpeg (CentOS/RHEL)")
    
    return False

def check_env_file():
    """Verifica el archivo .env"""
    print("\n🔑 Verificando configuración...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        print("💡 Crea un archivo .env con tu token:")
        print("   DISCORD_TOKEN=tu_token_aqui")
        return False
    
    # Verificar que el token esté configurado
    with open('.env', 'r') as f:
        content = f.read()
        if 'DISCORD_TOKEN=' not in content or 'tu_token_aqui' in content:
            print("❌ Token de Discord no configurado")
            print("💡 Edita el archivo .env y añade tu token real")
            return False
    
    print("✅ Archivo .env configurado")
    return True

def check_nanali_image():
    """Verifica que la imagen de Nanali esté presente"""
    print("\n🖼️  Verificando recursos...")
    
    if not Path('nanali.jpg').exists():
        print("❌ Imagen nanali.jpg no encontrada")
        print("💡 Asegúrate de que nanali.jpg esté en el directorio del bot")
        return False
    
    print("✅ Imagen nanali.jpg encontrada")
    return True

def run_audio_test():
    """Ejecuta pruebas de audio"""
    print("\n🧪 Ejecutando pruebas de audio...")
    
    try:
        result = subprocess.run([sys.executable, 'test_audio.py'], 
                              capture_output=True, 
                              text=True, 
                              timeout=60)
        
        if result.returncode == 0 and "¡Todas las pruebas pasaron!" in result.stdout:
            print("✅ Pruebas de audio exitosas")
            return True
        else:
            print("❌ Falló alguna prueba de audio")
            print("📋 Salida de pruebas:")
            print(result.stdout)
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False

def start_bot():
    """Inicia el bot"""
    print("\n🚀 Iniciando Nanali Music Bot...")
    print("   Presiona Ctrl+C para detener el bot")
    print("   " + "="*50)
    
    try:
        # Ejecutar el bot
        subprocess.run([sys.executable, 'bot.py'])
    except KeyboardInterrupt:
        print("\n\n🛑 Bot detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al ejecutar el bot: {e}")

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones del sistema
    checks = [
        ("Versión de Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("FFmpeg", check_ffmpeg),
        ("Configuración", check_env_file),
        ("Recursos", check_nanali_image)
    ]
    
    failed_checks = []
    
    for check_name, check_func in checks:
        if not check_func():
            failed_checks.append(check_name)
    
    if failed_checks:
        print(f"\n❌ Falló {'n' if len(failed_checks) > 1 else ''} {len(failed_checks)} verificación{'es' if len(failed_checks) > 1 else ''}:")
        for check in failed_checks:
            print(f"   • {check}")
        print("\n🔧 Por favor resuelve los problemas antes de continuar")
        input("\nPresiona Enter para salir...")
        return
    
    # Ejecutar pruebas de audio (opcional)
    print("\n🎵 ¿Ejecutar pruebas de audio? (recomendado)")
    response = input("   Presiona Enter para sí, o 'n' para omitir: ").strip().lower()
    
    if response != 'n':
        if not run_audio_test():
            print("\n⚠️  Las pruebas de audio fallaron, pero puedes continuar")
            response = input("   ¿Continuar de todos modos? (y/n): ").strip().lower()
            if response != 'y':
                return
    
    print("\n✅ Todas las verificaciones completadas")
    time.sleep(2)
    
    # Iniciar el bot
    start_bot()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        input("Presiona Enter para salir...")