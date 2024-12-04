import subprocess
from utils.discord_notifier import DiscordNotifier

class LicenseManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_cloudlinux_license(self):
        """
        Instala y activa la licencia de CloudLinux.
        """
        try:
            print("Instalando la licencia de CloudLinux...")
            subprocess.run(["/usr/sbin/clnreg_ks", "--register"], check=True)
            print("Licencia de CloudLinux instalada correctamente.")
            self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar la licencia de CloudLinux: {str(e)}")
            self.notifier.notify_error(f"Error al instalar la licencia de CloudLinux: {str(e)}")

    def install_imunify360(self):
        """
        Instala y activa Imunify360.
        """
        try:
            print("Instalando Imunify360...")
            subprocess.run(["wget", "https://repo.imunify360.cloudlinux.com/defence360/i360deploy.sh", "-O", "i360deploy.sh"], check=True)
            subprocess.run(["bash", "i360deploy.sh"], check=True)
            print("Imunify360 instalado correctamente.")
            self.notifier.notify_success("Imunify360 instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar Imunify360: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Imunify360: {str(e)}")