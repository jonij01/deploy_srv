#!/bin/bash

# Configuración
WEBHOOK_URL="https://discord.com/api/webhooks/1250521194718040124/g4Vb6moViRFG7ixrbD2CSG322uzW8529AHJ95zKZ4i2WlSykzyM_1xzLwJ-Z35_vdOVI"
LOG_FILE="/var/log/secure"

# Función para enviar mensajes a Discord
send_to_discord() {
    local message=$1
    curl -H "Content-Type: application/json" -X POST -d "{\"content\": \"$message\"}" $WEBHOOK_URL
}

# Monitorear el archivo de logs de SSH
tail -Fn0 $LOG_FILE | while read line; do
    echo "Línea del log: $line"  # Mensaje de depuración

    # Verificar si la línea contiene una conexión SSH exitosa
    if echo $line | grep -q "Accepted"; then
        echo "Conexión SSH aceptada en el servidor DCH-IRONMAN [54.84.0.47]"  # Mensaje de depuración

        # Extraer información relevante
        ip=$(echo $line | awk '{print $11}')
        user=$(echo $line | awk '{print $9}')
        timestamp=$(date +"%Y-%m-%d %H:%M:%S")

        # Crear el mensaje
        message="🚀 **Conexión SSH detectada en el servidor DCH-IRONMAN [54.84.0.47]**\nUsuario: $user\nIP: $ip\nHora: $timestamp"

        # Enviar el mensaje a Discord
        send_to_discord "$message"
        echo "Mensaje enviado a Discord: $message"  # Mensaje de depuración
    fi
done
