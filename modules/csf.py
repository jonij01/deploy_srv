import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class CSFManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_csf(self):
        """
        Instala el firewall CSF descargándolo desde la fuente oficial.
        """
        try:
            print("Descargando e instalando CSF...")

            # Descargar el paquete CSF desde la fuente oficial
            subprocess.run(["wget", "https://download.configserver.com/csf.tgz"], check=True)

            # Extraer el archivo descargado
            subprocess.run(["tar", "-xzf", "csf.tgz"], check=True)

            # Cambiar al directorio de instalación
            os.chdir("csf")

            # Ejecutar el script de instalación
            subprocess.run(["sh", "install.sh"], check=True)

            # Volver al directorio anterior
            os.chdir("..")

            # Limpiar archivos descargados
            subprocess.run(["rm", "-rf", "csf", "csf.tgz"], check=True)

            print("CSF instalado correctamente.")
            self.notifier.notify_success("CSF instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar CSF: {str(e)}")
            self.notifier.notify_error(f"Error al instalar CSF: {str(e)}")
        except Exception as e:
            print(f"Error inesperado durante la instalación de CSF: {str(e)}")
            self.notifier.notify_error(f"Error inesperado durante la instalación de CSF: {str(e)}")

    def configure_csf(self):
        """
        Configura CSF utilizando los archivos en config/csf/.
        """
        try:
            print("Configurando CSF...")

            # Copiar archivos de configuración personalizados
            subprocess.run(["cp", "config/csf/csf.conf", "/etc/csf/csf.conf"], check=True)
            subprocess.run(["cp", "config/csf/csf.allow", "/etc/csf/csf.allow"], check=True)
            subprocess.run(["cp", "config/csf/csf.deny", "/etc/csf/csf.deny"], check=True)

            # Reiniciar CSF para aplicar los cambios
            subprocess.run(["csf", "-r"], check=True)

            print("CSF configurado correctamente.")
            self.notifier.notify_success("CSF configurado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al configurar CSF: {str(e)}")
            self.notifier.notify_error(f"Error al configurar CSF: {str(e)}")
        except Exception as e:
            print(f"Error inesperado durante la configuración de CSF: {str(e)}")
            self.notifier.notify_error(f"Error inesperado durante la configuración de CSF: {str(e)}")