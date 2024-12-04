import subprocess
from utils.discord_notifier import DiscordNotifier

class LiteSpeedManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_litespeed(self):
        """
        Instala y configura LiteSpeed.
        """
        try:
            print("Instalando LiteSpeed...")
            subprocess.run(["wget", "https://www.litespeedtech.com/packages/cpanel/lsws_whm_plugin_install.sh"], check=True)
            subprocess.run(["bash", "lsws_whm_plugin_install.sh"], check=True)
            print("LiteSpeed instalado correctamente.")
            self.notifier.notify_success("LiteSpeed instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar LiteSpeed: {str(e)}")
            self.notifier.notify_error(f"Error al instalar LiteSpeed: {str(e)}")
