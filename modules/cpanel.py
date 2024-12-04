import subprocess
from utils.discord_notifier import DiscordNotifier

class CPanelManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_cpanel(self):
        """
        Instala cPanel en el servidor.
        """
        try:
            print("Instalando cPanel...")
            subprocess.run(["cd", "/home"], check=True)
            subprocess.run(["wget", "-N", "http://httpupdate.cpanel.net/latest"], check=True)
            subprocess.run(["sh", "latest"], check=True)
            print("cPanel instalado correctamente.")
            self.notifier.notify_success("cPanel instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar cPanel: {str(e)}")
            self.notifier.notify_error(f"Error al instalar cPanel: {str(e)}")
