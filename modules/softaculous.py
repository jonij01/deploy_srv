import subprocess
import os
from typing import Optional
from utils.discord_notifier import DiscordNotifier

class SoftaculousManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier
        self.installation_path = "/usr/local/cpanel"
        self.softaculous_script = "https://files.softaculous.com/install.sh"

    def _check_prerequisites(self) -> bool:
        """
        Verifica los prerequisitos necesarios
        """
        try:
            # Verificar si cPanel está instalado
            if not os.path.exists(self.installation_path):
                raise Exception("cPanel no está instalado en este servidor")

            # Verificar acceso root
            if os.geteuid() != 0:
                raise Exception("Este script debe ejecutarse como root")

            return True

        except Exception as e:
            error_msg = f"Error en verificación de prerequisitos: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False

    def _enable_ioncube(self) -> bool:
        """
        Habilita ionCube modificando la configuración y ejecutando los comandos necesarios
        """
        try:
            print("Habilitando ionCube...")
            
            # 1. Modificar el archivo de configuración
            config_file = "/var/cpanel/cpanel.config"
            config_updated = False
            
            # Leer el archivo actual
            with open(config_file, 'r') as f:
                lines = f.readlines()
            
            # Modificar o agregar la línea de phploader
            with open(config_file, 'w') as f:
                phploader_found = False
                for line in lines:
                    if line.startswith('phploader='):
                        phploader_found = True
                        if 'ioncube' not in line:
                            if '=' in line.strip() and line.strip() != 'phploader=':
                                line = line.strip() + ',ioncube\n'
                            else:
                                line = 'phploader=ioncube\n'
                        config_updated = True
                    f.write(line)
                
                if not phploader_found:
                    f.write('phploader=ioncube\n')
                    config_updated = True

            if config_updated:
                print("Configuración de phploader actualizada")
            
            # 2. Ejecutar los comandos necesarios
            commands = [
                "/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings",
                "/usr/local/cpanel/bin/checkphpini",
                "/usr/local/cpanel/bin/install_php_inis"
            ]

            for cmd in commands:
                print(f"Ejecutando: {cmd}")
                subprocess.run(cmd, shell=True, check=True)

            print("ionCube habilitado correctamente")
            self.notifier.notify_success("ionCube habilitado correctamente")
            return True

        except Exception as e:
            error_msg = f"Error habilitando ionCube: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False

    def _download_softaculous(self) -> Optional[str]:
        """
        Descarga el script de instalación de Softaculous
        """
        try:
            print("Descargando script de instalación de Softaculous...")
            
            # Descargar script
            subprocess.run([
                "wget",
                "-N",
                self.softaculous_script
            ], check=True)

            # Dar permisos de ejecución
            script_path = "./install.sh"
            subprocess.run(["chmod", "+x", script_path], check=True)
            
            return script_path

        except Exception as e:
            error_msg = f"Error descargando Softaculous: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return None

    def _execute_installation(self, script_path: str) -> bool:
        """
        Ejecuta el script de instalación de Softaculous
        """
        try:
            print("Instalando Softaculous...")
            
            # Ejecutar instalación
            process = subprocess.Popen(
                [script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitorear salida en tiempo real
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            # Verificar resultado
            if process.returncode != 0:
                raise Exception("La instalación falló")

            # Limpiar archivos temporales
            subprocess.run(["rm", "-f", script_path], check=True)
            
            print("Softaculous instalado correctamente")
            self.notifier.notify_success("Softaculous instalado correctamente")
            return True

        except Exception as e:
            error_msg = f"Error en la instalación: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False

    def install_softaculous(self) -> bool:
        """
        Proceso principal de instalación de Softaculous
        """
        try:
            # Verificar prerequisitos
            if not self._check_prerequisites():
                return False

            # Habilitar ionCube
            if not self._enable_ioncube():
                return False

            # Descargar Softaculous
            script_path = self._download_softaculous()
            if not script_path:
                return False

            # Ejecutar instalación
            if not self._execute_installation(script_path):
                return False

            return True

        except Exception as e:
            error_msg = f"Error en el proceso de instalación: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False

    def verify_installation(self) -> bool:
        """
        Verifica que la instalación se completó correctamente
        """
        try:
            # Verificar archivos y directorios críticos
            critical_paths = [
                "/usr/local/cpanel/whostmgr/docroot/cgi/softaculous",
                "/usr/local/cpanel/whostmgr/docroot/cgi/softaculous/enduser"
            ]

            for path in critical_paths:
                if not os.path.exists(path):
                    raise Exception(f"Ruta crítica no encontrada: {path}")

            print("Verificación de instalación completada exitosamente")
            self.notifier.notify_success("Verificación de instalación completada exitosamente")
            return True

        except Exception as e:
            error_msg = f"Error en la verificación: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False
