"""
Configuraciones específicas para Discord y el sistema de ACK diferido
"""

import os
from typing import Dict, Any

class DiscordConfig:
    """Configuraciones para el bot de Discord"""
    
    # Configuraciones del sistema de ACK diferido
    ACK_DEFERRED_CONFIG = {
        "max_workers": int(os.getenv("DISCORD_MAX_WORKERS", "5")),
        "request_timeout": int(os.getenv("DISCORD_REQUEST_TIMEOUT", "30")),
        "max_retries": int(os.getenv("DISCORD_MAX_RETRIES", "3")),
        "retry_delays": [1, 2, 5, 10],  # Delays en segundos para cada reintento
        "queue_max_size": int(os.getenv("DISCORD_QUEUE_MAX_SIZE", "100")),
        "worker_health_check_interval": int(os.getenv("DISCORD_WORKER_HEALTH_CHECK", "60")),
    }
    
    # Configuraciones de rate limiting
    RATE_LIMIT_CONFIG = {
        "requests_per_minute": int(os.getenv("DISCORD_RATE_LIMIT_PER_MINUTE", "50")),
        "burst_limit": int(os.getenv("DISCORD_BURST_LIMIT", "10")),
        "cooldown_period": int(os.getenv("DISCORD_COOLDOWN_PERIOD", "60")),
    }
    
    # Configuraciones de logging
    LOGGING_CONFIG = {
        "log_interactions": os.getenv("DISCORD_LOG_INTERACTIONS", "true").lower() == "true",
        "log_response_times": os.getenv("DISCORD_LOG_RESPONSE_TIMES", "true").lower() == "true",
        "log_errors": os.getenv("DISCORD_LOG_ERRORS", "true").lower() == "true",
        "log_retries": os.getenv("DISCORD_LOG_RETRIES", "true").lower() == "true",
    }
    
    # Configuraciones de métricas
    METRICS_CONFIG = {
        "enabled": os.getenv("DISCORD_METRICS_ENABLED", "true").lower() == "true",
        "retention_hours": int(os.getenv("DISCORD_METRICS_RETENTION_HOURS", "24")),
        "cleanup_interval_minutes": int(os.getenv("DISCORD_METRICS_CLEANUP_INTERVAL", "60")),
        "export_prometheus": os.getenv("DISCORD_EXPORT_PROMETHEUS", "true").lower() == "true",
    }
    
    # Configuraciones de seguridad
    SECURITY_CONFIG = {
        "verify_signatures": os.getenv("DISCORD_VERIFY_SIGNATURES", "true").lower() == "true",
        "max_request_size_mb": int(os.getenv("DISCORD_MAX_REQUEST_SIZE_MB", "10")),
        "allowed_origins": os.getenv("DISCORD_ALLOWED_ORIGINS", "discord.com,discordapp.com").split(","),
    }
    
    # Configuraciones de respuesta
    RESPONSE_CONFIG = {
        "default_timeout_seconds": int(os.getenv("DISCORD_DEFAULT_TIMEOUT", "25")),
        "max_response_length": int(os.getenv("DISCORD_MAX_RESPONSE_LENGTH", "2000")),
        "truncate_long_responses": os.getenv("DISCORD_TRUNCATE_RESPONSES", "true").lower() == "true",
        "add_timestamps": os.getenv("DISCORD_ADD_TIMESTAMPS", "false").lower() == "true",
    }
    
    @classmethod
    def get_ack_deferred_config(cls) -> Dict[str, Any]:
        """Obtiene la configuración del sistema de ACK diferido"""
        return cls.ACK_DEFERRED_CONFIG.copy()
    
    @classmethod
    def get_rate_limit_config(cls) -> Dict[str, Any]:
        """Obtiene la configuración de rate limiting"""
        return cls.RATE_LIMIT_CONFIG.copy()
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """Obtiene la configuración de logging"""
        return cls.LOGGING_CONFIG.copy()
    
    @classmethod
    def get_metrics_config(cls) -> Dict[str, Any]:
        """Obtiene la configuración de métricas"""
        return cls.METRICS_CONFIG.copy()
    
    @classmethod
    def get_security_config(cls) -> Dict[str, Any]:
        """Obtiene la configuración de seguridad"""
        return cls.SECURITY_CONFIG.copy()
    
    @classmethod
    def get_response_config(cls) -> Dict[str, Any]:
        """Obtiene la configuración de respuestas"""
        return cls.RESPONSE_CONFIG.copy()
    
    @classmethod
    def validate_config(cls) -> bool:
        """Valida que todas las configuraciones sean correctas"""
        try:
            # Validar configuraciones numéricas
            ack_config = cls.get_ack_deferred_config()
            if ack_config["max_workers"] <= 0:
                raise ValueError("max_workers debe ser mayor que 0")
            if ack_config["request_timeout"] <= 0:
                raise ValueError("request_timeout debe ser mayor que 0")
            if ack_config["max_retries"] < 0:
                raise ValueError("max_retries debe ser mayor o igual que 0")
            
            # Validar rate limiting
            rate_config = cls.get_rate_limit_config()
            if rate_config["requests_per_minute"] <= 0:
                raise ValueError("requests_per_minute debe ser mayor que 0")
            
            # Validar métricas
            metrics_config = cls.get_metrics_config()
            if metrics_config["retention_hours"] <= 0:
                raise ValueError("retention_hours debe ser mayor que 0")
            
            return True
            
        except Exception as e:
            print(f"Error validando configuración: {e}")
            return False
    
    @classmethod
    def print_config_summary(cls):
        """Imprime un resumen de la configuración actual"""
        print("=== Configuración de Discord ===")
        print(f"ACK Diferido: {cls.get_ack_deferred_config()}")
        print(f"Rate Limiting: {cls.get_rate_limit_config()}")
        print(f"Logging: {cls.get_logging_config()}")
        print(f"Métricas: {cls.get_metrics_config()}")
        print(f"Seguridad: {cls.get_security_config()}")
        print(f"Respuestas: {cls.get_response_config()}")
        print("================================")
