#!/bin/bash

echo "========================================"
echo "Ejecutando ejemplos de uso"
echo "========================================"

# Verificar que los contenedores estén corriendo
if [ "$(docker compose ps -q celery-worker)" = "" ]; then
    echo "❌ Error: Los contenedores no están corriendo"
    echo "Ejecuta primero: ./start.sh"
    exit 1
fi

echo "✓ Contenedores en ejecución"
echo ""
echo "Ejecutando script de ejemplos..."
echo ""

# Ejecutar el script de ejemplos dentro del contenedor
docker compose exec celery-worker python example_usage.py

echo ""
echo "========================================"
echo "✓ Ejemplos completados"
echo "========================================"
echo ""
echo "Revisa Flower para ver las tareas: http://localhost:5555"
echo ""
