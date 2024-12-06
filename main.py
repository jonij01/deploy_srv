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
import time

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
        Ejecuta la configuración automática del servidor con el orden correcto.
        """
        print("\n🚀 Iniciando configuración automática...")
        try:
            # 1. Verificar el sistema operativo
            if not self.os_manager.check_os():
                print("❌ Error: Sistema operativo no compatible")
                return False

            # 2. Solicitar las licencias al inicio
            if not self.license_manager.set_license_keys():
                print("❌ Error: No se pudieron configurar las licencias necesarias")
                self.notifier.notify_error("Configuración de licencias fallida")
                return False

            # 3. Instalar CloudLinux primero
            print("\n➡️ Instalando CloudLinux...")
            if not self.license_manager.install_cloudlinux_license():
                print("❌ Error: Falló la instalación de CloudLinux")
                return False

            # 4. Esperar un momento para que CloudLinux se establezca
            print("⏳ Esperando a que CloudLinux se establezca...")
            time.sleep(30)

            # 5. Instalar cPanel
            print("\n➡️ Instalando cPanel...")
            if not self.cpanel_manager.install_cpanel():
                print("❌ Error: Falló la instalación de cPanel")
                return False

            # 6. Esperar a que cPanel esté listo
            print("⏳ Esperando a que cPanel esté completamente instalado...")
            if not self.license_manager.wait_for_cpanel():
                print("❌ Error: Timeout esperando a cPanel")
                return False

            # 7. Instalar Imunify360
            print("\n➡️ Instalando Imunify360...")
            if not self.license_manager.install_imunify360():
                print("❌ Error: Falló la instalación de Imunify360")
                return False

            # 8. Continuar con el resto de las instalaciones
            print("\n➡️ Actualizando sistema...")
            self.os_manager.update_system()

            # Instalar y configurar servicios adicionales
            installation_steps = [
                ("CSF", lambda: self.csf_manager.install_csf()),
                ("Configuración CSF", lambda: self.csf_manager.configure_csf()),
                ("Pure-FTPd", lambda: self.ftp_manager.configure_ftp()),
                ("Montaje de discos", lambda: self.disk_manager.mount_disks()),
                ("Softaculous", lambda: self.softaculous_manager.install_softaculous()),
                ("JetBackup", lambda: self.jetbackup_manager.install_jetbackup()),
                ("EasyApache4", lambda: self.easyapache_manager.configure_easyapache()),
                ("LiteSpeed", lambda: self.litespeed_manager.install_litespeed()),
                ("Cronjobs", lambda: self.cron_manager.add_cronjobs()),
                ("SSHD", lambda: self.sshd_modifier.configure_sshd())
            ]

            for step_name, step_function in installation_steps:
                print(f"\n➡️ Instalando/Configurando {step_name}...")
                try:
                    if not step_function():
                        print(f"⚠️ Advertencia: Falló {step_name}, continuando con el siguiente paso...")
                except Exception as e:
                    print(f"⚠️ Error en {step_name}: {str(e)}")
                    self.notifier.notify_error(f"Error en {step_name}: {str(e)}")

            # Instalar utilidades
            print("\n➡️ Instalando utilidades...")
            self.utilities_installer.install_htop()
            self.utilities_installer.install_redis()
            self.utilities_installer.move_jetbackup_workspace()
            self.utilities_installer.move_scripts_to_maintenance()

            print("\n✅ ¡Configuración automática completada con éxito!")
            self.notifier.notify_success("Configuración automática completada con éxito.")
            return True

        except Exception as e:
            print(f"\n❌ Error durante la configuración automática: {str(e)}")
            self.notifier.notify_error(f"Error durante la configuración automática: {str(e)}")
            return False

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
                    self.handle_utilities_menu()
                elif manual_choice == "17":
                    break
                else:
                    print("⚠️ Opción no válida. Por favor, intente de nuevo.")
            except Exception as e:
                print(f"❌ Error durante la operación manual: {str(e)}")
                self.notifier.notify_error(f"Error durante la operación manual: {str(e)}")

    def handle_utilities_menu(self):
        """
        Maneja el submenú de utilidades
        """
        while True:
            utility_choice = self.utilities_menu()
            try:
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
                    print("⚠️ Opción no válida. Por favor, intente de nuevo.")
            except Exception as e:
                print(f"❌ Error en la instalación de utilidades: {str(e)}")
                self.notifier.notify_error(f"Error en utilidades: {str(e)}")

    def run(self):
        """
        Método principal que ejecuta el script.
        """
        while True:
            try:
                choice = self.main_menu()
                if choice == "1":
                    self.run_automatic_setup()
                elif choice == "2":
                    self.run_manual_setup()
                elif choice == "3":
                    print("👋 Saliendo del script...")
                    break
                else:
                    print("⚠️ Opción no válida. Por favor, intente de nuevo.")
            except KeyboardInterrupt:
                print("\n\n⚠️ Operación cancelada por el usuario")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {str(e)}")
                self.notifier.notify_error(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    setup = ServerSetupScript()
    setup.run()