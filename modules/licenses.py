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
            if os.path.exists('/etc/sysconfig/rhn/systemid'):
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
            
            if not self.check_cloudlinux_license():
                self.cloudlinux_key = input("Por favor, ingrese la clave de licencia de CloudLinux: ").strip()
                if not self.cloudlinux_key:
                    print("Error: La clave de CloudLinux no puede estar vacía")
                    self.notifier.notify_error("Error: Clave de CloudLinux vacía")
                    return False
            else:
                print("CloudLinux ya está instalado, omitiendo configuración de licencia.")

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
        """
        try:
            if self.check_cloudlinux_license():
                print("CloudLinux ya está instalado y activado. No es necesario reinstalar.")
                return True

            if os.geteuid() != 0:
                print("Este script debe ejecutarse con permisos de superusuario (root).")
                self.notifier.notify_error("El script no tiene permisos de superusuario. Abortando instalación.")
                return False

            license_key = self.cloudlinux_key if hasattr(self, 'cloudlinux_key') and self.cloudlinux_key else input("Por favor, ingrese la clave de licencia de CloudLinux: ").strip()

            if not license_key:
                print("No se proporcionó ninguna clave de licencia. Abortando instalación.")
                self.notifier.notify_error("No se proporcionó ninguna clave de licencia de CloudLinux. Instalación abortada.")
                return False

            print("Intentando instalar la licencia de CloudLinux...")
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

            if result.returncode == 0:
                print("Licencia de CloudLinux instalada correctamente.")
                self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")
                return True
            else:
                print(f"Advertencia: No se pudo activar la licencia de CloudLinux. Código de error: {result.returncode}")
                print(f"Salida del comando: {result.stderr.strip() or result.stdout.strip()}")
                self.notifier.notify_error(
                    f"No se pudo activar la licencia de CloudLinux. Código de error: {result.returncode}. "
                    f"Detalles: {result.stderr.strip() or result.stdout.strip()}"
                )
                return False

        except Exception as e:
            print(f"Error inesperado al instalar la licencia de CloudLinux: {str(e)}")
            self.notifier.notify_error(f"Error inesperado al instalar la licencia de CloudLinux: {str(e)}")
            return False

    def install_imunify360(self):
        """
        Instala Imunify360 usando la clave de licencia proporcionada
        """
        try:
            if self.check_imunify360_installation():
                print("Imunify360 ya está instalado. No es necesario reinstalar.")
                return True

            if not self.imunify360_key:
                print("Error: No se ha configurado la clave de licencia de Imunify360")
                self.notifier.notify_error("Error: Clave de Imunify360 no configurada")
                return False

            print("Instalando Imunify360...")
            commands = [
                'wget https://repo.imunify360.cloudlinux.com/defence360/i360deploy.sh',
                f'bash i360deploy.sh --key {self.imunify360_key}',
                'rm -f i360deploy.sh'
            ]

            for cmd in commands:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    text=True,
                    capture_output=True
                )
                
                if result.returncode != 0:
                    print(f"Error ejecutando comando: {cmd}")
                    print(f"Error: {result.stderr}")
                    self.notifier.notify_error(f"Error instalando Imunify360: {result.stderr}")
                    return False

            print("Imunify360 instalado exitosamente.")
            self.notifier.notify_success("Imunify360 instalado exitosamente.")
            return True

        except Exception as e:
            print(f"Error al instalar Imunify360: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Imunify360: {str(e)}")
            return False