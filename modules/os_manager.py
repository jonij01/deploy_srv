import subprocess
from typing import Optional
from utils.discord_notifier import DiscordNotifier

class OSManager:
    def __init__(self, notifier: Optional[DiscordNotifier] = None):
        self.notifier = notifier
        
    def check_os(self) -> str:
        """
        Verifica la versión del sistema operativo.
        """
        try:
            print("Verificando el sistema operativo...")
            result = subprocess.run(["cat", "/etc/os-release"], 
                                 capture_output=True, 
                                 text=True, 
                                 check=True)
            print(result.stdout)
            self.notifier.notify_success("Verificación del sistema operativo completada.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al verificar el sistema operativo: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return None

    def update_system(self):
        """
        Actualiza el sistema operativo usando yum.
        """
        try:
            print("Actualizando el sistema operativo...")
            subprocess.run(["yum", "update", "-y"], check=True)
            print("Sistema operativo actualizado correctamente.")
            self.notifier.notify_success("Sistema operativo actualizado correctamente.")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al actualizar el sistema operativo: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
