import subprocess
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account

# La ID de tu hoja de cálculo y el rango a actualizar
SPREADSHEET_ID = '1eDjSFGq6gKBrYSUMZ9wODDS-SEKt7urNpyTQ7ZLC-Jc'
RANGE_NAME = 'Licenciamientos 11/23!C20'

# Credenciales para la API de Google Sheets
SERVICE_ACCOUNT_FILE = '/mantenimiento/SyncAccounts/sync-411316-b00a12b1b27e.json'

# Credenciales para la API de WHM/cPanel
CPANEL_URL = "https://aioros.mi.com.co:2087"
API_TOKEN = "GXL7SXL63TK8DJHRIK6876ICMY024IIL"

def update_sheet(num_accounts):
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE)

    service = build('sheets', 'v4', credentials=creds)

    # Llamada a la API de Sheets para actualizar la hoja
    body = {
        'values': [[num_accounts]]
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
    print(f"{result.get('updatedCells')} celdas actualizadas.")

def get_cpanel_account_count():
    # Utilizar la API de WHM/cPanel para obtener el número de cuentas
    headers = {
        'Authorization': f'whm root:{API_TOKEN}'
    }
    try:
        response = requests.get(f"{CPANEL_URL}/json-api/listaccts", headers=headers, verify=True)
        if response.status_code == 200:
            accounts_data = response.json()
            return len(accounts_data.get("acct", []))
        else:
            print(f"Error al obtener datos de cPanel: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error al conectarse con la API de cPanel: {e}")
        return None

if __name__ == '__main__':
    num_accounts = get_cpanel_account_count()
    if num_accounts is not None:
        update_sheet(num_accounts)
