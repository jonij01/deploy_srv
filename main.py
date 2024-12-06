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
from modules.sshd_modifier import SSHDModifier
from modules.utilities_installer import UtilitiesInstaller

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
        # ClasesNuevas
        self.sshd_modifier = SSHDModifier(self.notifier)
        self.utilities_installer = UtilitiesInstaller(self.notifier)

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
   [15] 🌐 Configure SSHD
   [16] 🔧 Install Utilities
   [17] 🔙 Back to Main Menu
        '''
        print(menu)
        choice = input("Select your option: ")
        return choice

    def utilities_menu(self):
        """
        Muestra un submenú para seleccionar la utilidad a instalar.
        """
        menu = '''
  ╭──────────────────────────────────────────╮
  │      🔧 INSTALL UTILITIES SUBMENU       │
  ╰──────────────────────────────────────────╯
  
   [1] Instalar htop
   [2] Instalar Redis
   [3] Mover workspace de JetBackup
   [4] Mover scripts a la carpeta de mantenimiento
   [5] Volver al menú manual
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

            # 2. Continuar con el resto de las instalaciones
            self.license_manager.install_cloudlinux_license()
            self.cpanel_manager.install_cpanel()
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
            self.sshd_modifier.configure_sshd()
            self.utilities_installer.install_htop()
            self.utilities_installer.install_redis()
            self.utilities_installer.move_jetbackup_workspace()
            self.utilities_installer.move_scripts_to_maintenance()
               
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
                    self.license_manager.set_license_keys()
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
                    self.easyapache_manager.configure_easyapache()
                elif manual_choice == "13":
                    self.litespeed_manager.install_litespeed()
                elif manual_choice == "14":
                    self.cron_manager.add_cronjobs()
                elif manual_choice == "15":
                    self.sshd_modifier.configure_sshd()
                elif manual_choice == "16":
                    while True:
                        utility_choice = self.utilities_menu()
                        if utility_choice == "1":
                            self.utilities_installer.install_htop()
                        elif utility_choice == "2":
                            self.utilities_installer.install_redis()
                        elif utility_choice == "3":
                            self.utilities_installer.move_jetbackup_workspace()
                        elif utility_choice == "4":
                            self.utilities_installer.move_scripts_to_maintenance()
                        elif utility_choice == "5":
                            break
                        else:
                            print("Opción no válida. Por favor, intente de nuevo.")
                elif manual_choice == "17":
                    break
                elif manual_choice == "18":
                    print("Saliendo del script...")
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
    script = ServerSetupScript()
    script.run()