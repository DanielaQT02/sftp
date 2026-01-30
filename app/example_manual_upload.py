#!/usr/bin/env python3
import paramiko
import os

# Configuración
SFTP_HOST = 'localhost'
SFTP_PORT = 2222
SFTP_USER = 'sftpuser'
SFTP_PASS = 'sftppass123'

def upload_file_manual(local_file, remote_file):
    """
    Subir un archivo al SFTP de forma manual (sin Celery)
    """
    print(f"Conectando a {SFTP_HOST}:{SFTP_PORT}...")
    
    # Crear transporte SSH
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    
    # Crear cliente SFTP
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    print(f"Subiendo {local_file} -> {remote_file}")
    sftp.put(local_file, remote_file)
    
    print("✓ Archivo subido exitosamente!")
    
    # Listar archivos
    print("\nArchivos en /upload:")
    files = sftp.listdir('/upload')
    for f in files:
        print(f"  - {f}")
    
    # Cerrar conexión
    sftp.close()
    transport.close()

def download_file_manual(remote_file, local_file):
    """
    Descargar un archivo del SFTP
    """
    print(f"Conectando a {SFTP_HOST}:{SFTP_PORT}...")
    
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    print(f"Descargando {remote_file} -> {local_file}")
    sftp.get(remote_file, local_file)
    
    print("✓ Archivo descargado exitosamente!")
    
    sftp.close()
    transport.close()

if __name__ == '__main__':
    print("="*60)
    print("Ejemplo de Upload Manual al SFTP")
    print("="*60)
    print()
    
    # Crear un archivo de prueba
    test_file = '/tmp/manual_upload_test.txt'
    with open(test_file, 'w') as f:
        f.write("Este archivo fue subido manualmente\n")
        f.write("Sin usar Celery, solo Python + Paramiko\n")
    
    print(f"✓ Archivo creado: {test_file}")
    
    # Subir el archivo
    try:
        upload_file_manual(test_file, '/upload/manual_upload_test.txt')
        
        # Descargar el archivo
        download_file_manual('/upload/manual_upload_test.txt', '/tmp/downloaded_test.txt')
        
        # Mostrar contenido descargado
        print("\nContenido del archivo descargado:")
        with open('/tmp/downloaded_test.txt', 'r') as f:
            print(f.read())
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("="*60)
