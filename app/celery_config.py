import os
from celery import Celery
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Redis
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', '6379')
redis_db = os.getenv('REDIS_DB', '0')

# Crear instancia de Celery
celery_app = Celery(
    'sftp_tasks',
    broker=f'redis://{redis_host}:{redis_port}/{redis_db}',
    backend=f'redis://{redis_host}:{redis_port}/{redis_db}',
    include=['tasks']
)

# Configuración de Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Mexico_City',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

if __name__ == '__main__':
    celery_app.start()
