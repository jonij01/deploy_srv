import subprocess
from utils.discord_notifier import DiscordNotifier

class JetBackupManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_jetbackup(self):
        """
        Instala y configura JetBackup con la versión estable.
        """
        try:
            print("Instalando JetBackup...")
            
            # Instalar el repositorio JetApps
            install_cmd = "bash <(curl -LSs http://repo.jetlicense.com/static/install)"
            subprocess.run(install_cmd, shell=True, check=True)
            
            # Instalar JetBackup 5 versión estable para cPanel
            subprocess.run(["jetapps", "--install", "jetbackup5-cpanel", "stable"], check=True)
            
            # Configurar actualizaciones automáticas
            subprocess.run(["jetapps", "-p", "jetbackup5-cpanel", "yes"], check=True)
            
            # Verificar la instalación
            subprocess.run(["jetapps", "-v", "jetbackup5-cpanel"], check=True)
            
            print("JetBackup instalado y configurado correctamente.")
            self.notifier.notify_success("JetBackup instalado y configurado correctamente.")
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al instalar JetBackup: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado durante la instalación de JetBackup: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise Exception(error_msg)

    def verify_installation(self):
        """
        Verifica el estado de la instalación de JetBackup.
        """
        try:
            result = subprocess.run(["jetapps", "-v", "jetbackup5-cpanel"], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            print(f"Estado de JetBackup: {result.stdout}")
            return True
        except subprocess.CalledProcessError:
            print("No se pudo verificar la instalación de JetBackup")
            return False