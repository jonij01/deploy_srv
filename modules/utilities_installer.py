import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class UtilitiesInstaller:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_htop(self):
        """
        Instala htop en el sistema.
        """
        try:
            subprocess.run(['yum', 'install', 'htop', '-y'], check=True)
            print("htop instalado correctamente.")
            self.notifier.notify_success("htop instalado correctamente.")
            return True
        except Exception as e:
            print(f"Error al instalar htop: {str(e)}")
            self.notifier.notify_error(f"Error al instalar htop: {str(e)}")
            return False

    def install_redis(self):
        """
        Instala Redis en el sistema.
        """
        try:
            subprocess.run(['yum', 'install', 'redis', '-y'], check=True)
            print("Redis instalado correctamente.")
            self.notifier.notify_success("Redis instalado correctamente.")
            return True
        except Exception as e:
            print(f"Error al instalar Redis: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Redis: {str(e)}")
            return False

    def move_jetbackup_workspace(self):
        """
        Mueve el workspace de JetBackup a la nueva ubicación.
        """
        try:
            subprocess.run(['mkdir', '-p', '/mnt/jetbackup5'], check=True)
            subprocess.run(['mv', '/usr/local/jetapps/usr/jetbackup5/workspace', '/mnt/jetbackup5/'], check=True)
            print("Workspace de JetBackup movido correctamente.")
            self.notifier.notify_success("Workspace de JetBackup movido correctamente.")
            return True
        except Exception as e:
            print(f"Error al mover el workspace de JetBackup: {str(e)}")
            self.notifier.notify_error(f"Error al mover el workspace de JetBackup: {str(e)}")
            return False

    def move_scripts_to_maintenance(self):
        """
        Mueve los scripts a la carpeta de mantenimiento en la raíz del sistema.
        """
        try:
            # Crear carpeta de mantenimiento si no existe
            if not os.path.exists('/mantenimiento'):
                os.makedirs('/mantenimiento')

            # Obtener la ruta absoluta del script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            scripts_path = os.path.join(script_dir, 'config', 'scripts')

            # Mover scripts
            for script in os.listdir(scripts_path):
                script_path = os.path.join(scripts_path, script)
                if os.path.isfile(script_path):
                    subprocess.run(['mv', script_path, '/mantenimiento/'], check=True)

            print("Scripts movidos a la carpeta de mantenimiento correctamente.")
            self.notifier.notify_success("Scripts movidos a la carpeta de mantenimiento correctamente.")
            return True
        except Exception as e:
            print(f"Error al mover los scripts: {str(e)}")
            self.notifier.notify_error(f"Error al mover los scripts: {str(e)}")
            return False
