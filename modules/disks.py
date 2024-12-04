import subprocess
import os
import json
from typing import Dict, List
from utils.discord_notifier import DiscordNotifier

class DiskManager:
    # Constantes específicas para la configuración de EC2
    ROOT_SIZE = 120 * 1024**3  # 120GB - disco del sistema
    HOME_MIN_SIZE = 900 * 1024**3  # ~1TB - disco principal para /home
    MNT_SIZE_RANGE = (90 * 1024**3, 110 * 1024**3)  # 90GB-110GB para /mnt

    def __init__(self, notifier: DiscordNotifier):
        self.notifier = notifier

    def get_disk_info(self) -> Dict[str, Dict]:
        """
        Obtiene información detallada de todos los discos en el sistema.
        Incluye discos montados para validación de seguridad.
        """
        try:
            result = subprocess.run(
                ['lsblk', '-J', '-o', 'NAME,KNAME,TYPE,SIZE,MOUNTPOINT,MODEL'],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            self._handle_error(f"Error obteniendo información de discos: {str(e)}")
            return {}

    def verify_mounts(self) -> Dict[str, bool]:
        """
        Verifica el estado actual de los puntos de montaje.
        
        Returns:
            Dict con el estado de los montajes {'/home': bool, '/mnt': bool}
        """
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True, check=True)
            mount_status = {
                '/home': False,
                '/mnt': False
            }
            
            for line in result.stdout.splitlines():
                if '/home' in line:
                    mount_status['/home'] = True
                if '/mnt' in line:
                    mount_status['/mnt'] = True
                    
            return mount_status
        except Exception as e:
            self._handle_error(f"Error verificando montajes: {str(e)}")
            return {'/home': False, '/mnt': False}

    def is_safe_to_proceed(self, disk_info: Dict) -> bool:
        """
        Verifica si es seguro proceder con las operaciones de montaje.
        """
        try:
            # Verificar que el disco root está presente y montado
            root_found = False
            for device in disk_info.get('blockdevices', []):
                if (device.get('type') == 'disk' and 
                    abs(self.size_to_bytes(device.get('size', '0')) - self.ROOT_SIZE) < 5 * 1024**3):  # 5GB margen
                    root_found = True
                    break

            if not root_found:
                self._handle_error("No se encontró el disco root. Abortando por seguridad.")
                return False

            return True
        except Exception as e:
            self._handle_error(f"Error en verificación de seguridad: {str(e)}")
            return False

    def get_available_disks(self, disk_info: Dict) -> Dict[str, Dict]:
        """
        Identifica los discos disponibles excluyendo el disco root y los ya montados.
        """
        available_disks = {}
        
        for device in disk_info.get('blockdevices', []):
            size_bytes = self.size_to_bytes(device.get('size', '0'))
            
            # Ignorar el disco root y sus particiones
            if abs(size_bytes - self.ROOT_SIZE) < 5 * 1024**3:
                continue

            # Ignorar discos ya montados en puntos críticos
            if device.get('mountpoint') in ['/', '/boot']:
                continue

            if device['type'] == 'disk':
                device_path = f"/dev/{device['kname']}"
                available_disks[device_path] = {
                    'size': size_bytes,
                    'name': device['kname'],
                    'model': device.get('model', 'Unknown'),
                    'current_mount': device.get('mountpoint')
                }

        return available_disks

    def size_to_bytes(self, size_str: str) -> float:
        """
        Convierte una cadena de tamaño (ej: '1G', '2T') a bytes.
        """
        units = {
            'B': 1,
            'K': 1024,
            'M': 1024 ** 2,
            'G': 1024 ** 3,
            'T': 1024 ** 4,
            'P': 1024 ** 5,
            'E': 1024 ** 6
        }
        
        size_str = size_str.upper()
        if size_str[-1] in units:
            return float(size_str[:-1]) * units[size_str[-1]]
        return float(size_str)

    def _format_size(self, size_bytes: float) -> str:
        """
        Convierte bytes a formato legible por humanos.
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}PB"

    def mount_disk(self, device: str, mount_point: str, filesystem: str = "ext4"):
        """
        Monta un disco específico en el punto de montaje indicado.
        """
        try:
            # Crear punto de montaje si no existe
            if not os.path.exists(mount_point):
                print(f"Creando directorio de montaje {mount_point}")
                os.makedirs(mount_point)

            # Verificar sistema de archivos existente
            print(f"Verificando sistema de archivos en {device}")
            result = subprocess.run(["blkid", device], capture_output=True, text=True)
            
            # Formatear solo si no tiene sistema de archivos
            if not result.stdout:
                print(f"Formateando {device} como {filesystem}")
                subprocess.run(
                    ["mkfs", "-t", filesystem, device],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            # Montar el dispositivo
            print(f"Montando {device} en {mount_point}")
            subprocess.run(["mount", device, mount_point], check=True)
            
            # Configurar montaje automático
            self.configure_fstab(device, mount_point, filesystem)
            
            self.notifier.notify_success(f"Disco {device} montado exitosamente en {mount_point}")
            
        except Exception as e:
            self._handle_error(f"Error montando {device} en {mount_point}: {str(e)}")

    def configure_fstab(self, device: str, mount_point: str, filesystem: str):
        """
        Configura el montaje automático en /etc/fstab usando UUID.
        """
        try:
            # Obtener UUID del dispositivo
            result = subprocess.run(
                ["blkid", "-s", "UUID", "-o", "value", device],
                capture_output=True,
                text=True,
                check=True
            )
            uuid = result.stdout.strip()

            if not uuid:
                raise ValueError(f"No se pudo obtener UUID para {device}")

            # Verificar entrada existente
            with open("/etc/fstab", "r") as f:
                if any(uuid in line or mount_point in line for line in f):
                    print(f"Entrada para {device} ya existe en fstab")
                    return

            # Agregar nueva entrada
            with open("/etc/fstab", "a") as f:
                f.write(f"\nUUID={uuid} {mount_point} {filesystem} defaults,nofail 0 2\n")

            print(f"Configuración de fstab actualizada para {device}")
            
        except Exception as e:
            self._handle_error(f"Error configurando fstab para {device}: {str(e)}")

    def mount_disks(self):
        """
        Proceso principal de montaje de discos con verificaciones de seguridad.
        """
        print("Iniciando proceso de verificación y montaje de discos...")
        
        # Verificar montajes actuales
        current_mounts = self.verify_mounts()
        print(f"Estado actual de montajes: /home: {'montado' if current_mounts['/home'] else 'no montado'}, "
              f"/mnt: {'montado' if current_mounts['/mnt'] else 'no montado'}")
        
        # Obtener información completa de discos
        disk_info = self.get_disk_info()
        if not disk_info:
            return

        # Verificar seguridad
        if not self.is_safe_to_proceed(disk_info):
            return

        # Obtener discos disponibles
        available_disks = self.get_available_disks(disk_info)
        
        # Identificar y montar discos
        home_mounted = current_mounts['/home']
        mnt_mounted = current_mounts['/mnt']
        
        for device_path, info in available_disks.items():
            size = info['size']
            current_mount = info['current_mount']

            # Verificar disco grande para /home
            if size >= self.HOME_MIN_SIZE and not home_mounted:
                self.mount_disk(device_path, '/home')
                print(f"Disco grande ({self._format_size(size)}) montado en /home")
                home_mounted = True
                
            # Verificar disco mediano para /mnt
            elif (self.MNT_SIZE_RANGE[0] <= size <= self.MNT_SIZE_RANGE[1] and 
                  not mnt_mounted):
                self.mount_disk(device_path, '/mnt')
                print(f"Disco mediano ({self._format_size(size)}) montado en /mnt")
                mnt_mounted = True

        # Verificación final
        final_mounts = self.verify_mounts()
        if not final_mounts['/home'] or not final_mounts['/mnt']:
            self._handle_error("No se pudieron montar todos los discos requeridos:\n"
                             f"/home: {'montado' if final_mounts['/home'] else 'no montado'}\n"
                             f"/mnt: {'montado' if final_mounts['/mnt'] else 'no montado'}")
            return
            
        # Recargar systemd después de modificar fstab
        try:
            subprocess.run(['systemctl', 'daemon-reload'], check=True)
            print("systemd reloaded correctamente")
        except Exception as e:
            self._handle_error(f"Error al recargar systemd: {str(e)}")

    def _handle_error(self, message: str):
        """
        Manejo centralizado de errores con notificación.
        """
        print(f"ERROR: {message}")
        self.notifier.notify_error(message)