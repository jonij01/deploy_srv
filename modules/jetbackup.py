import subprocess
from utils.discord_notifier import DiscordNotifier

class JetBackupManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def check_jetbackup_installed(self):
        """
        Verifica si JetBackup ya está instalado
        """
        try:
            result = subprocess.run(
                ["jetapps", "-v", "jetbackup5-cpanel"],
                capture_output=True,
                text=True
            )
            # Si el comando se ejecuta exitosamente y muestra la versión, está instalado
            return result.returncode == 0
        except:
            return False

    def install_jetbackup(self):
        """
        Instala y configura JetBackup con la versión estable.
        Si ya está instalado, omite la instalación y continúa.
        """
        try:
            print("Verificando instalación de JetBackup...")
            
            # Verificar si ya está instalado
            if self.check_jetbackup_installed():
                print("JetBackup ya está instalado. Continuando con el proceso...")
                self.notifier.notify_success("JetBackup ya está instalado. Continuando...")
                return True

            print("Instalando JetBackup...")
            
            # Instalar el repositorio JetApps
            install_cmd = "bash <(curl -LSs http://repo.jetlicense.com/static/install)"
            subprocess.run(install_cmd, shell=True, check=True)
            
            # Instalar JetBackup 5 versión estable para cPanel
            try:
                subprocess.run(["jetapps", "--install", "jetbackup5-cpanel", "stable"], check=True)
            except subprocess.CalledProcessError as e:
                # Si falla porque ya está instalado, no lo consideramos un error
                if "Package is already installed" in str(e.output) if e.output else "":
                    print("JetBackup ya está instalado. Continuando con la configuración...")
                else:
                    raise e
            
            # Configurar actualizaciones automáticas
            subprocess.run(["jetapps", "-p", "jetbackup5-cpanel", "yes"], check=True)
            
            # Verificar la instalación
            if self.verify_installation():
                print("JetBackup instalado y configurado correctamente.")
                self.notifier.notify_success("JetBackup instalado y configurado correctamente.")
                return True
            else:
                raise Exception("No se pudo verificar la instalación de JetBackup")
            
        except subprocess.CalledProcessError as e:
            # Si el error es porque ya está instalado, no lo consideramos un error fatal
            if "Package is already installed" in str(e.output) if e.output else "":
                print("JetBackup ya está instalado. Continuando con el proceso...")
                self.notifier.notify_success("JetBackup ya está instalado. Continuando...")
                return True
            
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
            result = subprocess.run(
                ["jetapps", "-v", "jetbackup5-cpanel"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print(f"Estado de JetBackup: {result.stdout}")
            return True
        except subprocess.CalledProcessError:
            print("No se pudo verificar la instalación de JetBackup")
            return False