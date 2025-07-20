# 🔧 Guía de Solución de Problemas - Nanali Music Bot

## 🎵 Problemas de Reproducción de Audio

### Error: FFmpeg termina con código 4294967274

**Síntomas:**
- El bot se conecta al canal de voz
- Aparece el mensaje "Reproduciendo ahora" pero no se escucha audio
- En la consola aparece: `ffmpeg process ... terminated with return code of 4294967274`

**Causas comunes:**
1. Configuración incorrecta de FFmpeg
2. URL de audio inválida o expirada
3. Problemas de conectividad
4. Configuración de codec incompatible

**Soluciones aplicadas en v3.0:**

#### ✅ 1. Configuración FFmpeg Optimizada
```python
# Antes (problemático)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin -ss 0',
    'options': '-vn -b:a 320k -bufsize 512k -ac 2 -ar 48000 -acodec libopus -compression_level 10'
}

# Ahora (corregido)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin -loglevel error',
    'options': '-vn -filter:a "volume=0.7" -ac 2 -ar 48000 -b:a 128k -bufsize 64k'
}
```

#### ✅ 2. Configuración yt-dlp Simplificada
```python
# Antes (complejo)
YTDL_OPTIONS = {
    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '320',
    }],
    # ... muchas opciones más
}

# Ahora (simplificado y funcional)
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    # ... opciones esenciales únicamente
}
```

#### ✅ 3. Validación de URLs de Audio
- Verificación de URLs antes de enviar a FFmpeg
- Timeout en extracción de información
- Manejo robusto de errores

#### ✅ 4. Logging Mejorado
- Mensajes de debug detallados
- Seguimiento de errores específicos
- Información de tiempo de extracción

### 🧪 Verificar la Solución

1. **Ejecutar pruebas automáticas:**
   ```bash
   python test_audio.py
   ```

2. **Usar el script de inicio:**
   ```bash
   python start_bot.py
   ```

3. **Verificar manualmente:**
   - Probar con un video conocido de YouTube
   - Verificar que FFmpeg esté en el PATH
   - Comprobar la conexión a internet

---

## 🚨 Otros Problemas Comunes

### Bot no se conecta a Discord

**Error:** `discord.errors.LoginFailure`

**Solución:**
1. Verificar que el token en `.env` sea correcto
2. Asegurarse de que el bot tenga permisos en el servidor
3. Verificar que el token no haya expirado

### Bot no puede unirse al canal de voz

**Error:** `discord.errors.ClientException`

**Solución:**
1. Verificar permisos del bot:
   - `Connect` (Conectar)
   - `Speak` (Hablar)
   - `Use Voice Activity` (Usar actividad de voz)
2. Verificar que el canal no esté lleno
3. Comprobar que el bot no esté ya conectado a otro canal

### Comandos no responden

**Posibles causas:**
1. Prefijo incorrecto (debe ser `!`)
2. Bot sin permisos de lectura de mensajes
3. Bot sin permisos de envío de mensajes
4. Intents no configurados correctamente

**Solución:**
```python
# Verificar intents en bot.py
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
```

### Error de dependencias

**Error:** `ModuleNotFoundError`

**Solución:**
```bash
pip install -r requirements.txt
```

### FFmpeg no encontrado

**Windows:**
1. Descargar FFmpeg desde https://ffmpeg.org/download.html
2. Extraer a una carpeta (ej: `C:\ffmpeg`)
3. Añadir `C:\ffmpeg\bin` al PATH del sistema
4. Reiniciar la terminal/IDE

**Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

---

## 📊 Herramientas de Diagnóstico

### 1. Script de Pruebas
```bash
python test_audio.py
```
Verifica:
- Extracción de yt-dlp
- Compatibilidad de FFmpeg
- Configuración básica

### 2. Script de Inicio
```bash
python start_bot.py
```
Verifica:
- Versión de Python
- Dependencias instaladas
- FFmpeg disponible
- Archivo .env configurado
- Recursos necesarios

### 3. Modo Debug
Para activar logging detallado, edita `audio_config.py`:
```python
DEBUG_CONFIG = {
    'verbose_errors': True,  # Cambiar a True
    'log_audio_urls': True,
    'log_ffmpeg_errors': True
}
```

---

## 🆘 Obtener Ayuda

Si los problemas persisten:

1. **Revisar logs:** Buscar mensajes de error específicos
2. **Verificar versiones:** Asegurarse de usar versiones compatibles
3. **Probar con video simple:** Usar un video corto y conocido de YouTube
4. **Reiniciar completamente:** Cerrar bot, terminal, y volver a iniciar

### Información útil para reportar problemas:
- Versión de Python
- Sistema operativo
- Versión de FFmpeg
- URL que causa problemas
- Logs completos del error
- Resultado de `python test_audio.py`

---

## 📈 Optimizaciones de Rendimiento

### Para servidores grandes:
1. Aumentar `max_queue_size` en `audio_config.py`
2. Ajustar `extraction_timeout` según la conexión
3. Usar calidad 'low' o 'medium' en lugar de 'high'

### Para conexiones lentas:
1. Reducir `buffersize` en yt-dlp options
2. Usar formato de menor calidad
3. Aumentar timeouts

### Para uso intensivo:
1. Implementar cache de URLs extraídas
2. Usar pool de conexiones
3. Monitorear uso de memoria con `psutil`