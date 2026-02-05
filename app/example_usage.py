#!/usr/bin/env python3
"""
Script de ejemplo para interactuar con las tareas de Celery
"""
import os
import time
from celery_config import celery_app

def print_separator():
    print("\n" + "="*60 + "\n")

def check_task_status(task_id):
    """Verificar el estado de una tarea"""
    result = celery_app.AsyncResult(task_id)
    return {
        'task_id': task_id,
        'status': result.status,
        'result': result.result if result.ready() else None
    }

def wait_for_task(task_id, timeout=30):
    """Esperar a que una tarea se complete"""
    result = celery_app.AsyncResult(task_id)
    print(f"Esperando a que la tarea {task_id} se complete...")
    
    start_time = time.time()
    while not result.ready() and (time.time() - start_time) < timeout:
        time.sleep(1)
        print(".", end="", flush=True)
    
    print()
    
    if result.ready():
        return result.result
    else:
        return {"status": "timeout", "message": "La tarea excedió el tiempo de espera"}

# Ejemplo 1: Crear un archivo de prueba y subirlo
print_separator()
print("EJEMPLO 1: Subir archivo al SFTP")
print_separator()

# Crear un archivo de prueba
test_file = "/sftp_data/test_file.txt"
with open(test_file, 'w') as f:
    f.write("Este es un archivo de prueba para SFTP\n")
    f.write(f"Creado en: {time.ctime()}\n")

print(f"✓ Archivo de prueba creado: {test_file}")

# Enviar tarea para subir archivo
task = celery_app.send_task(
    'tasks.upload_file',
    args=[test_file, '/upload/test_file.txt']
)
print(f"✓ Tarea de upload enviada. ID: {task.id}")

# Esperar resultado
result = wait_for_task(task.id)
print(f"✓ Resultado: {result}")

# Ejemplo 2: Listar archivos en el servidor SFTP
print_separator()
print("EJEMPLO 2: Listar archivos en SFTP")
print_separator()

time.sleep(2)  # Esperar un momento

task = celery_app.send_task('tasks.list_files', args=['/upload'])
print(f"✓ Tarea de listado enviada. ID: {task.id}")

result = wait_for_task(task.id)
print(f"✓ Resultado: {result}")

# Ejemplo 3: Descargar archivo
print_separator()
print("EJEMPLO 3: Descargar archivo desde SFTP")
print_separator()

time.sleep(2)

download_path = "/sftp_data/downloaded_file.txt"
task = celery_app.send_task(
    'tasks.download_file',
    args=['/upload/test_file.txt', download_path]
)
print(f"✓ Tarea de download enviada. ID: {task.id}")

result = wait_for_task(task.id)
print(f"✓ Resultado: {result}")

# Verificar si el archivo se descargó
if os.path.exists(download_path):
    print(f"✓ Archivo descargado exitosamente")
    with open(download_path, 'r') as f:
        print("Contenido:")
        print(f.read())

# Ejemplo 4: Subir múltiples archivos (batch)
# Los archivos se ubican en /sftp_data que está sincronizado con el servidor SFTP
print_separator()
print("EJEMPLO 4: Batch upload de múltiples archivos")
print_separator()

# Crear varios archivos de prueba
files_to_upload = []
for i in range(3):
    filename = f"/sftp_data/batch_file_{i}.txt"
    with open(filename, 'w') as f:
        f.write(f"Archivo batch número {i}\n")
    files_to_upload.append((filename, f'/upload/batch_file_{i}.txt'))
    print(f"✓ Creado: {filename}")

# Enviar batch
task = celery_app.send_task('tasks.process_batch_upload', args=[files_to_upload])
print(f"\n✓ Tarea de batch upload enviada. ID: {task.id}")

result = wait_for_task(task.id)
print(f"✓ Resultado: {result}")

# Ejemplo 5: Listar archivos nuevamente
print_separator()
print("EJEMPLO 5: Listar todos los archivos")
print_separator()

time.sleep(3)  # Dar tiempo a que se completen los uploads

task = celery_app.send_task('tasks.list_files', args=['/upload'])
result = wait_for_task(task.id)
print(f"✓ Resultado: {result}")

print_separator()
print("✓ Ejemplos completados!")
print("Puedes monitorear las tareas en Flower: http://localhost:5555")
print_separator()
