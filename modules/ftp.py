import subprocess
from utils.discord_notifier import DiscordNotifier

class FTPManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def set_pureftpd_as_default(self):
        """
        Configura Pure-FTPd como el servidor FTP predeterminado en cPanel.
        """
        try:
            print("Configurando Pure-FTPd como el servidor FTP predeterminado en cPanel...")
            subprocess.run(["/usr/local/cpanel/scripts/setupftpserver", "pure-ftpd"], check=True)
            print("Pure-FTPd configurado como servidor FTP predeterminado correctamente.")
            self.notifier.notify_success("Pure-FTPd configurado como servidor FTP predeterminado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al configurar Pure-FTPd como predeterminado: {str(e)}")
            self.notifier.notify_error(f"Error al configurar Pure-FTPd como predeterminado: {str(e)}")

    def configure_pureftpd(self):
        """
        Configura Pure-FTPd utilizando los archivos de configuración.
        """
        try:
            print("Modificando configuración de Pure-FTPd...")

            # Contenido personalizado para el archivo de configuración
            config_content = """
# Configuración personalizada de Pure-FTPd
Bind                    1257
PassivePortRange        30000 35000
"""
            # Escribir la configuración en el archivo correspondiente
            with open("/etc/pure-ftpd/pure-ftpd.conf", "w") as config_file:
                config_file.write(config_content)

            # Reiniciar el servicio para aplicar cambios
            subprocess.run(["systemctl", "restart", "pure-ftpd"], check=True)
            print("Pure-FTPd configurado correctamente con los ajustes personalizados.")
            self.notifier.notify_success("Pure-FTPd configurado correctamente con los ajustes personalizados.")
        except FileNotFoundError as fnf_error:
            print(f"Error: No se encontró el archivo de configuración: {str(fnf_error)}")
            self.notifier.notify_error(f"Error: No se encontró el archivo de configuración: {str(fnf_error)}")
        except subprocess.CalledProcessError as e:
            print(f"Error al reiniciar Pure-FTPd: {str(e)}")
            self.notifier.notify_error(f"Error al reiniciar Pure-FTPd: {str(e)}")
        except Exception as e:
            print(f"Error inesperado al configurar Pure-FTPd: {str(e)}")
            self.notifier.notify_error(f"Error inesperado al configurar Pure-FTPd: {str(e)}")

    def setup_pureftpd(self):
        """
        Configura Pure-FTPd como predeterminado y aplica ajustes personalizados.
        """
        try:
            # Configurar Pure-FTPd como predeterminado en cPanel
            self.set_pureftpd_as_default()

            # Aplicar configuraciones personalizadas
            self.configure_pureftpd()
        except Exception as e:
            print(f"Error durante la configuración de Pure-FTPd: {str(e)}")
            self.notifier.notify_error(f"Error durante la configuración de Pure-FTPd: {str(e)}")
