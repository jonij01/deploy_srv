import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class UtilitiesInstaller:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

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
        Mueve el workspace de JetBackup a la nueva ubicación, forzando la copia de todos los archivos y carpetas.
        """
        try:
            # Crear el directorio de destino si no existe
            destination_dir = '/mnt/jetbackup5'
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            # Ruta de origen
            source_path = '/usr/local/jetapps/usr/jetbackup5/workspace'
            if not os.path.exists(source_path):
                print(f"Workspace no encontrado en la ruta predeterminada: {source_path}")
                source_path = input("Por favor, ingrese la ruta alternativa del workspace de JetBackup: ")
                if not os.path.exists(source_path):
                    raise FileNotFoundError(f"No se encontró el workspace en la ruta proporcionada: {source_path}")

            # Usar rsync para copiar todo el contenido
            print(f"Copiando contenido de {source_path} a {destination_dir}...")
            subprocess.run(['rsync', '-avh', '--remove-source-files', source_path + '/', destination_dir], check=True)

            # Eliminar directorios vacíos después de copiar
            subprocess.run(['find', source_path, '-type', 'd', '-empty', '-delete'], check=True)

            print("Workspace de JetBackup movido correctamente.")
            self.notifier.notify_success("Workspace de JetBackup movido correctamente.")
            return True
        except FileNotFoundError as fnf_error:
            print(f"Error al mover el workspace de JetBackup: {fnf_error}")
            self.notifier.notify_error(f"Error al mover el workspace de JetBackup: {fnf_error}")
            return False
        except subprocess.CalledProcessError as cpe_error:
            print(f"Error al ejecutar el comando rsync: {cpe_error}")
            self.notifier.notify_error(f"Error al ejecutar el comando rsync: {cpe_error}")
            return False
        except Exception as e:
            print(f"Error general al mover el workspace de JetBackup: {str(e)}")
            self.notifier.notify_error(f"Error general al mover el workspace de JetBackup: {str(e)}")
            return False

    def move_scripts_to_maintenance(self):
        """
        Mueve todo el contenido de la carpeta de scripts a la carpeta de mantenimiento, sin importar si son archivos, carpetas u otros.
        """
        try:
            # Ruta de destino
            maintenance_dir = '/mantenimiento'
            if not os.path.exists(maintenance_dir):
                os.makedirs(maintenance_dir)
                print(f"Directorio de mantenimiento creado: {maintenance_dir}")

            # Ruta de los scripts
            scripts_path = '/deploy_cPanelTools/config/scripts'
            if not os.path.exists(scripts_path):
                print(f"No se encontró la carpeta de scripts en la ruta predeterminada: {scripts_path}")
                scripts_path = input("Por favor, ingrese la ruta alternativa de la carpeta de scripts: ")
                if not os.path.exists(scripts_path):
                    raise FileNotFoundError(f"No se encontró la carpeta de scripts en la ruta proporcionada: {scripts_path}")

            # Verificar si la carpeta tiene contenido
            if not os.listdir(scripts_path):
                print(f"La carpeta de scripts está vacía: {scripts_path}")
                self.notifier.notify_error(f"La carpeta de scripts está vacía: {scripts_path}")
                return False

            # Mover todo el contenido del directorio
            print(f"Moviendo todo el contenido de {scripts_path} a {maintenance_dir}...")
            for item in os.listdir(scripts_path):
                source_item = os.path.join(scripts_path, item)
                subprocess.run(['mv', '-f', source_item, maintenance_dir], check=True)

            print("Todo el contenido se ha movido correctamente a la carpeta de mantenimiento.")
            self.notifier.notify_success("Todo el contenido se ha movido correctamente a la carpeta de mantenimiento.")
            return True
        except FileNotFoundError as fnf_error:
            print(f"Error al mover los scripts: {fnf_error}")
            self.notifier.notify_error(f"Error al mover los scripts: {fnf_error}")
            return False
        except subprocess.CalledProcessError as cpe_error:
            print(f"Error al ejecutar el comando mv: {cpe_error}")
            self.notifier.notify_error(f"Error al ejecutar el comando mv: {cpe_error}")
            return False
        except Exception as e:
            print(f"Error general al mover los scripts: {str(e)}")
            self.notifier.notify_error(f"Error general al mover los scripts: {str(e)}")
            return False