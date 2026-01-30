import os
import paramiko
import logging
from celery_config import celery_app
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración SFTP
SFTP_HOST = os.getenv('SFTP_HOST', 'sftp-server')
SFTP_PORT = int(os.getenv('SFTP_PORT', '22'))
SFTP_USER = os.getenv('SFTP_USER', 'sftpuser')
SFTP_PASS = os.getenv('SFTP_PASS', 'sftppass123')


def get_sftp_connection():
    """Crear conexión SFTP"""
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport
    except Exception as e:
        logger.error(f"Error al conectar con SFTP: {e}")
        raise


@celery_app.task(name='tasks.upload_file')
def upload_file(local_path, remote_path):
    """
    Tarea para subir un archivo al servidor SFTP
    
    Args:
        local_path: Ruta local del archivo
        remote_path: Ruta remota donde se guardará
    """
    logger.info(f"Iniciando upload de {local_path} a {remote_path}")
    
    try:
        sftp, transport = get_sftp_connection()
        
        # Subir archivo
        sftp.put(local_path, remote_path)
        logger.info(f"Archivo subido exitosamente: {remote_path}")
        
        # Cerrar conexión
        sftp.close()
        transport.close()
        
        return {
            'status': 'success',
            'message': f'Archivo subido: {remote_path}',
            'local_path': local_path,
            'remote_path': remote_path
        }
    except Exception as e:
        logger.error(f"Error al subir archivo: {e}")
        return {
            'status': 'error',
            'message': str(e),
            'local_path': local_path,
            'remote_path': remote_path
        }


@celery_app.task(name='tasks.download_file')
def download_file(remote_path, local_path):
    """
    Tarea para descargar un archivo del servidor SFTP
    
    Args:
        remote_path: Ruta remota del archivo
        local_path: Ruta local donde se guardará
    """
    logger.info(f"Iniciando download de {remote_path} a {local_path}")
    
    try:
        sftp, transport = get_sftp_connection()
        
        # Descargar archivo
        sftp.get(remote_path, local_path)
        logger.info(f"Archivo descargado exitosamente: {local_path}")
        
        # Cerrar conexión
        sftp.close()
        transport.close()
        
        return {
            'status': 'success',
            'message': f'Archivo descargado: {local_path}',
            'remote_path': remote_path,
            'local_path': local_path
        }
    except Exception as e:
        logger.error(f"Error al descargar archivo: {e}")
        return {
            'status': 'error',
            'message': str(e),
            'remote_path': remote_path,
            'local_path': local_path
        }


@celery_app.task(name='tasks.list_files')
def list_files(remote_dir='/upload'):
    """
    Tarea para listar archivos en el servidor SFTP
    
    Args:
        remote_dir: Directorio remoto a listar
    """
    logger.info(f"Listando archivos en {remote_dir}")
    
    try:
        sftp, transport = get_sftp_connection()
        
        # Listar archivos
        files = sftp.listdir(remote_dir)
        logger.info(f"Se encontraron {len(files)} archivos")
        
        # Cerrar conexión
        sftp.close()
        transport.close()
        
        return {
            'status': 'success',
            'directory': remote_dir,
            'files': files,
            'count': len(files)
        }
    except Exception as e:
        logger.error(f"Error al listar archivos: {e}")
        return {
            'status': 'error',
            'message': str(e),
            'directory': remote_dir
        }


@celery_app.task(name='tasks.delete_file')
def delete_file(remote_path):
    """
    Tarea para eliminar un archivo del servidor SFTP
    
    Args:
        remote_path: Ruta remota del archivo a eliminar
    """
    logger.info(f"Eliminando archivo {remote_path}")
    
    try:
        sftp, transport = get_sftp_connection()
        
        # Eliminar archivo
        sftp.remove(remote_path)
        logger.info(f"Archivo eliminado exitosamente: {remote_path}")
        
        # Cerrar conexión
        sftp.close()
        transport.close()
        
        return {
            'status': 'success',
            'message': f'Archivo eliminado: {remote_path}',
            'remote_path': remote_path
        }
    except Exception as e:
        logger.error(f"Error al eliminar archivo: {e}")
        return {
            'status': 'error',
            'message': str(e),
            'remote_path': remote_path
        }


@celery_app.task(name='tasks.process_batch_upload')
def process_batch_upload(file_list):
    """
    Tarea para procesar múltiples uploads
    
    Args:
        file_list: Lista de tuplas (local_path, remote_path)
    """
    logger.info(f"Procesando batch upload de {len(file_list)} archivos")
    
    results = []
    for local_path, remote_path in file_list:
        result = upload_file.delay(local_path, remote_path)
        results.append({
            'task_id': result.id,
            'local_path': local_path,
            'remote_path': remote_path
        })
    
    return {
        'status': 'success',
        'message': f'Batch upload iniciado con {len(results)} tareas',
        'tasks': results
    }


@celery_app.task(name='tasks.get_file_info')
def get_file_info(remote_path):
    """Obtener información detallada de un archivo"""
    logger.info(f"Obteniendo info de {remote_path}")
    
    try:
        sftp, transport = get_sftp_connection()
        attrs = sftp.stat(remote_path)
        sftp.close()
        transport.close()
        
        return {
            'status': 'success',
            'path': remote_path,
            'size': attrs.st_size,
            'modified': attrs.st_mtime,
            'permissions': oct(attrs.st_mode)
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {'status': 'error', 'message': str(e)}
