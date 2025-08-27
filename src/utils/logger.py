"""
Configuración centralizada de logging con loguru
"""

import sys
import os
from pathlib import Path
from loguru import logger

# Crear directorio de logs si no existe
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configurar loguru
def setup_logger():
    """Configura loguru para todo el proyecto"""
    
    # Remover el logger por defecto
    logger.remove()
    
    # Configurar formato para consola
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # Configurar archivo de logs general
    logger.add(
        "logs/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Configurar archivo de logs de errores
    logger.add(
        "logs/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="5 MB",
        retention="60 days",
        compression="zip"
    )
    
    # Configurar archivo de logs de Discord
    logger.add(
        "logs/discord.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        filter=lambda record: "discord" in record["name"].lower() or "interaction" in record["message"].lower()
    )
    
    # Configurar archivo de logs de chat/IA
    logger.add(
        "logs/chat.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="5 MB",
        retention="30 days",
        compression="zip",
        filter=lambda record: "chat" in record["name"].lower() or "llm" in record["name"].lower() or "rag" in record["name"].lower()
    )

# Inicializar logger
setup_logger()

# Exportar logger configurado
__all__ = ["logger"]
