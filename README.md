# Aplicación SFTP + Celery con Docker

Aplicación completa que simula un servidor SFTP con gestión de tareas asíncronas usando Celery y Redis.

## 🏗️ Arquitectura

- **SFTP Server**: Servidor SFTP basado en atmoz/sftp
- **Celery Worker**: Workers para procesar tareas asíncronas
- **Redis**: Broker de mensajes para Celery
- **Flower**: Monitor web para las tareas de Celery

## 📋 Requisitos

- Docker
- Docker Compose
- 4GB RAM mínimo

## 🚀 Inicio Rápido

### 1. Iniciar la aplicación

```bash
./start.sh
```

Este script:
- Construye las imágenes Docker
- Levanta todos los servicios
- Verifica que estén funcionando

### 2. Ejecutar ejemplos

```bash
./run_examples.sh
```

Este script ejecuta ejemplos de:
- Subir archivos al SFTP
- Descargar archivos del SFTP
- Listar archivos
- Batch upload de múltiples archivos

### 3. Detener la aplicación

```bash
./stop.sh
```

### 4. Probar conexión SFTP manual

```bash
./test_sftp_connection.sh
```

## 📂 Estructura del Proyecto

```
sftp/
├── app/
│   ├── celery_config.py      # Configuración de Celery
│   ├── tasks.py               # Definición de tareas
│   ├── example_usage.py       # Script de ejemplos
│   └── requirements.txt       # Dependencias Python
├── sftp_data/                 # Datos del servidor SFTP
├── sftp_users/
│   └── users.conf            # Configuración de usuarios SFTP
├── docker-compose.yml        # Orquestación de servicios
├── Dockerfile.celery         # Imagen para Celery
├── Dockerfile.sftp           # Imagen para SFTP
├── .env                      # Variables de entorno
├── start.sh                  # Script de inicio
├── run_examples.sh           # Script de ejemplos
├── test_sftp_connection.sh   # Script para probar SFTP
└── stop.sh                   # Script de parada
```

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Usuario SFTP
SFTP_USER=sftpuser
SFTP_PASS=sftppass123

# Puertos
SFTP_PORT=2222
```

### Puertos Expuestos

- **2222**: Servidor SFTP
- **6379**: Redis
- **5555**: Flower (Monitor)

## 📝 Tareas Disponibles

### 1. Upload File
```python
celery_app.send_task('tasks.upload_file', 
    args=['/local/path/file.txt', '/upload/file.txt'])
```

### 2. Download File
```python
celery_app.send_task('tasks.download_file',
    args=['/upload/file.txt', '/local/path/file.txt'])
```

### 3. List Files
```python
celery_app.send_task('tasks.list_files',
    args=['/upload'])
```

### 4. Delete File
```python
celery_app.send_task('tasks.delete_file',
    args=['/upload/file.txt'])
```

### 5. Batch Upload
```python
files = [
    ('/local/file1.txt', '/upload/file1.txt'),
    ('/local/file2.txt', '/upload/file2.txt')
]
celery_app.send_task('tasks.process_batch_upload',
    args=[files])
```

## 🔍 Monitoreo

### Flower UI
Accede a [http://localhost:5555](http://localhost:5555) para monitorear:
- Tareas activas
- Tareas completadas
- Workers disponibles
- Estadísticas en tiempo real

### Logs
```bash
# Ver logs de todos los servicios
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs -f celery-worker
docker compose logs -f sftp-server
docker compose logs -f flower
```

## 🧪 Pruebas Manuales

### Conectarse al SFTP manualmente
```bash
sftp -P 2222 sftpuser@localhost
# Contraseña: sftppass123
```

### Ejecutar tareas manualmente desde el contenedor
```bash
# Entrar al contenedor
docker compose exec celery-worker bash

# Ejecutar Python interactivo
python

# Enviar tarea
from celery_config import celery_app
task = celery_app.send_task('tasks.list_files', args=['/upload'])
print(task.id)
```

## 🔄 Comandos Útiles

```bash
# Reiniciar un servicio específico
docker compose restart celery-worker

# Ver estado de los contenedores
docker compose ps

# Reconstruir contenedores
docker compose build --no-cache

# Limpiar todo (incluyendo volúmenes)
docker compose down -v

# Escalar workers
docker compose up -d --scale celery-worker=3
```

## 🛠️ Desarrollo

### Agregar nuevas tareas

1. Edita [app/tasks.py](app/tasks.py)
2. Define tu nueva tarea:
```python
@celery_app.task(name='tasks.mi_nueva_tarea')
def mi_nueva_tarea(parametro):
    # Tu código aquí
    return {'status': 'success'}
```
3. Reinicia el worker:
```bash
docker compose restart celery-worker
```

### Cambiar configuración de Celery

Edita [app/celery_config.py](app/celery_config.py) y reinicia los servicios.

## 🐛 Solución de Problemas

### El servidor SFTP no inicia
- Verifica que el puerto 2222 esté libre
- Revisa los logs: `docker compose logs sftp-server`

### Celery no procesa tareas
- Verifica que Redis esté corriendo: `docker compose ps redis`
- Revisa conexión: `docker compose exec redis redis-cli ping`
- Revisa logs del worker: `docker compose logs celery-worker`

### Error de conexión SFTP desde Celery
- Verifica que todos los contenedores estén en la misma red
- Usa `sftp-server` como hostname (no `localhost`)
- Verifica credenciales en `.env`

## 📚 Recursos

- [Celery Documentation](https://docs.celeryq.dev/)
- [Paramiko Documentation](http://docs.paramiko.org/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [atmoz/sftp Docker Image](https://github.com/atmoz/sftp)

## 📄 Licencia

MIT License

## 👥 Autor

Proyecto creado para demostración de SFTP + Celery
