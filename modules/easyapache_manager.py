import os
import json
import subprocess
from datetime import datetime
from typing import Optional
from utils.discord_notifier import DiscordNotifier

class EasyApacheManager:
    def __init__(self, config_path: str, notifier: Optional[DiscordNotifier] = None):
        # Buscar el archivo EasyGeneral.json en el sistema
        self.config_path = self._find_config_file()
        if not self.config_path:
            raise FileNotFoundError("No se pudo encontrar EasyGeneral.json en el sistema")
            
        # Una vez encontrado el archivo, establecer las rutas
        self.config_dir = os.path.dirname(self.config_path)
        self.profile_path = self.config_path
        self.backup_dir = os.path.join(self.config_dir, 'backups')
        self.notifier = notifier
        
        # Crear directorio de backups si no existe
        os.makedirs(self.backup_dir, exist_ok=True)

    def _find_config_file(self) -> str:
        """
        Busca el archivo EasyGeneral.json en ubicaciones comunes
        """
        possible_locations = [
            '/deploy_cPanelTools/config/easyapache',
            '/config/easyapache/EasyGeneral.json',
            './config/easyapache/EasyGeneral.json',
            '../config/easyapache/EasyGeneral.json'
        ]

        # Buscar en las ubicaciones posibles
        for location in possible_locations:
            if os.path.exists(location):
                print(f"Archivo de configuración encontrado en: {location}")
                return location

        # Si no se encuentra, buscar recursivamente desde la raíz
        for root, dirs, files in os.walk('/'):
            if 'EasyGeneral.json' in files:
                path = os.path.join(root, 'EasyGeneral.json')
                print(f"Archivo de configuración encontrado en: {path}")
                return path

        return None

    def diagnose_easyapache_profile(self) -> None:
        """
        Realiza un diagnóstico completo de la configuración de EasyApache4.
        """
        print("=== Diagnóstico de EasyApache4 ===\n")
        
        # Verificar archivo de perfil
        if os.path.exists(self.profile_path):
            print("✓ Archivo de perfil encontrado")
            try:
                with open(self.profile_path, 'r') as f:
                    print(f.read())
            except Exception as e:
                print(f"Error al leer archivo: {str(e)}")
        else:
            print("✗ Archivo de perfil no encontrado")

        # Verificar permisos
        try:
            perms = oct(os.stat(self.profile_path).st_mode)[-3:]
            print(f"\nPermisos del archivo: {perms}")
        except Exception as e:
            print(f"\nError al verificar permisos: {str(e)}")

        # Listar perfiles actuales
        try:
            cmd = ["/usr/local/cpanel/bin/whmapi1", "list_ea4_profiles", "--output=json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            print("\nPerfiles EA4 actuales:")
            print(result.stdout)
        except Exception as e:
            print(f"Error al listar perfiles: {str(e)}")

    def backup_current_profile(self) -> str:
        """
        Crea una copia de seguridad del perfil actual.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"ea4_backup_{timestamp}.json")
            
            subprocess.run([
                "/usr/local/bin/ea_current_to_profile",
                f"--output={backup_path}"
            ], check=True)
            
            print(f"Backup creado en: {backup_path}")
            self.notifier.notify_success(f"Backup de EA4 creado: {backup_path}")
            return backup_path
            
        except Exception as e:
            error_msg = f"Error al crear backup: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise

    def validate_profile(self, profile_path: str) -> bool:
        """
        Valida el formato del archivo de perfil.
        """
        try:
            with open(profile_path, 'r') as f:
                data = json.load(f)
            
            required_fields = ['version', 'name', 'pkgs']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Campo requerido '{field}' faltante")
            return True
            
        except Exception as e:
            print(f"Error al validar perfil: {str(e)}")
            return False

    def configure_easyapache(self) -> None:
        """
        Configura EasyApache4 con el perfil especificado.
        """
        try:
            print("Configurando EasyApache4...")
            self.diagnose_easyapache_profile()
            
            if not os.path.exists(self.profile_path):
                raise FileNotFoundError(f"Perfil no encontrado: {self.profile_path}")

            if not self.validate_profile(self.profile_path):
                raise ValueError("Perfil inválido")

            backup_path = self.backup_current_profile()
            
            # Instalar perfil
            subprocess.run([
                "/usr/local/bin/ea_install_profile",
                "--install",
                self.profile_path
            ], check=True)

            # Sincronizar PHP
            subprocess.run([
                "/usr/local/bin/ea_sync_user_phpini_settings",
                "--all-users"
            ], check=True)

            print("EasyApache4 configurado correctamente")
            self.notifier.notify_success("EasyApache4 configurado correctamente")
            
        except Exception as e:
            error_msg = f"Error en configuración de EasyApache4: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise

    def restart_apache(self) -> None:
        """
        Reinicia el servicio de Apache.
        """
        try:
            print("Reiniciando Apache...")
            subprocess.run(["service", "httpd", "restart"], check=True)
            print("Apache reiniciado correctamente")
            self.notifier.notify_success("Apache reiniciado correctamente")
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al reiniciar Apache: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            raise