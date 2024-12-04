import subprocess
from utils.discord_notifier import DiscordNotifier

class SoftaculousManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def _enable_ioncube(self):
        """
        Habilita ionCube en cPanel/WHM usando whmapi1.
        """
        try:
            print("Habilitando ionCube...")
            
            # Configurar ionCube usando whmapi1
            subprocess.run([
                "whmapi1", 
                "set_tweaksetting",
                "key=phploader",
                "value=ioncube"
            ], check=True)

            # Verificar php.ini
            subprocess.run(["/usr/local/cpanel/bin/checkphpini"], check=True)

            # Instalar/Actualizar configuración de PHP
            subprocess.run(["/usr/local/cpanel/bin/install_php_inis"], check=True)

            print("ionCube habilitado correctamente.")
            self.notifier.notify_success("ionCube habilitado correctamente.")
        except Exception as e:
            error_msg = f"Error habilitando ionCube: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise

    def install_softaculous(self):
        """
        Habilita ionCube e instala Softaculous.
        """
        try:
            # Primero habilitar ionCube
            self._enable_ioncube()

            print("Instalando Softaculous...")
            subprocess.run(["wget", "-N", "https://files.softaculous.com/install.sh"], check=True)
            subprocess.run(["chmod", "+x", "install.sh"], check=True)
            subprocess.run(["./install.sh"], check=True)
            
            # Limpiar archivo de instalación
            subprocess.run(["rm", "-f", "install.sh"], check=True)
            
            print("Softaculous instalado correctamente.")
            self.notifier.notify_success("Softaculous instalado correctamente.")
            
        except Exception as e:
            error_msg = f"Error en el proceso de instalación: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise
