from modules.os_manager import OSManager
from modules.licenses import LicenseManager
from modules.cpanel import CPanelManager
from modules.csf import CSFManager
from modules.ftp import FTPManager
from modules.disks import DiskManager
from modules.softaculous import SoftaculousManager
from modules.jetbackup import JetBackupManager
from modules.litespeed import LiteSpeedManager
from modules.cron_manager import CronManager
from utils.discord_notifier import DiscordNotifier
from modules.easyapache_manager import EasyApacheManager


class ServerSetupScript:
    """
    Clase principal que controla el flujo del script de configuración del servidor.
    """
    def __init__(self):
        # Inicializar el sistema de notificaciones de Discord
        self.notifier = DiscordNotifier("https://discord.com/api/webhooks/1313584502207152128/YyVnmkV4WbZyeQGFz4jYOZlusx1WZaWMd8IyEAi7VSvBl6zaphcwW3mV7yT9Am55uFag")

        # Inicializar las clases principales para manejar las configuraciones
        self.os_manager = OSManager(self.notifier)
        self.license_manager = LicenseManager(self.notifier)
        self.cpanel_manager = CPanelManager(self.notifier)
        self.csf_manager = CSFManager(self.notifier)
        self.ftp_manager = FTPManager(self.notifier)
        self.disk_manager = DiskManager(self.notifier)
        self.softaculous_manager = SoftaculousManager(self.notifier)
        self.jetbackup_manager = JetBackupManager(self.notifier)
        self.litespeed_manager = LiteSpeedManager(self.notifier)
        self.cron_manager = CronManager(self.notifier)
        self.easyapache_manager = EasyApacheManager("/deploy_srv/config", self.notifier)

    def main_menu(self):
        """
        Muestra el menú principal del script y retorna la opción seleccionada.
        """
        print("\n=========================================")
        print("  Script de Configuración de Servidor")
        print("=========================================")
        print("1. Configuración automática")
        print("2. Configuración manual")
        print("3. Salir")
        print("=========================================")
        choice = input("Seleccione una opción: ")
        return choice

    def manual_menu(self):
        """
        Muestra el menú para la configuración manual y retorna la opción seleccionada.
        """
        print("\n=========================================")
        print("  Configuración Manual")
        print("=========================================")
        print("1. Verificar sistema operativo")
        print("2. Instalar/verificar licencia de CloudLinux")
        print("3. Instalar cPanel")
        print("4. Actualizar sistema operativo")
        print("5. Instalar/verificar Imunify360")
        print("6. Instalar CSF")
        print("7. Configurar CSF")
        print("8. Configurar Pure-FTPd")
        print("9. Montar discos")
        print("10. Instalar Softaculous")
        print("11. Instalar JetBackup")
        print("12. Montar perfil de EasyApache4")
        print("13. Instalar LiteSpeed")
        print("14. Añadir Cronjobs")
        print("15. Volver al menú principal")
        print("=========================================")
        choice = input("Seleccione un paso: ")
        return choice

    def run_automatic_setup(self):
        """
        Ejecuta la configuración automática del servidor.
        """
        print("Iniciando configuración automática...")
        try:
            self.os_manager.update_system()
            self.license_manager.install_cloudlinux_license()
            self.cpanel_manager.install_cpanel()
            self.license_manager.install_imunify360()
            self.csf_manager.install_csf()
            self.csf_manager.configure_csf()
            self.ftp_manager.configure_ftp()
            self.disk_manager.mount_disks()
            self.softaculous_manager.install_softaculous()
            self.jetbackup_manager.install_jetbackup()
            self.os_manager.configure_easyapache()
            self.litespeed_manager.install_litespeed()
            self.cron_manager.add_cronjobs()
            print("¡Configuración automática completada con éxito!")
            self.notifier.notify_success("Configuración automática completada con éxito.")
        except Exception as e:
            print(f"Error durante la configuración automática: {str(e)}")
            self.notifier.notify_error(f"Error durante la configuración automática: {str(e)}")

    def run_manual_setup(self):
        """
        Permite realizar configuraciones manuales seleccionando pasos específicos.
        """
        while True:
            manual_choice = self.manual_menu()
            if manual_choice == "1":
                self.os_manager.check_os()
            elif manual_choice == "2":
                self.license_manager.install_cloudlinux_license()
            elif manual_choice == "3":
                self.cpanel_manager.install_cpanel()
            elif manual_choice == "4":
                self.os_manager.update_system()
            elif manual_choice == "5":
                self.license_manager.install_imunify360()
            elif manual_choice == "6":
                self.csf_manager.install_csf()
            elif manual_choice == "7":
                self.csf_manager.configure_csf()
            elif manual_choice == "8":
                self.ftp_manager.configure_ftp()
            elif manual_choice == "9":
                self.disk_manager.mount_disks()
            elif manual_choice == "10":
                self.softaculous_manager.install_softaculous()
            elif manual_choice == "11":
                self.jetbackup_manager.install_jetbackup()
            elif manual_choice == "12":
                self.os_manager.configure_easyapache()
            elif manual_choice == "13":
                self.litespeed_manager.install_litespeed()
            elif manual_choice == "14":
                self.cron_manager.add_cronjobs()
            elif manual_choice == "15":
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

    def run(self):
        """
        Método principal que controla el flujo del script.
        """
        while True:
            choice = self.main_menu()

            if choice == "1":  # Configuración automática
                self.run_automatic_setup()

            elif choice == "2":  # Configuración manual
                self.run_manual_setup()

            elif choice == "3":  # Salir
                print("Saliendo del script...")
                break

            else:
                print("Opción no válida. Por favor, intente de nuevo.")


# Ejecutar el script
if __name__ == "__main__":
    script = ServerSetupScript()
    script.run()