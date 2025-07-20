#!/usr/bin/env python3
# 🌸 Nanali Music Bot v3.0 - Instalador Automático
# Script de instalación y configuración automatizada

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path

class Colors:
    """Colores para terminal"""
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Muestra el banner de Nanali"""
    banner = f"""
{Colors.PINK}{Colors.BOLD}
    ███╗   ██╗ █████╗ ███╗   ██╗ █████╗ ██╗     ██╗
    ████╗  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██║
    ██╔██╗ ██║███████║██╔██╗ ██║███████║██║     ██║
    ██║╚██╗██║██╔══██║██║╚██╗██║██╔══██║██║     ██║
    ██║ ╚████║██║  ██║██║ ╚████║██║  ██║███████╗██║
    ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝
    
    🎵 MUSIC BOT v3.0 - PREMIUM OTAKU EDITION 🌸
{Colors.END}
    """
    print(banner)
    print(f"{Colors.BLUE}¡Konnichiwa! Bienvenido al instalador de Nanali Music Bot{Colors.END}")
    print(f"{Colors.YELLOW}Este script configurará automáticamente todo lo necesario{Colors.END}\n")

def check_python_version():
    """Verifica la versión de Python"""
    print(f"{Colors.BLUE}🐍 Verificando versión de Python...{Colors.END}")
    
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}❌ Error: Se requiere Python 3.8 o superior{Colors.END}")
        print(f"{Colors.YELLOW}Versión actual: {sys.version}{Colors.END}")
        print(f"{Colors.BLUE}Por favor, actualiza Python desde: https://python.org{Colors.END}")
        return False
    
    print(f"{Colors.GREEN}✅ Python {sys.version.split()[0]} detectado{Colors.END}")
    return True

def install_requirements():
    """Instala las dependencias de Python"""
    print(f"\n{Colors.BLUE}📦 Instalando dependencias de Python...{Colors.END}")
    
    requirements = [
        'discord.py[voice]>=2.3.0',
        'yt-dlp>=2023.7.6',
        'PyNaCl>=1.5.0',
        'python-dotenv>=1.0.0',
        'aiohttp>=3.8.0',
        'psutil>=5.9.0'
    ]
    
    for req in requirements:
        try:
            print(f"{Colors.YELLOW}Instalando {req}...{Colors.END}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req, '--upgrade'])
            print(f"{Colors.GREEN}✅ {req} instalado correctamente{Colors.END}")
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}❌ Error instalando {req}{Colors.END}")
            return False
    
    return True

def check_ffmpeg():
    """Verifica si FFmpeg está instalado"""
    print(f"\n{Colors.BLUE}🎵 Verificando FFmpeg...{Colors.END}")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ FFmpeg encontrado{Colors.END}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print(f"{Colors.YELLOW}⚠️ FFmpeg no encontrado{Colors.END}")
    return False

def install_ffmpeg_windows():
    """Instala FFmpeg en Windows"""
    print(f"{Colors.BLUE}📥 Descargando FFmpeg para Windows...{Colors.END}")
    
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    ffmpeg_zip = "ffmpeg.zip"
    ffmpeg_dir = "ffmpeg"
    
    try:
        # Descargar FFmpeg
        print(f"{Colors.YELLOW}Descargando desde GitHub...{Colors.END}")
        urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
        
        # Extraer
        print(f"{Colors.YELLOW}Extrayendo archivos...{Colors.END}")
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            zip_ref.extractall()
        
        # Mover archivos
        extracted_folder = None
        for item in os.listdir('.'):
            if item.startswith('ffmpeg-') and os.path.isdir(item):
                extracted_folder = item
                break
        
        if extracted_folder:
            if os.path.exists(ffmpeg_dir):
                shutil.rmtree(ffmpeg_dir)
            shutil.move(extracted_folder, ffmpeg_dir)
            
            # Agregar al PATH del sistema
            ffmpeg_bin = os.path.abspath(os.path.join(ffmpeg_dir, 'bin'))
            current_path = os.environ.get('PATH', '')
            if ffmpeg_bin not in current_path:
                os.environ['PATH'] = ffmpeg_bin + os.pathsep + current_path
            
            print(f"{Colors.GREEN}✅ FFmpeg instalado en: {ffmpeg_bin}{Colors.END}")
            print(f"{Colors.YELLOW}⚠️ Reinicia la terminal para que los cambios surtan efecto{Colors.END}")
        
        # Limpiar archivos temporales
        if os.path.exists(ffmpeg_zip):
            os.remove(ffmpeg_zip)
        
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error instalando FFmpeg: {e}{Colors.END}")
        return False

def setup_ffmpeg():
    """Configura FFmpeg según el sistema operativo"""
    if check_ffmpeg():
        return True
    
    system = platform.system().lower()
    
    if system == 'windows':
        print(f"{Colors.BLUE}🪟 Sistema Windows detectado{Colors.END}")
        response = input(f"{Colors.YELLOW}¿Deseas instalar FFmpeg automáticamente? (s/n): {Colors.END}")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            return install_ffmpeg_windows()
        else:
            print(f"{Colors.BLUE}Instrucciones manuales para Windows:{Colors.END}")
            print(f"{Colors.YELLOW}1. Descarga FFmpeg desde: https://ffmpeg.org/download.html{Colors.END}")
            print(f"{Colors.YELLOW}2. Extrae el archivo y añade la carpeta 'bin' al PATH{Colors.END}")
            print(f"{Colors.YELLOW}3. Reinicia la terminal{Colors.END}")
    
    elif system == 'darwin':  # macOS
        print(f"{Colors.BLUE}🍎 Sistema macOS detectado{Colors.END}")
        print(f"{Colors.YELLOW}Instala FFmpeg con Homebrew:{Colors.END}")
        print(f"{Colors.GREEN}brew install ffmpeg{Colors.END}")
    
    elif system == 'linux':
        print(f"{Colors.BLUE}🐧 Sistema Linux detectado{Colors.END}")
        print(f"{Colors.YELLOW}Instala FFmpeg con tu gestor de paquetes:{Colors.END}")
        print(f"{Colors.GREEN}Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg{Colors.END}")
        print(f"{Colors.GREEN}CentOS/RHEL: sudo yum install ffmpeg{Colors.END}")
        print(f"{Colors.GREEN}Arch Linux: sudo pacman -S ffmpeg{Colors.END}")
    
    return False

def create_env_file():
    """Crea el archivo .env con configuración"""
    print(f"\n{Colors.BLUE}⚙️ Configurando archivo de entorno...{Colors.END}")
    
    env_content = '''# 🌸 Nanali Music Bot v3.0 - Configuración
# Archivo de variables de entorno

# Token del bot de Discord (REQUERIDO)
# Obtén tu token desde: https://discord.com/developers/applications
DISCORD_TOKEN=tu_token_aqui

# Configuración opcional
COMMAND_PREFIX=!
MAX_QUEUE_SIZE=100
AUTO_DISCONNECT_DELAY=300
DEFAULT_VOLUME=50
MAX_VOLUME=150

# Configuración de desarrollo (opcional)
DEBUG_MODE=False
LOG_LEVEL=INFO
'''
    
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"{Colors.GREEN}✅ Archivo .env creado{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️ Archivo .env ya existe{Colors.END}")
    
    print(f"{Colors.BLUE}📝 Recuerda editar .env y agregar tu token de Discord{Colors.END}")
    return True

def create_gitignore():
    """Crea el archivo .gitignore"""
    gitignore_content = '''# 🌸 Nanali Music Bot - Archivos a ignorar

# Archivos de configuración sensibles
.env
*.env
config.json
secrets.json

# Archivos de Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
PIPFILE.lock

# Archivos de audio temporales
*.mp3
*.mp4
*.webm
*.m4a
*.opus
*.wav
*.flac
*.aac

# Logs
*.log
logs/

# FFmpeg (si se instala localmente)
ffmpeg/

# Archivos del sistema
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Archivos de respaldo
*.bak
*.backup
*.tmp
'''
    
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print(f"{Colors.GREEN}✅ Archivo .gitignore creado{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠️ Archivo .gitignore ya existe{Colors.END}")
    
    return True

def create_start_script():
    """Crea script de inicio"""
    print(f"\n{Colors.BLUE}🚀 Creando script de inicio...{Colors.END}")
    
    if platform.system().lower() == 'windows':
        # Script para Windows
        start_content = '''@echo off
echo 🌸 Iniciando Nanali Music Bot v3.0...
echo.
python bot.py
pause
'''
        with open('start.bat', 'w', encoding='utf-8') as f:
            f.write(start_content)
        print(f"{Colors.GREEN}✅ Script start.bat creado{Colors.END}")
    else:
        # Script para Unix/Linux/macOS
        start_content = '''#!/bin/bash
echo "🌸 Iniciando Nanali Music Bot v3.0..."
echo
python3 bot.py
'''
        with open('start.sh', 'w', encoding='utf-8') as f:
            f.write(start_content)
        os.chmod('start.sh', 0o755)
        print(f"{Colors.GREEN}✅ Script start.sh creado{Colors.END}")
    
    return True

def show_final_instructions():
    """Muestra las instrucciones finales"""
    print(f"\n{Colors.PINK}{Colors.BOLD}🌸 ¡Instalación completada! 🌸{Colors.END}")
    print(f"{Colors.GREEN}Nanali Music Bot v3.0 está listo para usar{Colors.END}\n")
    
    print(f"{Colors.BLUE}{Colors.BOLD}📋 Pasos finales:{Colors.END}")
    print(f"{Colors.YELLOW}1. Edita el archivo .env y agrega tu token de Discord{Colors.END}")
    print(f"{Colors.YELLOW}2. Crea una aplicación en: https://discord.com/developers/applications{Colors.END}")
    print(f"{Colors.YELLOW}3. Invita el bot a tu servidor con los permisos necesarios{Colors.END}")
    
    if platform.system().lower() == 'windows':
        print(f"{Colors.YELLOW}4. Ejecuta start.bat para iniciar el bot{Colors.END}")
    else:
        print(f"{Colors.YELLOW}4. Ejecuta ./start.sh para iniciar el bot{Colors.END}")
    
    print(f"\n{Colors.BLUE}{Colors.BOLD}🎵 Comandos principales:{Colors.END}")
    print(f"{Colors.GREEN}!help_music    - Ayuda completa{Colors.END}")
    print(f"{Colors.GREEN}!play <url>    - Reproduce música{Colors.END}")
    print(f"{Colors.GREEN}!search <term> - Búsqueda interactiva{Colors.END}")
    print(f"{Colors.GREEN}!weeb          - Comandos otaku{Colors.END}")
    print(f"{Colors.GREEN}!nanali        - Información del bot{Colors.END}")
    
    print(f"\n{Colors.PINK}🌸 ¡Arigatou gozaimasu por elegir Nanali Music Bot! 🎵{Colors.END}")
    print(f"{Colors.BLUE}Para soporte: https://github.com/tu-usuario/nanali-music-bot{Colors.END}")

def main():
    """Función principal del instalador"""
    try:
        print_banner()
        
        # Verificar Python
        if not check_python_version():
            return False
        
        # Instalar dependencias
        if not install_requirements():
            print(f"{Colors.RED}❌ Error instalando dependencias{Colors.END}")
            return False
        
        # Configurar FFmpeg
        setup_ffmpeg()
        
        # Crear archivos de configuración
        create_env_file()
        create_gitignore()
        create_start_script()
        
        # Mostrar instrucciones finales
        show_final_instructions()
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Instalación cancelada por el usuario{Colors.END}")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error durante la instalación: {e}{Colors.END}")
        return False

if __name__ == '__main__':
    success = main()
    if not success:
        print(f"\n{Colors.RED}❌ La instalación no se completó correctamente{Colors.END}")
        print(f"{Colors.BLUE}Por favor, revisa los errores y vuelve a intentar{Colors.END}")
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}✅ ¡Instalación exitosa!{Colors.END}")
        sys.exit(0)