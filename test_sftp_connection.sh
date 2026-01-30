#!/bin/bash

echo "========================================"
echo "Prueba de conexión SFTP manual"
echo "========================================"
echo ""
echo "Credenciales:"
echo "  Usuario: sftpuser"
echo "  Contraseña: sftppass123"
echo "  Puerto: 2222"
echo ""
echo "Conectando al servidor SFTP..."
echo ""
echo "Comandos útiles una vez conectado:"
echo "  ls          - Listar archivos"
echo "  pwd         - Directorio actual"
echo "  put file    - Subir archivo"
echo "  get file    - Descargar archivo"
echo "  exit        - Salir"
echo ""
echo "=========================================="
echo ""

sftp -P 2222 sftpuser@localhost
