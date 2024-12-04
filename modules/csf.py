import subprocess
from utils.discord_notifier import DiscordNotifier

class CSFManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_csf(self):
        """
        Instala el firewall CSF.
        """
        try:
            print("Instalando CSF...")
            subprocess.run(["yum", "install", "csf", "-y"], check=True)
            print("CSF instalado correctamente.")
            self.notifier.notify_success("CSF instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar CSF: {str(e)}")
            self.notifier.notify_error(f"Error al instalar CSF: {str(e)}")

    def configure_csf(self):
        """
        Configura CSF utilizando los archivos en config/csf/.
        """
        try:
            print("Configurando CSF...")
            subprocess.run(["cp", "config/csf/csf.conf", "/etc/csf/csf.conf"], check=True)
            subprocess.run(["cp", "config/csf/csf.allow", "/etc/csf/csf.allow"], check=True)
            subprocess.run(["cp", "config/csf/csf.deny", "/etc/csf/csf.deny"], check=True)
            subprocess.run(["csf", "-r"], check=True)  # Reinicia CSF
            print("CSF configurado correctamente.")
            self.notifier.notify_success("CSF configurado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al configurar CSF: {str(e)}")
            self.notifier.notify_error(f"Error al configurar CSF: {str(e)}")
