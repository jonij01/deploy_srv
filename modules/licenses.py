import os
import subprocess
import time
from utils.discord_notifier import DiscordNotifier

class LicenseManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier
        self.cloudlinux_key = None
        self.imunify360_key = None
        self.install_path = "/deploy_cPanelTools/config"

    def run_command(self, command, shell=False, timeout=600):
        """
        Ejecuta un comando y muestra la salida en tiempo real con timeout
        """
        try:
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            output = []
            start_time = time.time()

            while True:
                if time.time() - start_time > timeout:
                    process.kill()
                    print(f"Timeout después de {timeout} segundos")
                    return 1, ["Timeout"]

                line = process.stdout.readline()
                error = process.stderr.readline()

                if line:
                    print(line.strip())
                    output.append(line.strip())
                if error:
                    print(f"Error: {error.strip()}")
                    output.append(error.strip())

                if line == '' and error == '' and process.poll() is not None:
                    break

            return process.poll(), output

        except Exception as e:
            print(f"Error ejecutando comando: {str(e)}")
            return 1, [str(e)]

    def wait_for_cpanel(self, timeout=300):
        """
        Espera a que cPanel esté completamente instalado y funcionando
        """
        print("\nEsperando a que cPanel esté listo...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if os.path.exists("/usr/local/cpanel/cpanel"):
                    returncode, _ = self.run_command("systemctl status cpanel", shell=True)
                    if returncode == 0:
                        print("✓ cPanel está listo")
                        return True
            except Exception:
                pass
            print(".", end="", flush=True)
            time.sleep(10)
        print("\n✗ Timeout esperando a cPanel")
        return False

    def check_cloudlinux_license(self):
        """
        Verifica si CloudLinux ya está activado usando cldetect
        """
        try:
            print("\nVerificando licencia de CloudLinux...")
            returncode, output = self.run_command(['cldetect', '--check-license'])

            if returncode == 0 and any('OK' in line for line in output):
                print("✓ CloudLinux está activado y con licencia válida.")
                self.notifier.notify_success("CloudLinux está activado y licenciado.")
                return True

            returncode, output = self.run_command(['rhn-channel', '--list'])
            if returncode == 0 and any('cloudlinux' in line.lower() for line in output):
                print("✓ CloudLinux está registrado en los canales.")
                self.notifier.notify_success("CloudLinux está registrado.")
                return True

            print("✗ CloudLinux no está activado o requiere licencia.")
            return False

        except Exception as e:
            print(f"✗ Error al verificar la licencia de CloudLinux: {str(e)}")
            return False

    def check_imunify360_installation(self):
        """
        Verifica si Imunify360 ya está instalado.
        """
        try:
            print("\nVerificando instalación de Imunify360...")
            
            returncode, _ = self.run_command(['which', 'imunify360-agent'])
            if returncode == 0:
                service_check, output = self.run_command(['systemctl', 'status', 'imunify360'])

                if service_check == 0 and any('active (running)' in line for line in output):
                    print("✓ Imunify360 está instalado y el servicio está activo.")
                    return True
                else:
                    print("⚠ Imunify360 está instalado, pero el servicio no está activo.")
                    return False

            print("✗ Imunify360 no está instalado.")
            return False

        except Exception as e:
            print(f"✗ Error al verificar Imunify360: {str(e)}")
            return False

    def set_license_keys(self):
        """
        Solicita y almacena las claves de licencia solo si son necesarias
        """
        try:
            print("\n=== Configuración de Licencias ===")
            
            cloudlinux_active = self.check_cloudlinux_license()
            imunify_installed = self.check_imunify360_installation()

            if not cloudlinux_active:
                self.cloudlinux_key = input("\nIngrese la clave de activación de CloudLinux: ").strip()
                if not self.cloudlinux_key:
                    print("✗ Error: La clave de CloudLinux no puede estar vacía")
                    self.notifier.notify_error("Error: Clave de CloudLinux vacía")
                    return False

            if not imunify_installed:
                self.imunify360_key = input("Ingrese la clave de licencia de Imunify360: ").strip()
                if not self.imunify360_key:
                    print("✗ Error: La clave de Imunify360 no puede estar vacía")
                    self.notifier.notify_error("Error: Clave de Imunify360 vacía")
                    return False

            if cloudlinux_active and imunify_installed:
                print("\n✓ Todos los servicios ya están activados y licenciados.")

            return True

        except Exception as e:
            print(f"✗ Error al configurar las licencias: {str(e)}")
            self.notifier.notify_error(f"Error al configurar las licencias: {str(e)}")
            return False

    def install_cloudlinux_license(self):
        """
        Instala la licencia de CloudLinux solo si es necesario
        """
        try:
            if self.check_cloudlinux_license():
                return True

            if not self.cloudlinux_key:
                print("✗ Error: No se ha configurado la clave de CloudLinux")
                self.notifier.notify_error("Error: Clave de CloudLinux no configurada")
                return False

            print("\nInstalando licencia de CloudLinux...")
            self.run_command("yum clean all", shell=True)

            command = f"/usr/sbin/rhnreg_ks --activationkey={self.cloudlinux_key} --force --migrate-silently"
            returncode, output = self.run_command(command, shell=True)

            if returncode == 0:
                print("✓ Licencia de CloudLinux instalada correctamente.")
                self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")

                time.sleep(10)
                return self.check_cloudlinux_license()

            print("✗ Error en la activación de CloudLinux")
            self.notifier.notify_error("Error activando CloudLinux")
            return False

        except Exception as e:
            print(f"✗ Error en la activación de CloudLinux: {str(e)}")
            self.notifier.notify_error(f"Error en activación de CloudLinux: {str(e)}")
            return False

    def install_imunify360(self):
        """
        Instala Imunify360 con verificaciones mejoradas y manejo correcto de la key
        """
        try:
            if self.check_imunify360_installation():
                print("✅ Imunify360 ya está instalado")
                return True

            if not self.wait_for_cpanel():
                print("❌ Error: cPanel no está listo para la instalación de Imunify360")
                return False

            if not self.imunify360_key:
                print("❌ Error: No se ha configurado la clave de Imunify360")
                return False

            print("\n📦 Instalando Imunify360...")
            os.makedirs(self.install_path, exist_ok=True)

            download_command = f"""
            cd {self.install_path} && \
            rm -f i360deploy.sh && \
            wget https://repo.imunify360.cloudlinux.com/defence360/i360deploy.sh && \
            chmod +x i360deploy.sh
            """
            returncode, _ = self.run_command(download_command, shell=True)

            if returncode != 0:
                print("❌ Error al preparar el script de instalación")
                self.notifier.notify_error("Error al preparar la instalación de Imunify360")
                return False

            install_command = f"cd {self.install_path} && ./i360deploy.sh --key {self.imunify360_key}"
            returncode, output = self.run_command(install_command, shell=True, timeout=900)

            if returncode == 0:
                print("✅ Imunify360 instalado correctamente")
                time.sleep(30)
                return self.check_imunify360_installation()

            print("❌ Error al instalar Imunify360")
            self.notifier.notify_error("Error al instalar Imunify360")
            return False

        except Exception as e:
            print(f"❌ Error al instalar Imunify360: {str(e)}")
            self.notifier.notify_error(f"Error al instalar Imunify360: {str(e)}")
            return False

    def install_all(self):
        """
        Instala tanto CloudLinux como Imunify360 solo si es necesario
        """
        cloudlinux_active = self.check_cloudlinux_license()
        imunify_installed = self.check_imunify360_installation()

        if cloudlinux_active and imunify_installed:
            print("\n✓ Todos los servicios ya están activados y licenciados.")
            return True

        if not self.set_license_keys():
            print("✗ Error: No se pudieron configurar las licencias necesarias.")
            return False

        if not cloudlinux_active and self.cloudlinux_key:
            if not self.install_cloudlinux_license():
                print("✗ Error: Falló la instalación de la licencia de CloudLinux")
                return False

        if not imunify_installed and self.imunify360_key:
            if not self.install_imunify360():
                print("✗ Error: Falló la instalación de Imunify360")
                return False

        print("\n✓ Instalación completada con éxito")
        return True