import subprocess
from utils.discord_notifier import DiscordNotifier

class SoftaculousManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_softaculous(self):
        """
        Instala y configura Softaculous.
        """
        try:
            print("Instalando Softaculous...")
            subprocess.run(["wget", "-N", "https://files.softaculous.com/install.sh"], check=True)
            subprocess.run(["chmod", "+x", "install.sh"], check=True)
            subprocess.run(["./install.sh"], check=True)
            print("Softaculous instalado correctamente.")
            self.notifier.notify_success("Softaculous instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar Softaculous: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Softaculous: {str(e)}")
