#!/bin/bash

echo "========================================"
echo "Deteniendo aplicación SFTP + Celery"
echo "========================================"

docker compose down

echo ""
echo "✓ Aplicación detenida"
echo ""
echo "Para eliminar los volúmenes también:"
echo "  docker compose down -v"
echo ""
