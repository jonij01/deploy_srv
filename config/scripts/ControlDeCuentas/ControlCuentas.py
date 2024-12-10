import os
import requests
import subprocess
from datetime import datetime, timedelta

def send_to_discord(message):
    webhook_url = 'https://discord.com/api/webhooks/1167130122478964766/_qphbYc2e6lINNRQL-neckOHO8WdDj84IWcLcQpTb1MepQmLQPfcov6RKFpCcyUIJuTo'
    
    data = {
        'content': message
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print("Notificación enviada exitosamente a Discord.")
    except requests.exceptions.RequestException as e:
        print("Error al enviar la notificación a Discord:", str(e))

def check_accounts():
    # Obtener la lista de cuentas de cPanel
    accounts = subprocess.check_output(['ls', '/var/cpanel/users']).decode('utf-8').split()

    # Leer el archivo con las cuentas creadas anteriormente
    created_accounts = []
    if os.path.isfile('created_accounts.txt'):
        with open('created_accounts.txt', 'r') as file:
            created_accounts = file.read().splitlines()

    # Leer el archivo con las cuentas eliminadas anteriormente
    deleted_accounts = []
    if os.path.isfile('deleted_accounts.txt'):
        with open('deleted_accounts.txt', 'r') as file:
            deleted_accounts = file.read().splitlines()

    # Encontrar cuentas creadas y eliminadas en el intervalo de tiempo actual
    new_created_accounts = [account for account in accounts if account not in created_accounts]
    new_deleted_accounts = [account for account in deleted_accounts if account not in accounts]

    # Guardar cuentas creadas y eliminadas en archivos
    with open('created_accounts.txt', 'w') as file:
        file.write('\n'.join(accounts))

    with open('deleted_accounts.txt', 'w') as file:
        file.write('\n'.join(accounts))

    return new_created_accounts, new_deleted_accounts

def main():
    created_accounts, deleted_accounts = check_accounts()

    # Crear y enviar notificaciones a Discord
    message = ""
    if created_accounts:
        created_message = f"**[Cloud-Aioros] Reporte de cuentas creadas hasta las 8:00 AM:**\n\n"
        for username in created_accounts:
            created_message += f":white_check_mark: Usuario creado: {username}\n"
        message += created_message + "\n"

    if deleted_accounts:
        deleted_message = f"**[Cloud-Aioros] Reporte de cuentas eliminadas hasta el día de hoy:**\n\n"
        for username in deleted_accounts:
            deleted_message += f":x: Usuario eliminado: {username}\n"
        message += deleted_message

    if message:
        send_to_discord(message)

if __name__ == "__main__":
    main()
