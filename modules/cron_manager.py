import subprocess
import os
from utils.discord_notifier import DiscordNotifier

class CronManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier
        self.cron_config_path = "/deploy_cPanelTools/config/cronjobs/Cron.txt"
        self.system_crontab = "/var/spool/cron/root"

    def backup_current_crontab(self):
        """
        Crea un backup del crontab actual
        """
        try:
            backup_path = f"{self.system_crontab}.bak"
            if os.path.exists(self.system_crontab):
                subprocess.run(["cp", "-f", self.system_crontab, backup_path], check=True)
                print(f"Backup del crontab creado en {backup_path}")
            return True
        except Exception as e:
            print(f"Error creando backup del crontab: {str(e)}")
            return False

    def add_cronjobs(self):  # Cambiado de import_cronjobs a add_cronjobs
        """
        Importa los cronjobs desde el archivo de configuración
        """
        try:
            print("Importando cronjobs...")

            # Verificar si existe el archivo de configuración
            if not os.path.exists(self.cron_config_path):
                raise FileNotFoundError(f"Archivo de configuración no encontrado: {self.cron_config_path}")

            # Crear backup del crontab actual
            self.backup_current_crontab()

            # Leer los nuevos cronjobs
            with open(self.cron_config_path, 'r') as f:
                new_crontab = f.read().strip()

            # Agregar header al crontab
            crontab_content = (
                "# /etc/crontab: system-wide crontab\n"
                "# Archivo gestionado automáticamente - NO EDITAR MANUALMENTE\n"
                "SHELL=/bin/bash\n"
                "PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n\n"
                f"{new_crontab}\n"
            )

            # Escribir al archivo temporal
            temp_cron = "/tmp/new_crontab"
            with open(temp_cron, 'w') as f:
                f.write(crontab_content)

            # Instalar el nuevo crontab
            subprocess.run(["crontab", "-u", "root", temp_cron], check=True)

            # Limpiar archivo temporal
            if os.path.exists(temp_cron):
                os.remove(temp_cron)

            # Reiniciar el servicio de cron
            subprocess.run(["systemctl", "restart", "crond"], check=True)

            print("Cronjobs importados correctamente")
            self.notifier.notify_success("Cronjobs importados correctamente")
            return True

        except Exception as e:
            error_msg = f"Error importando cronjobs: {str(e)}"
            print(error_msg)
            self.notifier.notify_error(error_msg)
            return False

    def verify_cronjobs(self):
        """
        Verifica que los cronjobs se hayan importado correctamente
        """
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
            print("Cronjobs actuales:")
            print(result.stdout)
            return True
        except Exception as e:
            print(f"Error verificando cronjobs: {str(e)}")
            return False