import subprocess
import os
from utils.discord_notifier import DiscordNotifier


class LicenseManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_cloudlinux_license(self):
        """
        Solicita la clave de licencia de CloudLinux, la valida e intenta instalarla.
        """
        try:
            # Solicitar la clave de licencia al usuario
            license_key = input("Por favor, ingrese la clave de licencia de CloudLinux: ").strip()

            # Validar que se haya proporcionado una clave
            if not license_key:
                print("No se proporcionó ninguna clave de licencia. Abortando instalación.")
                self.notifier.notify_error("No se proporcionó ninguna clave de licencia de CloudLinux. Instalación abortada.")
                return False

            print("Instalando la licencia de CloudLinux...")
            # Ejecutar el comando de registro con la clave proporcionada
            subprocess.run(["/usr/sbin/clnreg_ks", "--register", license_key], check=True)

            print("Licencia de CloudLinux instalada correctamente.")
            self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error al instalar la licencia de CloudLinux: {str(e)}")
            self.notifier.notify_error(f"Error al instalar la licencia de CloudLinux: {str(e)}")
            return False

        except Exception as e:
            print(f"Error inesperado al instalar la licencia de CloudLinux: {str(e)}")
            self.notifier.notify_error(f"Error inesperado al instalar la licencia de CloudLinux: {str(e)}")
            return False

    def install_imunify360(self):
        """
        Solicita la clave de licencia de Imunify360, la valida e intenta instalar el software.
        """
        try:
            # Solicitar la clave de licencia al usuario
            license_key = input("Por favor, ingrese la clave de licencia de Imunify360: ").strip()

            # Validar que se haya proporcionado una clave
            if not license_key:
                print("No se proporcionó ninguna clave de licencia. Abortando instalación.")
                self.notifier.notify_error("No se proporcionó ninguna clave de licencia de Imunify360. Instalación abortada.")
                return False

            print("Descargando e instalando Imunify360...")
            # Descargar el script de instalación
            subprocess.run(["wget", "https://repo.imunify360.cloudlinux.com/defence360/i360deploy.sh", "-O", "i360deploy.sh"], check=True)

            # Ejecutar el script de instalación
            subprocess.run(["bash", "i360deploy.sh"], check=True)

            # Registrar la licencia de Imunify360
            subprocess.run(["imunify360-agent", "register", license_key], check=True)

            print("Imunify360 instalado y registrado correctamente.")
            self.notifier.notify_success("Imunify360 instalado y registrado correctamente.")

            # Eliminar el script descargado para limpieza
            if os.path.exists("i360deploy.sh"):
                os.remove("i360deploy.sh")

            return True

        except subprocess.CalledProcessError as e:
            print(f"Error al instalar Imunify360: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Imunify360: {str(e)}")
            return False

        except Exception as e:
            print(f"Error inesperado al instalar Imunify360: {str(e)}")
            self.notifier.notify_error(f"Error inesperado al instalar Imunify360: {str(e)}")
            return False
