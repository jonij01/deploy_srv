#!/bin/bash

# Ruta al directorio /tmp
tmp_dir="/tmp"

# Archivo que se debe excluir
exclude_file="mysql.sock"

# Obtener la hora actual
current_time=$(date +"%Y-%m-%d %H:%M:%S")

# Eliminar archivos en /tmp excepto $exclude_file
find "$tmp_dir" -type f ! -name "$exclude_file" -delete

# Verificar si la eliminación fue exitosa
if [ $? -eq 0 ]; then
    # Enviar notificación a Discord
    discord_webhook_url="https://discord.com/api/webhooks/1192598193452613712/y4nc87HFJt5kj9NE2ZKPsXv8GqpmMdpF9YB9M6JRce1czNlaeyjtQJ7_xYN_foNLsUyv"
    message="Se ha eliminado el contenido de /tmp (excepto $exclude_file) en el servidor Aioros, a las $current_time de manera exitosa."
    
    curl -H "Content-Type: application/json" -X POST -d "{\"content\":\"$message\"}" "$discord_webhook_url"
else
    # Enviar notificación a Discord en caso de error
    discord_webhook_url="https://discord.com/api/webhooks/your_webhook_url"
    message="Hubo un error al intentar eliminar el contenido de /tmp (excepto $exclude_file) a las $current_time."
    
    curl -H "Content-Type: application/json" -X POST -d "{\"content\":\"$message\"}" "$discord_webhook_url"
fi
