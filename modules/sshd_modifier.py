import os
import subprocess
from utils.discord_notifier import DiscordNotifier

class SSHDModifier:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def modify_sshd_config(self):
        """
        Reemplaza la configuración de SSHD eliminando el archivo existente y copiando uno nuevo.
        """
        try:
            print("Modificando la configuración de SSHD...")

            # Obtener la ruta absoluta del script
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Path al archivo de configuración de SSHD relativo al script
            new_config_path = os.path.join(script_dir, 'config', 'ssh', 'sshd_config')
            sshd_config_path = '/etc/ssh/sshd_config'

            # Verificar si el archivo de configuración existe
            if not os.path.isfile(new_config_path):
                raise FileNotFoundError(f"No se pudo encontrar el archivo de configuración en: {new_config_path}")

            # Eliminar el archivo existente
            subprocess.run(['rm', sshd_config_path], check=True)

            # Copiar el nuevo archivo de configuración
            subprocess.run(['cp', new_config_path, sshd_config_path], check=True)

            # Reiniciar el servicio SSHD para aplicar cambios
            subprocess.run(['systemctl', 'restart', 'sshd'], check=True)

            print("Configuración de SSHD modificada y aplicada correctamente.")
            self.notifier.notify_success("Configuración de SSHD modificada y aplicada correctamente.")
            return True
        except Exception as e:
            print(f"Error al modificar la configuración de SSHD: {str(e)}")
            self.notifier.notify_error(f"Error al modificar la configuración de SSHD: {str(e)}")
            return False