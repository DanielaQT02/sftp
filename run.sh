#!/bin/bash

# Script para levantar la aplicación SFTP + Celery + Redis

echo "🚀 Iniciando aplicación..."

# Verificar que Docker está disponible
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Verificar que Docker Compose está disponible
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

# Crear directorio de datos si no existe
mkdir -p sftp_data

# Levantar los servicios
docker-compose up -d

# Verificar que los servicios se levantaron correctamente
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Aplicación levantada exitosamente!"
    echo ""
    echo "📍 Servicios disponibles:"
    echo "   • SFTP Server:     sftp://localhost:2222"
    echo "   • Flower Dashboard: http://localhost:5555"
    echo "   • Redis:           localhost:6379"
    echo ""
    echo "📌 Comandos útiles:"
    echo "   • Ver logs:        docker-compose logs -f"
    echo "   • Detener:         docker-compose down"
    echo "   • Estado:          docker-compose ps"
    echo ""
else
    echo "❌ Error al levantar la aplicación"
    exit 1
fi
