import subprocess
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Carga las credenciales y autoriza el cliente
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('healthy-dragon-414300-0a8cb78c518b.json', scope)
gc = gspread.authorize(credentials)

# Cambiar solo la hoja del sheets en nombre, ejemplo: "[F-003] POOL-HOSTING"
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1aMQeDqUIOfP6anW9601aN8C0sIW1VN7vj9phpgxWUaQ')
worksheet = sh.worksheet("[F-003] POOL-HOSTING")

# Contabilizar los cores actuales asignados en la vm
cpus = subprocess.run(['nproc'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

# Traer la info de la raiz y el home, después convierte en gb para añadir al sheets
uso_raiz_output = subprocess.run(['df', '/', '--output=pcent,size'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[1].split()
uso_raiz = f"{uso_raiz_output[0]} / {int(uso_raiz_output[1])//1024**2}GB"

uso_home_output = subprocess.run(['df', '/home', '--output=pcent,size'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[1].split()
uso_home = f"{uso_home_output[0]} / {int(uso_home_output[1])//1024**2}GB"

# Calcular la memora ram y convertirla en gb
ram_output = subprocess.run(['free', '-m'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[1].split()
ram = f"{int(ram_output[1])//1024}GB"

# Actualiza la hoja de cálculo con las métricas recogidas
worksheet.update('I7', cpus)
worksheet.update('J7', uso_raiz)
worksheet.update('K7', uso_home)
worksheet.update('L7', ram)