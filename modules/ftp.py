import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class FTPManager:
    """
    Clase para gestionar la configuración del servidor FTP.
    """
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def configure_ftp(self):
        """
        Método principal que configura Pure-FTPd como servidor FTP predeterminado y aplica ajustes personalizados.
        """
        try:
            # Verificar permisos de superusuario
            if os.geteuid() != 0:
                print("Este script debe ejecutarse con permisos de superusuario (root).")
                self.notifier.notify_error("El script no tiene permisos de superusuario. Abortando configuración de FTP.")
                return

            # Configurar Pure-FTPd como servidor FTP predeterminado en cPanel
            self.set_pureftpd_as_default()

            # Aplicar configuraciones personalizadas a Pure-FTPd
            self.configure_pureftpd()

            print("Configuración de Pure-FTPd completada con éxito.")
            self.notifier.notify_success("Configuración de Pure-FTPd completada con éxito.")

        except Exception as e:
            print(f"Error durante la configuración de Pure-FTPd: {str(e)}")
            self.notifier.notify_error(f"Error durante la configuración de Pure-FTPd: {str(e)}")

    def set_pureftpd_as_default(self):
        """
        Configura Pure-FTPd como el servidor FTP predeterminado en cPanel.
        """
        try:
            print("Configurando Pure-FTPd como el servidor FTP predeterminado en cPanel...")
            subprocess.run(["/usr/local/cpanel/scripts/setupftpserver", "pure-ftpd", "--force"], check=True)
            print("Pure-FTPd configurado como servidor FTP predeterminado correctamente.")
            self.notifier.notify_success("Pure-FTPd configurado como servidor FTP predeterminado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al configurar Pure-FTPd como predeterminado: {str(e)}")
            self.notifier.notify_error(f"Error al configurar Pure-FTPd como predeterminado: {str(e)}")
        except Exception as e:
            print(f"Error inesperado al configurar Pure-FTPd como predeterminado: {str(e)}")
            self.notifier.notify_error(f"Error inesperado al configurar Pure-FTPd como predeterminado: {str(e)}")

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

            # Ruta al archivo de configuración
            config_path = "/etc/pure-ftpd/pure-ftpd.conf"

            # Verificar que el archivo de configuración existe
            if not os.path.exists(os.path.dirname(config_path)):
                error_msg = f"El directorio de configuración no existe: {os.path.dirname(config_path)}"
                print(f"Error: {error_msg}")
                self.notifier.notify_error(f"Error: {error_msg}")
                return

            # Escribir la configuración en el archivo correspondiente
            with open(config_path, "w") as config_file:
                config_file.write(config_content.strip())

            # Reiniciar el servicio para aplicar cambios
            subprocess.run(["systemctl", "restart", "pure-ftpd"], check=True)
            print("Pure-FTPd configurado correctamente con los ajustes personalizados.")
            self.notifier.notify_success("Pure-FTPd configurado correctamente con los ajustes personalizados.")
        except FileNotFoundError as fnf_error:
            error_msg = f"No se encontró el archivo de configuración: {str(fnf_error)}"
            print(f"Error: {error_msg}")
            self.notifier.notify_error(f"Error: {error_msg}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al reiniciar Pure-FTPd: {str(e)}"
            print(f"Error: {error_msg}")
            self.notifier.notify_error(f"Error: {error_msg}")
        except Exception as e:
            error_msg = f"Error inesperado al configurar Pure-FTPd: {str(e)}"
            print(f"Error: {error_msg}")
            self.notifier.notify_error(f"Error: {error_msg}")