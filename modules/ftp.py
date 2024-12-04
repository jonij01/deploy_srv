import subprocess
from utils.discord_notifier import DiscordNotifier

class FTPManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def install_pureftpd(self):
        """
        Instala y configura el servidor FTP Pure-FTPd.
        """
        try:
            print("Instalando Pure-FTPd...")
            subprocess.run(["yum", "install", "pure-ftpd", "-y"], check=True)
            print("Pure-FTPd instalado correctamente.")
            self.notifier.notify_success("Pure-FTPd instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar Pure-FTPd: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Pure-FTPd: {str(e)}")

    def configure_pureftpd(self):
        """
        Configura Pure-FTPd utilizando los archivos de configuración.
        """
        try:
            print("Configurando Pure-FTPd...")
            
            # Modificar configuración para bind y puertos pasivos
            config_content = f"""
Bind                    1257
PassivePortRange        30000 35000
"""
            
            # Escribir configuración
            with open("/etc/pure-ftpd/pure-ftpd.conf", "w") as config_file:
                config_file.write(config_content)
            
            subprocess.run(["systemctl", "restart", "pure-ftpd"], check=True)
            print("Pure-FTPd configurado correctamente.")
            self.notifier.notify_success("Pure-FTPd configurado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al configurar Pure-FTPd: {str(e)}")
            self.notifier.notify_error(f"Error al configurar Pure-FTPd: {str(e)}")