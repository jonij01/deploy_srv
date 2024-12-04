import subprocess
from utils.discord_notifier import DiscordNotifier

class JetBackupManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_jetbackup(self):
        """
        Instala y configura JetBackup.
        """
        try:
            print("Instalando JetBackup...")
            subprocess.run(["yum", "install", "-y", "https://repo.jetlicense.com/centOS/jetapps-repo-latest.rpm"], check=True)
            subprocess.run(["yum", "install", "-y", "jetbackup5"], check=True)
            print("JetBackup instalado correctamente.")
            self.notifier.notify_success("JetBackup instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar JetBackup: {str(e)}")
            self.notifier.notify_error(f"Error al instalar JetBackup: {str(e)}")
