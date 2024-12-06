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
    def __init__(self):
        # Mantener todas las inicializaciones como están
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
        menu = '''
                     .  　　　　　　　 ✦ 　　　　   ✦ 　　　　
    　　　　　　　　　　 　.　　　　　　    　　　　 　　　　　.
             🚀 HELLO.CO HOSTING cPanelToolsInstall 🛸
    　　　　　　　　　　　　　　　　　　  　　　　　　　　　　　
    ╭──────────────────────────────────────────╮
    │                                          │
    │      [1] 🛠️  Automatic Setup            │
    │                                          │
    │      [2] 🎮  Manual Setup               │
    │                                          │
    │      [3] 🚪  Exit                       │
    │                                          │
    ╰──────────────────────────────────────────╯
        '''
        print(menu)
        choice = input("Select your option: ")
        return choice

    def manual_menu(self):
        """
        Muestra el menú para la configuración manual y retorna la opción seleccionada.
        """
        menu = '''
    ╭──────────────────────────────────────────────────╮
    │           🔧 MANUAL CONFIGURATION 🔧             │
    ╰──────────────────────────────────────────────────╯
    
     [1]  📊 Check Operating System
     [2]  🔑 Install/Verify CloudLinux License
     [3]  🎛️  Install cPanel
     [4]  🔄 Update Operating System
     [5]  🛡️  Install/Verify Imunify360
     [6]  🔒 Install CSF
     [7]  ⚙️  Configure CSF
     [8]  📡 Configure Pure-FTPd
     [9]  💾 Mount Disks
     [10] 📦 Install Softaculous
     [11] 💫 Install JetBackup
     [12] 🔧 Mount EasyApache4 Profile
     [13] ⚡ Install LiteSpeed
     [14] ⏰ Add Cronjobs
     [15] 🔙 Back to Main Menu
    
    ╭──────────────────────────────────────────────────╮
        '''
        print(menu)
        choice = input("Select your option: ")
        return choice

    def run_automatic_setup(self):
        """
        Ejecuta la configuración automática del servidor.
        """
        print("Iniciando configuración automática...")
        try:
            # 1. Solicitar las licencias al inicio
            if not self.license_manager.set_license_keys():
                print("Error: No se pudieron configurar las licencias necesarias.")
                self.notifier.notify_error("Configuración de licencias fallida")
                return

            # 2. Instalar licencia de CloudLinux
            if not self.license_manager.install_cloudlinux_license():
                print("Error: Falló la instalación de la licencia de CloudLinux")
                self.notifier.notify_error("Falló la instalación de CloudLinux")
                return

            # 3. Instalar cPanel
            if not self.cpanel_manager.install_cpanel():
                print("Error: Falló la instalación de cPanel")
                self.notifier.notify_error("Falló la instalación de cPanel")
                return

            # 4. Instalar Imunify360
            if not self.license_manager.install_imunify360():
                print("Advertencia: Falló la instalación de Imunify360")
                self.notifier.notify_warning("Falló la instalación de Imunify360")
                # Continuamos con el resto del proceso aunque falle Imunify360

            # Continuar con el resto de las instalaciones
            self.os_manager.update_system()
            self.csf_manager.install_csf()
            self.csf_manager.configure_csf()
            self.ftp_manager.configure_ftp()
            self.disk_manager.mount_disks()
            self.softaculous_manager.install_softaculous()
            self.jetbackup_manager.install_jetbackup()
            self.easyapache_manager.configure_easyapache()
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
            try:
                if manual_choice == "1":
                    self.os_manager.check_os()
                elif manual_choice == "2":
                    # Asegurar que tenemos las licencias antes de instalar
                    if not hasattr(self.license_manager, 'cloudlinux_key'):
                        self.license_manager.set_license_keys()
                    self.license_manager.install_cloudlinux_license()
                elif manual_choice == "3":
                    self.cpanel_manager.install_cpanel()
                elif manual_choice == "4":
                    self.os_manager.update_system()
                elif manual_choice == "5":
                    # Asegurar que tenemos las licencias antes de instalar
                    if not hasattr(self.license_manager, 'imunify360_key'):
                        self.license_manager.set_license_keys()
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
                    self.easyapache_manager.configure_easyapache()
                elif manual_choice == "13":
                    self.litespeed_manager.install_litespeed()
                elif manual_choice == "14":
                    self.cron_manager.add_cronjobs()
                elif manual_choice == "15":
                    break
                else:
                    print("Opción no válida. Por favor, intente de nuevo.")
            except Exception as e:
                print(f"Error durante la operación manual: {str(e)}")
                self.notifier.notify_error(f"Error durante la operación manual: {str(e)}")

    def run(self):
        """
        Método principal que ejecuta el script.
        """
        while True:
            choice = self.main_menu()
            if choice == "1":
                self.run_automatic_setup()
            elif choice == "2":
                self.run_manual_setup()
            elif choice == "3":
                print("Saliendo del script...")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    setup = ServerSetupScript()
    setup.run()