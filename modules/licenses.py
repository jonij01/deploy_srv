import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class LicenseManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier
        self.cloudlinux_key = None
        self.imunify360_key = None

    def check_cloudlinux_license(self):
        """
        Verifica si CloudLinux ya está instalado y activado
        """
        try:
            # Verificar si el archivo de licencia existe
            if os.path.exists('/etc/sysconfig/rhn/systemid'):
                # Intentar obtener información de la licencia
                result = subprocess.run(
                    ['rhn-channel', '--list'],
                    text=True,
                    capture_output=True
                )
                
                if result.returncode == 0 and 'cloudlinux' in result.stdout.lower():
                    print("CloudLinux ya está instalado y activado en este sistema.")
                    self.notifier.notify_success("CloudLinux ya está instalado y activado.")
                    return True
            return False
            
        except Exception as e:
            print(f"Error al verificar la licencia de CloudLinux: {str(e)}")
            return False

    def check_imunify360_installation(self):
        """
        Verifica si Imunify360 ya está instalado
        """
        try:
            # Verificar si el servicio imunify360 existe
            result = subprocess.run(
                ['systemctl', 'status', 'imunify360'],
                text=True,
                capture_output=True
            )
            
            if result.returncode == 0:
                print("Imunify360 ya está instalado en este sistema.")
                self.notifier.notify_success("Imunify360 ya está instalado.")
                return True
            return False
            
        except Exception as e:
            print(f"Error al verificar la instalación de Imunify360: {str(e)}")
            return False

    def set_license_keys(self):
        """
        Solicita y almacena las claves de licencia para su uso posterior
        """
        try:
            print("\n=== Configuración de Licencias ===")
            
            # Primero verificar CloudLinux
            if not self.check_cloudlinux_license():
                self.cloudlinux_key = input("Por favor, ingrese la clave de licencia de CloudLinux: ").strip()
                if not self.cloudlinux_key:
                    print("Error: La clave de CloudLinux no puede estar vacía")
                    self.notifier.notify_error("Error: Clave de CloudLinux vacía")
                    return False
            else:
                print("CloudLinux ya está instalado, omitiendo configuración de licencia.")

            # Luego verificar Imunify360
            if not self.check_imunify360_installation():
                self.imunify360_key = input("Por favor, ingrese la clave de licencia de Imunify360: ").strip()
                if not self.imunify360_key:
                    print("Error: La clave de Imunify360 no puede estar vacía")
                    self.notifier.notify_error("Error: Clave de Imunify360 vacía")
                    return False
            else:
                print("Imunify360 ya está instalado, omitiendo configuración de licencia.")

            return True

        except Exception as e:
            print(f"Error al configurar las licencias: {str(e)}")
            self.notifier.notify_error(f"Error al configurar las licencias: {str(e)}")
            return False

    def install_cloudlinux_license(self):
        """
        Solicita la clave de licencia de CloudLinux, valida e intenta instalarla.
        Si requiere migración, acepta automáticamente la migración.
        """
        try:
            # Verificar si CloudLinux ya está instalado
            if self.check_cloudlinux_license():
                print("CloudLinux ya está instalado y activado. No es necesario reinstalar.")
                return True

            # Validar si el script se ejecuta con permisos de superusuario
            if os.geteuid() != 0:
                print("Este script debe ejecutarse con permisos de superusuario (root).")
                self.notifier.notify_error("El script no tiene permisos de superusuario. Abortando instalación.")
                return False

            # Usar la clave almacenada si existe, si no, solicitarla
            license_key = self.cloudlinux_key if hasattr(self, 'cloudlinux_key') and self.cloudlinux_key else input("Por favor, ingrese la clave de licencia de CloudLinux: ").strip()

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
        Instala Imunify360 en el servidor usando la clave de licencia proporcionada.
        """
        try:
            # Verificar si Imunify360 ya está instalado
            if self.check_imunify360_installation():
                print("Imunify360 ya está instalado. No es necesario reinstalar.")
                return True

            # Validar permisos de superusuario
            if os.geteuid() != 0:
                print("Este script debe ejecutarse con permisos de superusuario (root).")
                self.notifier.notify_error("El script no tiene permisos de superusuario. Abortando instalación.")
                return False

            # Usar la clave almacenada o solicitarla
            license_key = self.imunify360_key if hasattr(self, 'imunify360_key') and self.imunify360_key else input("Por favor, ingrese la clave de licencia de Imunify360: ").strip()

            if not license_key:
                print("No se proporcionó ninguna clave de licencia. Abortando instalación.")
                self.notifier.notify_error("No se proporcionó ninguna clave de licencia de Imunify360. Instalación abortada.")
                return False

            print("Instalando Imunify360...")
            
            # Descargar el script de instalación
            if not os.path.exists('i360deploy.sh'):
                download_command = "wget https://repo.imunify360.cloudlinux.com/defence360/i360deploy.sh"
                download_result = subprocess.run(
                    download_command,
                    shell=True,
                    text=True,
                    capture_output=True
                )

                if download_result.returncode != 0:
                    print(f"Error al descargar el script de instalación de Imunify360.")
                    print(f"Detalles: {download_result.stderr}")
                    self.notifier.notify_error(f"Error al descargar script de Imunify360: {download_result.stderr}")
                    return False

            # Hacer el script ejecutable
            os.chmod("i360deploy.sh", 0o755)

            # Ejecutar el script de instalación
            install_command = f"bash i360deploy.sh --key {license_key}"
            print(f"Ejecutando: {install_command}")
            
            install_result = subprocess.run(
                install_command,
                shell=True,
                text=True,
                capture_output=True
            )

            # Mostrar la salida en tiempo real
            print(install_result.stdout)
            if install_result.stderr:
                print(install_result.stderr)

            if install_result.returncode == 0:
                print("Imunify360 instalado correctamente.")
                self.notifier.notify_success("Imunify360 instalado correctamente.")
                return True
            else:
                error_msg = f"Error al instalar Imunify360. Código: {install_result.returncode}"
                print(error_msg)
                print(f"Salida: {install_result.stdout}")
                print(f"Error: {install_result.stderr}")
                self.notifier.notify_error(error_msg)
                return False

        except Exception as e:
            error_msg = f"Error inesperado al instalar Imunify360: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False