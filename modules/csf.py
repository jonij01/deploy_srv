import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class CSFManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def run_command(self, command, shell=False, check=False):
        """
        Ejecuta un comando y muestra la salida en tiempo real.
        """
        try:
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            output, error = process.communicate()
            if process.returncode != 0 and check:
                raise subprocess.CalledProcessError(process.returncode, command, output, error)
            return process.returncode, output, error
        except Exception as e:
            print(f"Error ejecutando comando '{command}': {str(e)}")
            return 1, "", str(e)

    def install_csf(self):
        """
        Instala el firewall CSF descargándolo desde la fuente oficial.
        """
        try:
            print("Descargando e instalando CSF...")

            # Descargar el paquete CSF desde la fuente oficial
            _, _, error = self.run_command(["wget", "https://download.configserver.com/csf.tgz"], check=True)
            if error:
                raise Exception(f"Error al descargar CSF: {error}")

            # Extraer el archivo descargado
            _, _, error = self.run_command(["tar", "-xzf", "csf.tgz"], check=True)
            if error:
                raise Exception(f"Error al extraer el archivo CSF: {error}")

            # Cambiar al directorio de instalación
            os.chdir("csf")

            # Ejecutar el script de instalación
            _, output, error = self.run_command(["sh", "install.sh"], check=True)
            if error:
                raise Exception(f"Error al ejecutar el script de instalación de CSF: {error}")
            print(output)

            # Volver al directorio anterior
            os.chdir("..")

            # Limpiar archivos descargados
            _, _, error = self.run_command(["rm", "-rf", "csf", "csf.tgz"], check=True)
            if error:
                print(f"Error al limpiar archivos: {error}")

            print("CSF instalado correctamente.")
            self.notifier.notify_success("CSF instalado correctamente.")
            return True
        except Exception as e:
            print(f"Error al instalar CSF: {str(e)}")
            self.notifier.notify_error(f"Error al instalar CSF: {str(e)}")
            return False

    def configure_csf(self):
        """
        Configura CSF utilizando los archivos en config/csf/.
        """
        try:
            print("Configurando CSF...")

            # Copiar archivos de configuración personalizados
            _, _, error = self.run_command(["cp", "config/csf/csf.conf", "/etc/csf/csf.conf"], check=True)
            if error:
                raise Exception(f"Error al copiar csf.conf: {error}")

            _, _, error = self.run_command(["cp", "config/csf/csf.allow", "/etc/csf/csf.allow"], check=True)
            if error:
                raise Exception(f"Error al copiar csf.allow: {error}")

            _, _, error = self.run_command(["cp", "config/csf/csf.deny", "/etc/csf/csf.deny"], check=True)
            if error:
                raise Exception(f"Error al copiar csf.deny: {error}")

            # Reiniciar CSF para aplicar los cambios
            _, output, error = self.run_command(["csf", "-r"], check=True)
            if error:
                raise Exception(f"Error al reiniciar CSF: {error}")
            print(output)

            print("CSF configurado correctamente.")
            self.notifier.notify_success("CSF configurado correctamente.")
            return True
        except Exception as e:
            print(f"Error al configurar CSF: {str(e)}")
            self.notifier.notify_error(f"Error al configurar CSF: {str(e)}")
            return False

    def install_and_configure_csf(self):
        """
        Instala y configura CSF, asegurando que el proceso continúe incluso si hay errores.
        """
        if self.install_csf() and self.configure_csf():
            print("Instalación y configuración de CSF completadas con éxito.")
        else:
            print("Hubo errores durante la instalación o configuración de CSF, pero el script continuará.")