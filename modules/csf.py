import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class CSFManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier
        self.csf_config_path = "/etc/csf"

    def install_csf(self):
        """
        Instala CSF desde el repositorio oficial
        """
        try:
            print("Instalando CSF...")

            # Eliminar instalaciones previas si existen
            if os.path.exists("csf"):
                subprocess.run(["rm", "-rf", "csf"], check=True)
            if os.path.exists("csf.tgz"):
                subprocess.run(["rm", "-f", "csf.tgz"], check=True)

            # Descargar e instalar CSF
            subprocess.run(["wget", "https://download.configserver.com/csf.tgz"], check=True)
            subprocess.run(["tar", "-xzf", "csf.tgz"], check=True)
            
            # Instalar
            os.chdir("csf")
            subprocess.run(["sh", "install.sh"], check=True)
            os.chdir("..")

            # Limpiar archivos de instalación
            subprocess.run(["rm", "-rf", "csf", "csf.tgz"], check=True)

            print("CSF instalado correctamente")
            self.notifier.notify_success("CSF instalado correctamente")
            return True

        except Exception as e:
            error_msg = f"Error en la instalación de CSF: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False

    def configure_csf(self):
        """
        Reemplaza los archivos de configuración de CSF con los personalizados
        """
        try:
            print("Configurando CSF...")
            
            # Lista de archivos a reemplazar
            config_files = ['csf.conf', 'csf.allow', 'csf.deny']
            
            for file in config_files:
                source = f"/deploy_cPanelTools/config/csf/{file}"
                dest = f"{self.csf_config_path}/{file}"
                
                if not os.path.exists(source):
                    raise FileNotFoundError(f"Archivo de configuración no encontrado: {source}")
                
                # Crear backup del archivo original
                if os.path.exists(dest):
                    subprocess.run(["cp", "-f", dest, f"{dest}.bak"], check=True)
                
                # Copiar el nuevo archivo de configuración
                subprocess.run(["cp", "-f", source, dest], check=True)
                print(f"Archivo {file} reemplazado correctamente")

            # Reiniciar CSF para aplicar cambios
            print("Reiniciando CSF...")
            subprocess.run(["csf", "-r"], check=True)

            print("CSF configurado correctamente")
            self.notifier.notify_success("CSF configurado correctamente")
            return True

        except Exception as e:
            error_msg = f"Error en la configuración de CSF: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False