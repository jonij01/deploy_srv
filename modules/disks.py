import subprocess
from utils.discord_notifier import DiscordNotifier

class DiskManager:
    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def mount_disk(self, device: str, mount_point: str):
        """
        Monta un disco en el sistema.
        """
        try:
            print(f"Montando el disco {device} en {mount_point}...")
            subprocess.run(["mount", device, mount_point], check=True)
            print(f"Disco {device} montado correctamente en {mount_point}.")
            self.notifier.notify_success(f"Disco {device} montado correctamente en {mount_point}.")
        except subprocess.CalledProcessError as e:
            print(f"Error al montar el disco {device}: {str(e)}")
            self.notifier.notify_error(f"Error al montar el disco {device}: {str(e)}")

    def configure_fstab(self, device: str, mount_point: str, filesystem: str):
        """
        Agrega una configuración en /etc/fstab para el montaje automático.
        """
        try:
            print(f"Configurando /etc/fstab para {device}...")
            with open("/etc/fstab", "a") as fstab:
                fstab.write(f"{device} {mount_point} {filesystem} defaults 0 0\n")
            print(f"Configuración de /etc/fstab actualizada para {device}.")
            self.notifier.notify_success(f"Configuración de /etc/fstab actualizada para {device}.")
        except Exception as e:
            print(f"Error al configurar /etc/fstab: {str(e)}")
            self.notifier.notify_error(f"Error al configurar /etc/fstab: {str(e)}")