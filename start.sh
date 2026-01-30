#!/bin/bash

echo "========================================"
echo "Iniciando aplicación SFTP + Celery"
echo "========================================"

# Verificar que existe .env
if [ ! -f .env ]; then
    echo "❌ Error: Archivo .env no encontrado"
    exit 1
fi

echo "✓ Archivo .env encontrado"

# Construir y levantar contenedores
echo ""
echo "Construyendo contenedores..."
docker compose build

echo ""
echo "Iniciando servicios..."
docker compose up -d

echo ""
echo "Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado de los contenedores
echo ""
echo "Estado de los contenedores:"
docker compose ps

echo ""
echo "========================================"
echo "✓ Aplicación iniciada exitosamente"
echo "========================================"
echo ""
echo "Servicios disponibles:"
echo "  - SFTP Server: localhost:2222"
echo "  - Redis: localhost:6379"
echo "  - Flower (Monitor): http://localhost:5555"
echo ""
echo "Comandos útiles:"
echo "  - Ver logs: docker compose logs -f"
echo "  - Detener: docker compose down"
echo "  - Reiniciar: docker compose restart"
echo ""
