import subprocess
import os
from utils.discord_notifier import DiscordNotifier


class LicenseManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_cloudlinux_license(self):
        """
        Solicita la clave de licencia de CloudLinux, la valida e intenta instalarla.
        Si falla la activación, el script continuará con una advertencia.
        """
        try:
            # Validar si el script se ejecuta con permisos de superusuario
            if os.geteuid() != 0:
                print("Este script debe ejecutarse con permisos de superusuario (root).")
                self.notifier.notify_error("El script no tiene permisos de superusuario. Abortando instalación.")
                return False

            # Validar si el comando rhnreg_ks está disponible
            if not os.path.exists("/usr/sbin/rhnreg_ks"):
                print("El comando 'rhnreg_ks' no está disponible en este sistema.")
                self.notifier.notify_error("El comando 'rhnreg_ks' no está disponible. Abortando instalación.")
                return False

            # Solicitar la clave de licencia al usuario
            license_key = input("Por favor, ingrese la clave de licencia de CloudLinux: ").strip()

            # Validar que se haya proporcionado una clave
            if not license_key:
                print("No se proporcionó ninguna clave de licencia. Abortando instalación.")
                self.notifier.notify_error("No se proporcionó ninguna clave de licencia de CloudLinux. Instalación abortada.")
                return False

            print("Intentando instalar la licencia de CloudLinux...")
            # Ejecutar el comando de registro con la clave proporcionada
            result = subprocess.run(
                ["/usr/sbin/rhnreg_ks", "--activationkey", license_key, "--force"],
                check=False,  # No interrumpir el flujo si el comando falla
                capture_output=True,
                text=True
            )

            # Validar el código de salida del comando
            if result.returncode == 0:
                print("Licencia de CloudLinux instalada correctamente.")
                self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")
                return True
            else:
                # Si falla la activación, mostrar el error pero continuar
                print(f"Advertencia: No se pudo activar la licencia de CloudLinux. Código de error: {result.returncode}")
                print(f"Salida del comando: {result.stderr.strip()}")
                self.notifier.notify_warning(
                    f"No se pudo activar la licencia de CloudLinux. Código de error: {result.returncode}. "
                    f"Detalles: {result.stderr.strip()}"
                )
                return False

        except FileNotFoundError as e:
            print(f"Error: No se encontró el archivo o comando necesario: {str(e)}")
            self.notifier.notify_error(f"Error: No se encontró el archivo o comando necesario: {str(e)}")
            return False

        except PermissionError as e:
            print(f"Error de permisos: {str(e)}")
            self.notifier.notify_error(f"Error de permisos: {str(e)}")
            return False

        except Exception as e:
            print(f"Error inesperado al instalar la licencia de CloudLinux: {str(e)}")
            self.notifier.notify_error(f"Error inesperado al instalar la licencia de CloudLinux: {str(e)}")
            return False