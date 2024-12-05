import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class CPanelManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def check_cpanel_installed(self):
        """
        Verifica si cPanel ya está instalado en el servidor
        """
        try:
            # Verificar la existencia del directorio de cPanel
            if os.path.exists("/usr/local/cpanel"):
                # Verificar el proceso de cPanel
                result = subprocess.run(
                    ["ps", "aux"], 
                    capture_output=True, 
                    text=True
                )
                return "cpanel" in result.stdout
            return False
        except:
            return False

    def install_cpanel(self):
        """
        Verifica e instala cPanel en el servidor si no está instalado.
        """
        try:
            # Verificar si cPanel ya está instalado
            if self.check_cpanel_installed():
                print("cPanel ya está instalado. Continuando con el proceso...")
                self.notifier.notify_success("cPanel ya está instalado. Continuando...")
                return True

            print("Instalando cPanel...")
            
            # Cambiar al directorio home
            os.chdir("/home")
            
            # Descargar el instalador de cPanel
            subprocess.run(
                ["wget", "-N", "http://httpupdate.cpanel.net/latest"], 
                check=True
            )
            
            # Ejecutar el instalador
            subprocess.run(["sh", "latest"], check=True)
            
            # Verificar la instalación
            if self.check_cpanel_installed():
                print("cPanel instalado correctamente.")
                self.notifier.notify_success("cPanel instalado correctamente.")
                return True
            else:
                raise Exception("No se pudo verificar la instalación de cPanel")
                
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al instalar cPanel: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado durante la instalación de cPanel: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise Exception(error_msg)

    def verify_installation(self):
        """
        Verifica el estado de la instalación de cPanel
        """
        return self.check_cpanel_installed()
