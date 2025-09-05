# 🌸 Music Bot v3.0

Bienvenido al bot de música! 🎵✨

## 🆕 ¡Nuevas Funcionalidades v3.0!

### 🎌 Comandos Temáticos 
- **🎵 Openings** - Reproduce openings épicos aleatoriamente
- **🎶 Endings** - Endings que te harán llorar
- **🎼 Música Vocaloid** - Hatsune Miku, Rin, Len y más
- **🌸 J-Pop** - Música adorable y pegajosa
- **⚡ OSTs Épicos** - Música de peleas y momentos intensos
- **🎭 Búsqueda por Personaje** - Encuentra música de tu personaje favorito

### 🔊 Audio Premium
- **Calidad 320kbps** - Máxima calidad de audio
- **Codec Opus** - Audio cristalino y eficiente
- **Volumen Boost** - Hasta 150% con modo boost
- **Ecualizador Integrado** - Bass boost de 0 a 4 niveles
- **Buffer Optimizado** - 512kb para reproducción fluida

### 🔍 Búsqueda Avanzada
- **Búsqueda Interactiva** - Selecciona entre 5 resultados
- **Reacciones Intuitivas** - Usa emojis para elegir
- **Información Detallada** - Duración, canal y más
- **Timeout Inteligente** - 30 segundos para decidir

## ✨ Características Principales

### 🎶 Sistema Musical Avanzado
- **Cola sin distorsión** - Procesamiento asíncrono optimizado
- **Modo repetición** - Song/Queue/Off con control total
- **Auto-desconexión inteligente** - 5 minutos de inactividad
- **Gestión de errores robusta** - Recuperación automática
- **Soporte multiplataforma** - YouTube y más



## 🎮 Comandos Completos

### 🎵 Comandos Básicos
```
!play <url> o !p <url>     - Reproduce música de alta calidad
!search <término>          - Búsqueda interactiva avanzada
!skip                      - Salta la canción actual
!stop                      - Detiene y limpia la cola
!leave                     - Desconecta del canal de voz
```

### 📋 Gestión de Cola
```
!queue o !q               - Muestra la cola de reproducción
!nowplaying o !np         - Información de la canción actual
!shuffle                  - Mezcla la cola aleatoriamente
!clear                    - Limpia toda la cola
!remove <posición>        - Elimina canción específica
!loop <song/queue/off>    - Modo repetición avanzado
```

### 🌸 Comandos Especiales
```
!weeb o !anime o !otaku   - Menú completo de comandos otaku
!anime_op                 - Opening de anime aleatorio
!anime_ed                 - Ending emotivo de anime
!vocaloid                 - Música de Vocaloid
!kawaii                   - J-Pop y música kawaii
!epic_anime               - OSTs épicos de anime
!character <nombre>       - Música del personaje
```

### ⚙️ Comandos Avanzados
```
!volume <0-150> o !v      - Control de volumen con boost
!bass_boost <0-4> o !eq   - Ecualizador y efectos
!stats                    - Estadísticas completas
!nanali                   - Información del bot
!help_music               - Ayuda completa
```

## 🚀 Instalación y Configuración

### Requisitos del Sistema
- **Python 3.8+** - Versión recomendada: 3.9 o superior
- **FFmpeg** - Para procesamiento de audio
- **Conexión estable** - Para streaming de calidad
- **4GB RAM mínimo** - Para funcionamiento óptimo

### 🎯 Instalación Automática (Recomendada)

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/nanali-music-bot.git
cd nanali-music-bot
```

2. **Ejecutar instalación automática:**
```bash
python setup.py
```
Este script:
- Verifica la versión de Python
- Instala todas las dependencias
- Configura FFmpeg (con instrucciones)
- Crea archivos de configuración
- Genera scripts de inicio

3. **Configurar el token:**
- Editar el archivo `.env` creado
- Reemplazar `tu_token_aqui` con tu token real

4. **Iniciar el bot:**
```bash
python start_bot.py
```
O usar los scripts generados:
- Windows: `start.bat`
- Linux/macOS: `./start.sh`

### 🔧 Instalación Manual

1. **Instala dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configura el token:**
```bash
cp .env.example .env
# Editar .env con tu token
```

3. **Verifica configuración:**
```bash
python test_audio.py
```

4. **Ejecuta el bot:**
```bash
python bot.py
```

### Instalación de FFmpeg

#### 🪟 Windows
1. Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extrae y añade `bin/` al PATH del sistema
3. Reinicia la terminal
4. Verifica: `ffmpeg -version`

#### 🍎 macOS
```bash
# Con Homebrew
brew install ffmpeg

# Con MacPorts
sudo port install ffmpeg
```

#### 🐧 Linux
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

### Configuración del Bot de Discord

1. **Crea una aplicación** en [Discord Developer Portal](https://discord.com/developers/applications)
2. **Crea un bot** y copia el token
3. **Configura permisos:**
   - ✅ Conectar a canales de voz
   - ✅ Hablar en canales de voz
   - ✅ Enviar mensajes
   - ✅ Usar comandos de aplicación
   - ✅ Adjuntar archivos
   - ✅ Añadir reacciones
   - ✅ Leer historial de mensajes


### ❌ Problemas Comunes

**🔇 Sin audio:**
```bash
# Verifica FFmpeg
ffmpeg -version

# Verifica permisos del bot
# Reinicia el bot
python bot.py
```

**🔑 Error de token:**
```bash
# Verifica el archivo .env
cat .env

# Regenera el token en Discord Developer Portal
```

**🌐 Problemas de conexión:**
```bash
# Verifica conectividad
ping discord.com

# Verifica puertos (443, 80)
telnet discord.com 443
```

**🎵 Calidad de audio baja:**
- Usa `!bass_boost 2` para mejorar graves
- Ajusta volumen con `!volume 120` (modo boost)
- Verifica la calidad del video original

**Para problemas específicos, consultar:** [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)



<div align="center">


[![Discord](https://img.shields.io/badge/Discord-Bot-7289da?style=for-the-badge&logo=discord)](https://discord.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0-ff69b4?style=for-the-badge)](README.md)

</div>
