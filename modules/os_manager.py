import os
import subprocess
from utils.discord_notifier import DiscordNotifier

class OSManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def check_os(self):
        """
        Verifica la versión del sistema operativo.
        """
        try:
            print("Verificando el sistema operativo...")
            result = subprocess.run(["cat", "/etc/os-release"], capture_output=True, text=True, check=True)
            print(result.stdout)
            self.notifier.notify_success("Verificación del sistema operativo completada.")
        except subprocess.CalledProcessError as e:
            print(f"Error al verificar el sistema operativo: {str(e)}")
            self.notifier.notify_error(f"Error al verificar el sistema operativo: {str(e)}")

    def configure_easyapache(self):
        """
        Carga el perfil de EasyApache4 desde el archivo de configuración.
        """
        try:
            print("Configurando EasyApache4...")
            profile_path = "config/easyapache/EasyGeneral.json"
            subprocess.run(["/usr/local/cpanel/scripts/easyapache", "--import", profile_path], check=True)
            print("EasyApache4 configurado correctamente.")
            self.notifier.notify_success("EasyApache4 configurado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al configurar EasyApache4: {str(e)}")
            self.notifier.notify_error(f"Error al configurar EasyApache4: {str(e)}")
