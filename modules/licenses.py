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
        Verifica si CloudLinux ya está activado
        """
        try:
            print("Verificando licencia de CloudLinux...")
            result = subprocess.run(['rhn-channel', '--list'], text=True, capture_output=True)
            
            if result.returncode == 0 and 'cloudlinux' in result.stdout.lower():
                print("✓ CloudLinux ya está activado en este sistema.")
                self.notifier.notify_success("CloudLinux ya está activado.")
                return True

            print("✗ CloudLinux no está activado.")
            return False

        except Exception as e:
            print(f"✗ Error al verificar la licencia de CloudLinux: {str(e)}")
            return False

    def check_imunify360_installation(self):
        """
        Verifica si Imunify360 ya está instalado
        """
        try:
            print("Verificando instalación de Imunify360...")
            result = subprocess.run(['systemctl', 'status', 'imunify360'], text=True, capture_output=True)
            
            if result.returncode == 0:
                print("✓ Imunify360 ya está instalado y activo.")
                self.notifier.notify_success("Imunify360 ya está instalado.")
                return True

            print("✗ Imunify360 no está instalado.")
            return False

        except Exception as e:
            print(f"✗ Error al verificar Imunify360: {str(e)}")
            return False

    def set_license_keys(self):
        """
        Solicita y almacena las claves de licencia
        """
        try:
            print("\n=== Configuración de Licencias ===")

            if not self.check_cloudlinux_license():
                self.cloudlinux_key = input("\nIngrese la clave de activación de CloudLinux: ").strip()
                if not self.cloudlinux_key:
                    print("✗ Error: La clave de CloudLinux no puede estar vacía")
                    self.notifier.notify_error("Error: Clave de CloudLinux vacía")
                    return False

            if not self.check_imunify360_installation():
                self.imunify360_key = input("\nIngrese la clave de licencia de Imunify360: ").strip()
                if not self.imunify360_key:
                    print("✗ Error: La clave de Imunify360 no puede estar vacía")
                    self.notifier.notify_error("Error: Clave de Imunify360 vacía")
                    return False

            return True

        except Exception as e:
            print(f"✗ Error al configurar las licencias: {str(e)}")
            self.notifier.notify_error(f"Error al configurar las licencias: {str(e)}")
            return False

    def install_cloudlinux_license(self):
        """
        Instala la licencia de CloudLinux
        """
        try:
            if not self.cloudlinux_key:
                print("Error: No se ha configurado la clave de activación")
                self.notifier.notify_error("Error: Clave de CloudLinux no configurada")
                return False

            print("Intentando instalar la licencia de CloudLinux...")

            # Ejecutar el comando con --migrate-silently para aceptar automáticamente la migración
            command = f"/usr/sbin/rhnreg_ks --activationkey={self.cloudlinux_key} --force --migrate-silently"
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✓ Licencia de CloudLinux instalada correctamente.")
                self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")
                return True
            else:
                print(f"✗ Error en la activación: {result.stderr}")
                self.notifier.notify_error(f"Error activando CloudLinux: {result.stderr}")
                return False

        except Exception as e:
            print(f"✗ Error en la activación de CloudLinux: {str(e)}")
            self.notifier.notify_error(f"Error en activación de CloudLinux: {str(e)}")
            return False

    def install_imunify360_license(self):
        """
        Instala la licencia de Imunify360
        """
        try:
            if not self.imunify360_key:
                print("Error: No se ha configurado la clave de Imunify360")
                self.notifier.notify_error("Error: Clave de Imunify360 no configurada")
                return False

            print("Instalando licencia de Imunify360...")
            
            # Comando para instalar la licencia de Imunify360
            result = subprocess.run(
                ['imunify360-agent', 'register', self.imunify360_key],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✓ Licencia de Imunify360 instalada correctamente")
                self.notifier.notify_success("Licencia de Imunify360 instalada correctamente")
                return True
            else:
                print(f"✗ Error al instalar la licencia de Imunify360: {result.stderr}")
                self.notifier.notify_error(f"Error al instalar Imunify360: {result.stderr}")
                return False

        except Exception as e:
            print(f"✗ Error al instalar la licencia de Imunify360: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Imunify360: {str(e)}")
            return False

    def install_licenses(self):
        """
        Instala ambas licencias
        """
        success = True

        if not self.check_cloudlinux_license():
            if not self.install_cloudlinux_license():
                success = False

        if not self.check_imunify360_installation():
            if not self.install_imunify360_license():
                success = False

        return success