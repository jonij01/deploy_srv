# Panel Manager para CloudLinux
## Script de Automatización para Servidores CloudLinux

### Descripción
Este script proporciona una suite completa de herramientas para la gestión y automatización de servidores CloudLinux, diseñado para ser desplegado en la raíz del sistema (`/`).

### Requisitos Previos
- Sistema operativo CloudLinux
- Python 3.6 o superior
- Permisos de root
- Conexión a internet

### Módulos y Funcionalidades

#### Gestión de Panel
- **cpanel.py**: Administración de cPanel
  - Instalación y configuración
  - Gestión de licencias
  - Automatización de tareas comunes

#### Seguridad
- **csf.py**: ConfigServer Firewall
  - Configuración de firewall
  - Gestión de reglas
  - Monitoreo de seguridad

- **licenses.py**: Gestión de Licencias
  - CloudLinux
  - Imunify360
  - Automatización de activación

#### Optimización y Rendimiento
- **litespeed.py**: Gestión de LiteSpeed
  - Instalación y configuración
  - Optimización de rendimiento

- **easyapache_manager.py**: Gestión de EasyApache
  - Configuración de PHP
  - Gestión de módulos Apache

#### Backup y Almacenamiento
- **jetbackup.py**: Sistema de Respaldo
  - Configuración de copias de seguridad
  - Programación de backups

- **disks.py**: Gestión de Discos
  - Monitoreo de espacio
  - Gestión de particiones

#### Utilidades
- **cron_manager.py**: Gestor de Tareas Programadas
  - Creación y gestión de cronjobs
  - Automatización de tareas

- **ftp.py**: Gestión FTP
  - Configuración de servicios FTP
  - Gestión de usuarios

- **softaculous.py**: Instalador de Aplicaciones
  - Gestión de instalaciones automáticas
  - Actualizaciones de scripts

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
cd panel-manager
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
Soporte
Para reportar problemas o solicitar ayuda:

Abrir un issue en el repositorio
Contactar al equipo de soporte
Licencia
Este software está protegido bajo términos de licencia propietaria.
