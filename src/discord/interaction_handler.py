"""
Manejador mejorado de interacciones de Discord con ACK diferido robusto
"""

import asyncio
import threading
import time
import requests
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import queue
from src.utils.logger import logger
from src.utils.metrics import metrics_collector
from config.discord_settings import DiscordConfig

class InteractionStatus(Enum):
    """Estados posibles de una interacción"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class InteractionRequest:
    """Estructura para manejar una petición de interacción"""
    interaction_token: str
    application_id: str
    user_id: str
    username: str
    roles: list
    prompt: str
    timestamp: float
    guild_id: str = None
    channel_id: str = None
    retry_count: int = 0
    max_retries: int = 3
    status: InteractionStatus = InteractionStatus.PENDING

class DiscordInteractionHandler:
    """
    Manejador robusto de interacciones de Discord con ACK diferido mejorado
    """
    
    def __init__(self, max_workers: int = None, request_timeout: int = None):
        # Usar configuración por defecto si no se especifica
        config = DiscordConfig.get_ack_deferred_config()
        self.max_workers = max_workers or config["max_workers"]
        self.request_timeout = request_timeout or config["request_timeout"]
        self.max_retries = config["max_retries"]
        self.retry_delays = config["retry_delays"]
        self.queue_max_size = config["queue_max_size"]
        
        self.request_queue = queue.Queue(maxsize=self.queue_max_size)
        self.active_requests: Dict[str, InteractionRequest] = {}
        self.processing_threads = []
        self.running = False
        
        # Iniciar workers
        self._start_workers()
        
        # Iniciar limpieza automática de métricas
        self._start_metrics_cleanup()
    
    def _start_workers(self):
        """Inicia los workers para procesar las peticiones"""
        self.running = True
        for i in range(self.max_workers):
            thread = threading.Thread(target=self._worker_loop, name=f"DiscordWorker-{i}")
            thread.daemon = True
            thread.start()
            self.processing_threads.append(thread)
        logger.info(f"Iniciados {self.max_workers} workers para procesamiento de interacciones")
    
    def _worker_loop(self):
        """Loop principal del worker para procesar peticiones"""
        while self.running:
            try:
                # Obtener petición de la cola con timeout
                request = self.request_queue.get(timeout=1)
                self._process_request(request)
                self.request_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error en worker loop: {e}")
    
    def _process_request(self, request: InteractionRequest):
        """Procesa una petición individual"""
        request_id = f"{request.interaction_token}_{request.user_id}"
        start_time = time.time()
        
        try:
            # Actualizar estado
            request.status = InteractionStatus.PROCESSING
            self.active_requests[request_id] = request
            
            # Registrar métricas
            metrics_collector.increment_counter("discord_interactions_total", labels={"command": "chat"})
            metrics_collector.record_value("discord_queue_size", self.request_queue.qsize())
            
            logger.info(f"Procesando petición {request_id} (intento {request.retry_count + 1})")
            
            # Importar aquí para evitar dependencias circulares
            from src.core.chat import chat
            
            # Procesar la respuesta del chat
            chat_start_time = time.time()
            respuesta = chat(
                request.prompt, 
                user_id=request.user_id, 
                roles=request.roles,
                username=request.username,
                interaction_token=request.interaction_token,
                guild_id=request.guild_id,
                channel_id=request.channel_id
            )
            processing_time = time.time() - chat_start_time
            
            logger.info(f"Chat procesado en {processing_time:.2f}s para usuario {request.user_id}")
            
            # Enviar respuesta a Discord
            success = self._send_discord_response(request, respuesta)
            
            if success:
                request.status = InteractionStatus.COMPLETED
                total_time = time.time() - start_time
                metrics_collector.increment_counter("discord_interactions_success", labels={"command": "chat"})
                metrics_collector.record_response_time("discord_response_time_ms", start_time, labels={"command": "chat"})
                logger.info(f"Petición {request_id} completada exitosamente en {total_time:.2f}s")
            else:
                raise Exception("Error enviando respuesta a Discord")
                
        except Exception as e:
            logger.error(f"Error procesando petición {request_id}: {e}")
            metrics_collector.increment_counter("discord_interactions_failed", labels={"command": "chat", "error": str(e)[:50]})
            self._handle_request_failure(request, str(e))
    
    def _send_discord_response(self, request: InteractionRequest, content: str) -> bool:
        """Envía la respuesta a Discord con reintentos"""
        url = f"https://discord.com/api/v10/webhooks/{request.application_id}/{request.interaction_token}"
        
        for attempt in range(request.max_retries):
            try:
                data = {"content": content}
                response = requests.post(
                    url, 
                    json=data, 
                    timeout=self.request_timeout,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "PythonBots-Discord/1.0"
                    }
                )
                
                if response.status_code == 200:
                    logger.info(f"Respuesta enviada exitosamente a Discord (intento {attempt + 1})")
                    return True
                elif response.status_code == 429:  # Rate limit
                    retry_after = int(response.headers.get("Retry-After", 1))
                    logger.warning(f"Rate limit alcanzado, esperando {retry_after}s")
                    time.sleep(retry_after)
                    continue
                else:
                    logger.warning(f"Error HTTP {response.status_code} enviando respuesta (intento {attempt + 1})")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout enviando respuesta (intento {attempt + 1})")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Error de red enviando respuesta (intento {attempt + 1}): {e}")
            
            # Esperar antes del siguiente intento
            if attempt < request.max_retries - 1:
                delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]
                logger.info(f"Reintentando en {delay}s...")
                time.sleep(delay)
        
        return False
    
    def _handle_request_failure(self, request: InteractionRequest, error: str):
        """Maneja el fallo de una petición"""
        request_id = f"{request.interaction_token}_{request.user_id}"
        
        if request.retry_count < request.max_retries:
            # Reintentar
            request.retry_count += 1
            request.status = InteractionStatus.RETRYING
            
            # Registrar reintento
            metrics_collector.increment_counter("discord_retry_count", labels={"command": "chat"})
            
            delay = self.retry_delays[min(request.retry_count - 1, len(self.retry_delays) - 1)]
            logger.info(f"Reintentando petición {request_id} en {delay}s (intento {request.retry_count})")
            
            # Programar reintento
            threading.Timer(delay, self._retry_request, args=[request]).start()
        else:
            # Fallo definitivo
            request.status = InteractionStatus.FAILED
            logger.error(f"Petición {request_id} falló definitivamente después de {request.max_retries} intentos")
            
            # Enviar mensaje de error
            self._send_error_message(request, error)
    
    def _retry_request(self, request: InteractionRequest):
        """Reintenta una petición fallida"""
        request.status = InteractionStatus.PENDING
        self.request_queue.put(request)
    
    def _send_error_message(self, request: InteractionRequest, error: str):
        """Envía un mensaje de error al usuario"""
        try:
            url = f"https://discord.com/api/v10/webhooks/{request.application_id}/{request.interaction_token}"
            error_data = {
                "content": "❌ Lo siento, hubo un error procesando tu mensaje. Por favor, inténtalo de nuevo en unos momentos.",
                "flags": 64  # Ephemeral flag
            }
            
            response = requests.post(url, json=error_data, timeout=10)
            if response.status_code == 200:
                logger.info(f"Mensaje de error enviado para petición {request.interaction_token}")
            else:
                logger.error(f"No se pudo enviar mensaje de error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error enviando mensaje de error: {e}")
    
    def submit_interaction(self, interaction_data: Dict[str, Any], prompt: str) -> bool:
        """
        Envía una interacción para procesamiento asíncrono
        
        Args:
            interaction_data: Datos de la interacción de Discord
            prompt: Mensaje del usuario
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Extraer datos de la interacción
            interaction_token = interaction_data.get("token")
            application_id = interaction_data.get("application_id")
            user_id = str(interaction_data.get("member", {}).get("user", {}).get("id", "unknown"))
            username = interaction_data.get("member", {}).get("user", {}).get("username", "Unknown")
            roles = interaction_data.get("member", {}).get("roles", [])
            guild_id = interaction_data.get("guild_id")
            channel_id = interaction_data.get("channel_id")
            
            if not all([interaction_token, application_id, user_id]):
                logger.error("Datos de interacción incompletos")
                return False
            
            # Crear petición
            request = InteractionRequest(
                interaction_token=interaction_token,
                application_id=application_id,
                user_id=user_id,
                username=username,
                roles=roles,
                prompt=prompt,
                timestamp=time.time(),
                guild_id=guild_id,
                channel_id=channel_id,
                max_retries=self.max_retries
            )
            
            # Enviar a la cola
            self.request_queue.put(request)
            
            # Registrar métricas
            metrics_collector.record_value("discord_queue_size", self.request_queue.qsize())
            metrics_collector.record_value("discord_active_workers", len([t for t in self.processing_threads if t.is_alive()]))
            
            logger.info(f"Interacción enviada a cola para usuario {user_id}: {prompt[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando interacción a cola: {e}")
            return False
    
    def get_request_status(self, interaction_token: str, user_id: str) -> Optional[InteractionStatus]:
        """Obtiene el estado de una petición específica"""
        request_id = f"{interaction_token}_{user_id}"
        request = self.active_requests.get(request_id)
        return request.status if request else None
    
    def get_queue_size(self) -> int:
        """Obtiene el tamaño actual de la cola"""
        return self.request_queue.qsize()
    
    def get_active_requests_count(self) -> int:
        """Obtiene el número de peticiones activas"""
        return len(self.active_requests)
    
    def _start_metrics_cleanup(self):
        """Inicia el proceso de limpieza automática de métricas"""
        def cleanup_loop():
            while self.running:
                try:
                    time.sleep(3600)  # Limpiar cada hora
                    if self.running:
                        metrics_collector.clear_old_data(max_age_seconds=86400)  # 24 horas
                        logger.debug("Limpieza automática de métricas completada")
                except Exception as e:
                    logger.error(f"Error en limpieza automática de métricas: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, name="MetricsCleanup")
        cleanup_thread.daemon = True
        cleanup_thread.start()
        logger.info("Proceso de limpieza automática de métricas iniciado")
    
    def shutdown(self):
        """Detiene el manejador de interacciones"""
        self.running = False
        logger.info("Deteniendo manejador de interacciones de Discord...")
        
        # Esperar a que se completen las peticiones pendientes
        self.request_queue.join()
        
        # Limpiar peticiones activas
        self.active_requests.clear()

# Instancia global del manejador
interaction_handler = DiscordInteractionHandler()
