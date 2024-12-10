#!/bin/bash

# Configuración
webhook_url="https://discord.com/api/webhooks/1172191412981338142/VWhjZ7Ky3O4f8PU7Otm43kkv7jFpX2W-Ci9zrvTws4S-Yw1xVZlrLn0eG3_vPuRrWsIm"
usernames_file="p.txt"

# Función para enviar mensajes a Discord
send_to_discord() {
  local message="$1"
  curl -s -H "Content-Type: application/json" -X POST -d "{\"content\": \"$message\"}" $webhook_url
}

# Leer la lista de usuarios a eliminar del archivo
mapfile -t usernames_to_remove < "$usernames_file"

# Variables para almacenar los resultados
cpanel_accounts_removed=0
cpanel_accounts_not_found=0
not_found_cpanel_accounts=""

# Eliminar cuentas de cPanel y guardar los resultados
for username in "${usernames_to_remove[@]}"; do
    echo "Eliminando cuenta de cPanel para el usuario: ${username}"
    output=$( /usr/local/cpanel/scripts/removeacct "$username" -f 2>&1 )

    if [ $? -eq 0 ]; then
        cpanel_accounts_removed=$((cpanel_accounts_removed + 1))
    else
        cpanel_accounts_not_found=$((cpanel_accounts_not_found + 1))
        not_found_cpanel_accounts+="${username}, "
        echo "Error al eliminar la cuenta de cPanel para el usuario ${username}: $output"
    fi
done

# Crear un mensaje resumido y enviarlo a Discord
summary_message="Se eliminaron de Aioros ${cpanel_accounts_removed} cuentas de cPanel. No se encontraron ${cpanel_accounts_not_found} cuentas de cPanel."
if [ $cpanel_accounts_not_found -gt 0 ]; then
  summary_message+=" Cuentas de cPanel no encontradas: ${not_found_cpanel_accounts::-2}."
fi
send_to_discord "$summary_message"
