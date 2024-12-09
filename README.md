# cPanelTools
## Script de Automatización para Servidores CloudLinux

### Descripción
Este script proporciona una suite completa de herramientas para la gestión y automatización de servidores CloudLinux, diseñado para ser desplegado en la raíz del sistema (`/`).

### Requisitos Previos
- Sistema operativo CloudLinux
- Python 3.6 o superior
- Permisos de root

### Módulos y Funcionalidades

#### Gestión de Panel
- **cpanel.py**: Administración de cPanel
  - Instalación y configuración básica de cPanel

#### Seguridad
- **csf.py**: ConfigServer Firewall
  - Instalación de CSF interno
  - Configuración de firewall automatizada por plantilla

- **licenses.py**: Gestión de Licencias
  - Instalación de licencia CloudLinux
  - Instalación de licencia Imunify360
  - Automatización de activación

#### Optimización y Rendimiento
- **litespeed.py**: Gestión de LiteSpeed
  - Instalación y configuración
  - Optimización de rendimiento

- **easyapache_manager.py**: Gestión de EasyApache
  - Aplicar configuración de EasyApache predeterminada para cPanel por medio de CLI
  
#### Backup y Almacenamiento
- **jetbackup.py**: Sistema de Respaldo
  - Instalación de Jetbackup sin configuración nativa.
    

- **disks.py**: Gestión de Discos
  - Particiona dos discos,  /home y /mnt para cPanel
    
#### Utilidades
- **cron_manager.py**: Gestor de Tareas Programadas
  - Automatiza ciertos CronJobs y los eleva a crontab para que sean ejecutados según sean agregados en el .txt


- **ftp.py**: Gestión FTP
  - Asignar Pure-Ftpd como predeterminado para cPanel
  - Configura una regla de puertos específicos, Bind y PassivePorts

- **softaculous.py**: Instalador de Aplicaciones
  - Activa IonCube y instala Softacolus

#### Sistema
- **os_manager.py**: Gestión del Sistema Operativo
  - Actualizaciones del sistema
  - Optimización de recursos

### Utilidades de Soporte
- **discord_notifier.py**: Notificaciones
  - Alertas en tiempo real
  - Reportes de estado

- **helpers.py**: Funciones Auxiliares
  - Utilidades comunes
  - Funciones de ayuda

### Instalación
```bash
cd /
git clone [URL_DEL_REPOSITORIO]
python3 main.py

Uso
Ejecute el script principal como root:
Copiar
python3 main.py
Siga las instrucciones en pantalla para:
Configurar licencias
Gestionar servicios
Automatizar tareas
Monitorear el sistema
Notas Importantes
Ejecutar siempre como usuario root
Realizar backup antes de modificaciones importantes
Verificar compatibilidad con la versión de CloudLinux

Licencia
Este software está protegido bajo términos de licencia propietaria.
