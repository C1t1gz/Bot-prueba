"""
Sistema de métricas para monitorear el rendimiento del bot
"""

import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
from src.utils.logger import logger

class MetricType(Enum):
    """Tipos de métricas disponibles"""
    REQUEST_COUNT = "request_count"
    RESPONSE_TIME = "response_time"
    SUCCESS_RATE = "success_rate"
    ERROR_COUNT = "error_count"
    QUEUE_SIZE = "queue_size"
    ACTIVE_WORKERS = "active_workers"

@dataclass
class MetricPoint:
    """Punto de datos para una métrica"""
    timestamp: float
    value: float
    labels: Dict[str, str] = field(default_factory=dict)

@dataclass
class Metric:
    """Métrica individual con historial"""
    name: str
    metric_type: MetricType
    description: str
    data: deque = field(default_factory=lambda: deque(maxlen=1000))
    labels: Dict[str, str] = field(default_factory=dict)

class MetricsCollector:
    """
    Recolector de métricas para monitorear el rendimiento del bot
    """
    
    def __init__(self):
        self.metrics: Dict[str, Metric] = {}
        self.lock = threading.RLock()
        self.start_time = time.time()
        
        # Inicializar métricas básicas
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Inicializa las métricas básicas del sistema"""
        self.register_metric("discord_interactions_total", MetricType.REQUEST_COUNT, "Total de interacciones de Discord")
        self.register_metric("discord_interactions_success", MetricType.REQUEST_COUNT, "Interacciones exitosas")
        self.register_metric("discord_interactions_failed", MetricType.REQUEST_COUNT, "Interacciones fallidas")
        self.register_metric("discord_response_time_ms", MetricType.RESPONSE_TIME, "Tiempo de respuesta en milisegundos")
        self.register_metric("discord_queue_size", MetricType.QUEUE_SIZE, "Tamaño de la cola de procesamiento")
        self.register_metric("discord_active_workers", MetricType.ACTIVE_WORKERS, "Workers activos")
        self.register_metric("discord_retry_count", MetricType.REQUEST_COUNT, "Número de reintentos")
        
        logger.info("Sistema de métricas inicializado")
    
    def register_metric(self, name: str, metric_type: MetricType, description: str, labels: Optional[Dict[str, str]] = None):
        """Registra una nueva métrica"""
        with self.lock:
            if name not in self.metrics:
                self.metrics[name] = Metric(
                    name=name,
                    metric_type=metric_type,
                    description=description,
                    labels=labels or {}
                )
                logger.debug(f"Métrica registrada: {name}")
    
    def record_value(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Registra un valor para una métrica específica"""
        with self.lock:
            if metric_name in self.metrics:
                metric = self.metrics[metric_name]
                point = MetricPoint(
                    timestamp=time.time(),
                    value=value,
                    labels=labels or {}
                )
                metric.data.append(point)
            else:
                logger.warning(f"Métrica no registrada: {metric_name}")
    
    def increment_counter(self, metric_name: str, increment: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Incrementa un contador"""
        self.record_value(metric_name, increment, labels)
    
    def record_response_time(self, metric_name: str, start_time: float, labels: Optional[Dict[str, str]] = None):
        """Registra el tiempo de respuesta en milisegundos"""
        response_time_ms = (time.time() - start_time) * 1000
        self.record_value(metric_name, response_time_ms, labels)
    
    def get_metric_summary(self, metric_name: str, window_seconds: int = 300) -> Optional[Dict]:
        """Obtiene un resumen de una métrica específica"""
        with self.lock:
            if metric_name not in self.metrics:
                return None
            
            metric = self.metrics[metric_name]
            cutoff_time = time.time() - window_seconds
            
            # Filtrar datos dentro de la ventana de tiempo
            recent_data = [point for point in metric.data if point.timestamp >= cutoff_time]
            
            if not recent_data:
                return {
                    "name": metric_name,
                    "description": metric.description,
                    "window_seconds": window_seconds,
                    "count": 0,
                    "total": 0,
                    "average": 0,
                    "min": 0,
                    "max": 0
                }
            
            values = [point.value for point in recent_data]
            
            return {
                "name": metric_name,
                "description": metric.description,
                "window_seconds": window_seconds,
                "count": len(values),
                "total": sum(values),
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
    
    def get_all_metrics_summary(self, window_seconds: int = 300) -> Dict[str, Dict]:
        """Obtiene un resumen de todas las métricas"""
        with self.lock:
            summary = {}
            for metric_name in self.metrics:
                summary[metric_name] = self.get_metric_summary(metric_name, window_seconds)
            return summary
    
    def get_system_health(self) -> Dict[str, any]:
        """Obtiene el estado de salud del sistema"""
        with self.lock:
            uptime = time.time() - self.start_time
            
            # Obtener métricas recientes (últimos 5 minutos)
            recent_metrics = self.get_all_metrics_summary(300)
            
            # Calcular tasas de éxito
            total_interactions = recent_metrics.get("discord_interactions_total", {}).get("total", 0)
            successful_interactions = recent_metrics.get("discord_interactions_success", {}).get("total", 0)
            failed_interactions = recent_metrics.get("discord_interactions_failed", {}).get("total", 0)
            
            success_rate = (successful_interactions / total_interactions * 100) if total_interactions > 0 else 0
            
            # Tiempo de respuesta promedio
            avg_response_time = recent_metrics.get("discord_response_time_ms", {}).get("average", 0)
            
            # Estado de la cola
            current_queue_size = recent_metrics.get("discord_queue_size", {}).get("total", 0)
            
            return {
                "status": "healthy" if success_rate > 95 and avg_response_time < 10000 else "degraded",
                "uptime_seconds": uptime,
                "uptime_formatted": self._format_uptime(uptime),
                "success_rate_percent": round(success_rate, 2),
                "average_response_time_ms": round(avg_response_time, 2),
                "total_interactions": total_interactions,
                "failed_interactions": failed_interactions,
                "current_queue_size": current_queue_size,
                "last_updated": time.time()
            }
    
    def _format_uptime(self, seconds: float) -> str:
        """Formatea el tiempo de actividad en formato legible"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def export_metrics_prometheus(self) -> str:
        """Exporta las métricas en formato Prometheus"""
        with self.lock:
            lines = []
            current_time = int(time.time() * 1000)
            
            for metric_name, metric in self.metrics.items():
                if not metric.data:
                    continue
                
                # Obtener el valor más reciente
                latest_point = metric.data[-1]
                
                # Construir etiquetas
                labels_str = ""
                if metric.labels or latest_point.labels:
                    all_labels = {**metric.labels, **latest_point.labels}
                    if all_labels:
                        labels_str = "{" + ",".join([f'{k}="{v}"' for k, v in all_labels.items()]) + "}"
                
                # Formato Prometheus
                line = f"{metric_name}{labels_str} {latest_point.value} {current_time}"
                lines.append(line)
            
            return "\n".join(lines)
    
    def clear_old_data(self, max_age_seconds: int = 3600):
        """Limpia datos antiguos de las métricas"""
        with self.lock:
            cutoff_time = time.time() - max_age_seconds
            cleared_count = 0
            
            for metric in self.metrics.values():
                original_size = len(metric.data)
                metric.data = deque(
                    [point for point in metric.data if point.timestamp >= cutoff_time],
                    maxlen=metric.data.maxlen
                )
                cleared_count += original_size - len(metric.data)
            
            if cleared_count > 0:
                logger.info(f"Limpieza de métricas: {cleared_count} puntos de datos antiguos eliminados")

# Instancia global del recolector de métricas
metrics_collector = MetricsCollector()
