import subprocess
from utils.discord_notifier import DiscordNotifier

class CronManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def add_cronjob(self, cron_command: str, schedule: str):
        """
        Agrega un nuevo cronjob al sistema.
        """
        try:
            print(f"Agregando nuevo cronjob: {schedule} {cron_command}...")
            cron_entry = f"{schedule} {cron_command}\n"
            with open("/etc/crontab", "a") as crontab:
                crontab.write(cron_entry)
            subprocess.run(["systemctl", "restart", "crond"], check=True)
            print("Cronjob agregado correctamente.")
            self.notifier.notify_success("Cronjob agregado correctamente.")
        except Exception as e:
            print(f"Error al agregar el cronjob: {str(e)}")
            self.notifier.notify_error(f"Error al agregar el cronjob: {str(e)}")
