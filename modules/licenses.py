import os
import subprocess
from utils.discord_notifier import DiscordNotifier

class LicenseManager:
  def __init__(self, notifier: DiscordNotifier):
      self.notifier = notifier
      self.cloudlinux_key = None
      self.imunify360_key = None
      self.install_path = "/deploy_srv/config"

  def run_command(self, command, shell=False):
      """
      Ejecuta un comando y muestra la salida en tiempo real
      """
      try:
          if shell:
              process = subprocess.Popen(
                  command,
                  shell=True,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE,
                  universal_newlines=True
              )
          else:
              process = subprocess.Popen(
                  command,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE,
                  universal_newlines=True
              )

          output = []
          while True:
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
          return 1, []

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
          
          # Verificación adicional con rhn-channel
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
      Verifica si Imunify360 ya está instalado
      """
      try:
          print("\nVerificando instalación de Imunify360...")
          returncode, output = self.run_command(['systemctl', 'status', 'imunify360'])
          
          if returncode == 0:
              print("✓ Imunify360 ya está instalado y activo.")
              self.notifier.notify_success("Imunify360 ya está instalado.")
              return True

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
          
          # Verificar CloudLinux primero
          cloudlinux_active = self.check_cloudlinux_license()
          
          if not cloudlinux_active:
              self.cloudlinux_key = input("\nIngrese la clave de activación de CloudLinux: ").strip()
              if not self.cloudlinux_key:
                  print("✗ Error: La clave de CloudLinux no puede estar vacía")
                  self.notifier.notify_error("Error: Clave de CloudLinux vacía")
                  return False
          
          # Verificar Imunify360
          imunify_installed = self.check_imunify360_installation()
          
          if not imunify_installed:
              self.imunify360_key = input("Ingrese la clave de licencia de Imunify360: ").strip()
              if not self.imunify360_key:
                  print("✗ Error: La clave de Imunify360 no puede estar vacía")
                  self.notifier.notify_error("Error: Clave de Imunify360 vacía")
                  return False

          # Si ambos están activos, no necesitamos hacer nada
          if cloudlinux_active and imunify_installed:
              print("\n✓ Todos los servicios ya están activados y licenciados.")
              return True

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
          # Si ya está activado, no hacemos nada
          if self.check_cloudlinux_license():
              return True

          if not self.cloudlinux_key:
              print("✗ Error: No se ha configurado la clave de CloudLinux")
              self.notifier.notify_error("Error: Clave de CloudLinux no configurada")
              return False

          print("\nInstalando licencia de CloudLinux...")
          command = f"/usr/sbin/rhnreg_ks --activationkey={self.cloudlinux_key} --force --migrate-silently"
          
          returncode, _ = self.run_command(command, shell=True)
          
          if returncode == 0:
              print("✓ Licencia de CloudLinux instalada correctamente.")
              self.notifier.notify_success("Licencia de CloudLinux instalada correctamente.")
              return True
          else:
              print("✗ Error en la activación de CloudLinux")
              self.notifier.notify_error("Error activando CloudLinux")
              return False

      except Exception as e:
          print(f"✗ Error en la activación de CloudLinux: {str(e)}")
          self.notifier.notify_error(f"Error en activación de CloudLinux: {str(e)}")
          return False

  def install_imunify360(self):
      """
      Instala Imunify360 solo si es necesario
      """
      try:
          # Si ya está instalado, no hacemos nada
          if self.check_imunify360_installation():
              return True

          if not self.imunify360_key:
              print("✗ Error: No se ha configurado la clave de Imunify360")
              self.notifier.notify_error("Error: Clave de Imunify360 no configurada")
              return False

          print("\nInstalando Imunify360...")
          
          # Crear el directorio si no existe
          os.makedirs(self.install_path, exist_ok=True)
          
          # Descargar el script de instalación
          install_script = "i360deploy.sh"
          install_script_path = os.path.join(self.install_path, install_script)
          
          print("Descargando script de instalación...")
          wget_command = f"wget https://repo.imunify360.cloudlinux.com/defence360/i360deploy.sh -O {install_script_path}"
          self.run_command(wget_command, shell=True)
          
          # Dar permisos de ejecución
          os.chmod(install_script_path, 0o755)
          
          # Ejecutar el script de instalación
          print("Ejecutando script de instalación...")
          install_command = f"bash {install_script_path} --key {self.imunify360_key}"
          returncode, _ = self.run_command(install_command, shell=True)
          
          if returncode == 0:
              print("✓ Imunify360 instalado correctamente")
              self.notifier.notify_success("Imunify360 instalado correctamente")
              return True
          else:
              print("✗ Error al instalar Imunify360")
              self.notifier.notify_error("Error al instalar Imunify360")
              return False

      except Exception as e:
          print(f"✗ Error al instalar Imunify360: {str(e)}")
          self.notifier.notify_error(f"Error al instalar Imunify360: {str(e)}")
          return False

  def install_all(self):
      """
      Instala tanto CloudLinux como Imunify360 solo si es necesario
      """
      # Primero verificamos el estado actual
      cloudlinux_active = self.check_cloudlinux_license()
      imunify_installed = self.check_imunify360_installation()

      # Si ambos están activos, no hay nada que hacer
      if cloudlinux_active and imunify_installed:
          print("\n✓ Todos los servicios ya están activados y licenciados.")
          return True

      # Solo pedimos las claves si es necesario
      if not self.set_license_keys():
          print("✗ Error: No se pudieron configurar las licencias necesarias.")
          return False

      # Instalar CloudLinux si no está activado
      if not cloudlinux_active and self.cloudlinux_key:
          if not self.install_cloudlinux_license():
              print("✗ Error: Falló la instalación de la licencia de CloudLinux")
              return False

      # Instalar Imunify360 si no está instalado
      if not imunify_installed and self.imunify360_key:
          if not self.install_imunify360():
              print("✗ Error: Falló la instalación de Imunify360")
              return False

      print("\n✓ Instalación completada con éxito")
      return True