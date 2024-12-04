import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class LicenseManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_cloudlinux_license(self):
        """
        Solicita la clave de licencia de CloudLinux, valida e intenta instalarla.
        Si requiere migración, acepta automáticamente la migración.
        """
        try:
            # Validar si el script se ejecuta con permisos de superusuario
            if os.geteuid() != 0:
                print("Este script debe ejecutarse con permisos de superusuario (root).")
                self.notifier.notify_error("El script no tiene permisos de superusuario. Abortando instalación.")
                return False

            # Solicitar la clave de licencia al usuario
            license_key = input("Por favor, ingrese la clave de licencia de CloudLinux: ").strip()

            # Validar que se haya proporcionado una clave
            if not license_key:
                print("No se proporcionó ninguna clave de licencia. Abortando instalación.")
                self.notifier.notify_error("No se proporcionó ninguna clave de licencia de CloudLinux. Instalación abortada.")
                return False

            print("Intentando instalar la licencia de CloudLinux...")
            # Ejecutar el comando de registro con la clave proporcionada y aceptar migración automáticamente
            command = [
                "/usr/sbin/rhnreg_ks",
                f"--activationkey={license_key}",
                "--force",
                "--migrate-silently"
            ]
            result = subprocess.run(
                command,
                text=True,
                capture_output=True
            )

            # Validar el código de salida del comando
            if result.returncode == 0:
                print("Licencia de CloudLinux instalada correctamente.")
                self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")
                return True
            else:
                # Si falla la activación, mostrar el error pero continuar
                print(f"Advertencia: No se pudo activar la licencia de CloudLinux. Código de error: {result.returncode}")
                print(f"Salida del comando: {result.stderr.strip() or result.stdout.strip()}")
                self.notifier.notify_error(
                    f"No se pudo activar la licencia de CloudLinux. Código de error: {result.returncode}. "
                    f"Detalles: {result.stderr.strip() or result.stdout.strip()}"
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

    def install_imunify360(self):
        """
        Solicita la clave de licencia de Imunify360, valida e instala Imunify360 en el servidor.
        """
        try:
            # Validar si el script se ejecuta con permisos de superusuario
            if os.geteuid() != 0:
                print("Este script debe ejecutarse con permisos de superusuario (root).")
                self.notifier.notify_error("El script no tiene permisos de superusuario. Abortando instalación.")
                return False

            # Solicitar la clave de licencia al usuario
            license_key = input("Por favor, ingrese la clave de licencia de Imunify360: ").strip()

            # Validar que se haya proporcionado una clave
            if not license_key:
                print("No se proporcionó ninguna clave de licencia. Abortando instalación.")
                self.notifier.notify_error("No se proporcionó ninguna clave de licencia de Imunify360. Instalación abortada.")
                return False

            print("Instalando Imunify360...")
            # Descargar el script de instalación
            download_command = [
                "wget",
                "https://repo.imunify360.cloudlinux.com/defence360/i360deploy.sh"
            ]
            download_result = subprocess.run(
                download_command,
                text=True,
                capture_output=True
            )

            # Verificar si la descarga fue exitosa
            if download_result.returncode != 0:
                print(f"Error al descargar el script de instalación de Imunify360.")
                print(f"Detalles: {download_result.stderr.strip() or download_result.stdout.strip()}")
                self.notifier.notify_error(
                    f"No se pudo descargar el script de instalación de Imunify360. "
                    f"Detalles: {download_result.stderr.strip() or download_result.stdout.strip()}"
                )
                return False

            # Hacer el script ejecutable
            os.chmod("i360deploy.sh", 0o700)

            # Ejecutar el script de instalación con la clave de licencia
            install_command = [
                "bash",
                "i360deploy.sh",
                "--key",
                license_key
            ]
            install_result = subprocess.run(
                install_command,
                text=True,
                capture_output=True
            )

            # Validar el código de salida del comando de instalación
            if install_result.returncode == 0:
                print("Imunify360 instalado correctamente.")
                self.notifier.notify_success("Imunify360 instalado correctamente.")
                return True
            else:
                print(f"Advertencia: No se pudo instalar Imunify360. Código de error: {install_result.returncode}")
                print(f"Salida del comando: {install_result.stderr.strip() or install_result.stdout.strip()}")
                self.notifier.notify_error(
                    f"No se pudo instalar Imunify360. Código de error: {install_result.returncode}. "
                    f"Detalles: {install_result.stderr.strip() or install_result.stdout.strip()}"
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
            print(f"Error inesperado al instalar Imunify360: {str(e)}")
            self.notifier.notify_error(f"Error inesperado al instalar Imunify360: {str(e)}")
            return False