"""
Módulo para almacenar y gestionar contextos de consultas del bot
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
from collections import defaultdict

from src.utils.logger import logger

@dataclass
class QueryContext:
    """Estructura para almacenar el contexto de una consulta"""
    user_id: str
    username: str
    prompt: str
    response: str
    timestamp: float
    roles: List[str]
    documents_used: List[str]
    processing_time: float
    model_used: str
    interaction_token: str
    guild_id: Optional[str] = None
    channel_id: Optional[str] = None

class ContextStorage:
    """
    Sistema para almacenar y gestionar contextos de consultas
    """
    
    def __init__(self, storage_dir: str = "data/contexts"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo principal para almacenar contextos
        self.contexts_file = self.storage_dir / "query_contexts.jsonl"
        
        # Archivo para estadísticas
        self.stats_file = self.storage_dir / "query_stats.json"
        
        # Lock para operaciones thread-safe
        self._lock = threading.Lock()
        
        # Cache en memoria para estadísticas
        self._stats_cache = None
        self._cache_timestamp = 0
        self._cache_ttl = 300  # 5 minutos
        
        logger.info(f"Sistema de almacenamiento de contextos inicializado en: {self.storage_dir}")
    
    def store_context(self, context: QueryContext) -> bool:
        """
        Almacena un contexto de consulta
        
        Args:
            context: Contexto de la consulta a almacenar
            
        Returns:
            bool: True si se almacenó correctamente
        """
        try:
            with self._lock:
                # Convertir a diccionario
                context_dict = asdict(context)
                context_dict['datetime'] = datetime.fromtimestamp(context.timestamp).isoformat()
                
                # Escribir en formato JSONL
                with open(self.contexts_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(context_dict, ensure_ascii=False) + '\n')
                
                # Invalidar cache de estadísticas
                self._invalidate_stats_cache()
                
                logger.debug(f"Contexto almacenado para usuario {context.user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error almacenando contexto: {e}")
            return False
    
    def get_user_contexts(self, user_id: str, limit: int = 50) -> List[QueryContext]:
        """
        Obtiene los contextos de un usuario específico
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de contextos a retornar
            
        Returns:
            List[QueryContext]: Lista de contextos del usuario
        """
        contexts = []
        try:
            with open(self.contexts_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        if data.get('user_id') == user_id:
                            # Recrear objeto QueryContext
                            context = QueryContext(
                                user_id=data['user_id'],
                                username=data['username'],
                                prompt=data['prompt'],
                                response=data['response'],
                                timestamp=data['timestamp'],
                                roles=data['roles'],
                                documents_used=data['documents_used'],
                                processing_time=data['processing_time'],
                                model_used=data['model_used'],
                                interaction_token=data['interaction_token'],
                                guild_id=data.get('guild_id'),
                                channel_id=data.get('channel_id')
                            )
                            contexts.append(context)
                            
                            if len(contexts) >= limit:
                                break
                                
        except FileNotFoundError:
            logger.debug("Archivo de contextos no encontrado")
        except Exception as e:
            logger.error(f"Error leyendo contextos del usuario {user_id}: {e}")
        
        return contexts
    
    def get_all_contexts(self, limit: int = 1000) -> List[QueryContext]:
        """
        Obtiene todos los contextos almacenados
        
        Args:
            limit: Número máximo de contextos a retornar
            
        Returns:
            List[QueryContext]: Lista de todos los contextos
        """
        contexts = []
        try:
            with open(self.contexts_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and len(contexts) < limit:
                        data = json.loads(line)
                        context = QueryContext(
                            user_id=data['user_id'],
                            username=data['username'],
                            prompt=data['prompt'],
                            response=data['response'],
                            timestamp=data['timestamp'],
                            roles=data['roles'],
                            documents_used=data['documents_used'],
                            processing_time=data['processing_time'],
                            model_used=data['model_used'],
                            interaction_token=data['interaction_token'],
                            guild_id=data.get('guild_id'),
                            channel_id=data.get('channel_id')
                        )
                        contexts.append(context)
                        
        except FileNotFoundError:
            logger.debug("Archivo de contextos no encontrado")
        except Exception as e:
            logger.error(f"Error leyendo todos los contextos: {e}")
        
        return contexts
    
    def get_query_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de las consultas
        
        Returns:
            Dict con estadísticas de consultas
        """
        # Verificar cache
        current_time = time.time()
        if (self._stats_cache and 
            current_time - self._cache_timestamp < self._cache_ttl):
            return self._stats_cache
        
        try:
            # Intentar cargar desde archivo
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                    self._stats_cache = stats
                    self._cache_timestamp = current_time
                    return stats
        except Exception as e:
            logger.warning(f"Error cargando estadísticas desde archivo: {e}")
        
        # Calcular estadísticas desde los datos
        stats = self._calculate_statistics()
        
        # Guardar en archivo
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error guardando estadísticas: {e}")
        
        self._stats_cache = stats
        self._cache_timestamp = current_time
        return stats
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """
        Calcula estadísticas desde los datos almacenados
        """
        contexts = self.get_all_contexts()
        
        if not contexts:
            return {
                "total_queries": 0,
                "unique_users": 0,
                "top_users": [],
                "top_queries": [],
                "average_processing_time": 0,
                "queries_by_hour": {},
                "queries_by_day": {},
                "last_updated": datetime.now().isoformat()
            }
        
        # Estadísticas básicas
        total_queries = len(contexts)
        unique_users = len(set(ctx.user_id for ctx in contexts))
        
        # Usuarios más activos
        user_counts = defaultdict(int)
        for ctx in contexts:
            user_counts[ctx.user_id] += 1
        
        top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_users = [{"user_id": user_id, "username": self._get_username(user_id, contexts), "count": count} 
                    for user_id, count in top_users]
        
        # Consultas más comunes (basadas en palabras clave)
        query_keywords = defaultdict(int)
        for ctx in contexts:
            # Extraer palabras clave del prompt
            words = ctx.prompt.lower().split()
            for word in words:
                if len(word) > 3:  # Solo palabras de más de 3 caracteres
                    query_keywords[word] += 1
        
        top_queries = sorted(query_keywords.items(), key=lambda x: x[1], reverse=True)[:20]
        top_queries = [{"keyword": keyword, "count": count} for keyword, count in top_queries]
        
        # Tiempo promedio de procesamiento
        avg_processing_time = sum(ctx.processing_time for ctx in contexts) / total_queries
        
        # Consultas por hora del día
        queries_by_hour = defaultdict(int)
        for ctx in contexts:
            hour = datetime.fromtimestamp(ctx.timestamp).hour
            queries_by_hour[hour] += 1
        
        # Consultas por día de la semana
        queries_by_day = defaultdict(int)
        for ctx in contexts:
            day = datetime.fromtimestamp(ctx.timestamp).strftime('%A')
            queries_by_day[day] += 1
        
        return {
            "total_queries": total_queries,
            "unique_users": unique_users,
            "top_users": top_users,
            "top_queries": top_queries,
            "average_processing_time": round(avg_processing_time, 2),
            "queries_by_hour": dict(queries_by_hour),
            "queries_by_day": dict(queries_by_day),
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_username(self, user_id: str, contexts: List[QueryContext]) -> str:
        """Obtiene el username de un user_id desde los contextos"""
        for ctx in contexts:
            if ctx.user_id == user_id:
                return ctx.username
        return "Unknown"
    
    def _invalidate_stats_cache(self):
        """Invalida el cache de estadísticas"""
        self._stats_cache = None
        self._cache_timestamp = 0
    
    def export_contexts(self, output_file: str = None) -> str:
        """
        Exporta todos los contextos a un archivo JSON
        
        Args:
            output_file: Archivo de salida (opcional)
            
        Returns:
            str: Ruta del archivo exportado
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.storage_dir / f"contexts_export_{timestamp}.json"
        
        try:
            contexts = self.get_all_contexts()
            contexts_dict = [asdict(ctx) for ctx in contexts]
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(contexts_dict, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Contextos exportados a: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error exportando contextos: {e}")
            return ""
    
    def cleanup_old_contexts(self, days_to_keep: int = 30) -> int:
        """
        Limpia contextos antiguos
        
        Args:
            days_to_keep: Número de días de contextos a mantener
            
        Returns:
            int: Número de contextos eliminados
        """
        cutoff_time = time.time() - (days_to_keep * 24 * 3600)
        temp_file = self.storage_dir / "temp_contexts.jsonl"
        removed_count = 0
        
        try:
            with open(self.contexts_file, 'r', encoding='utf-8') as input_file, \
                 open(temp_file, 'w', encoding='utf-8') as output_file:
                
                for line in input_file:
                    if line.strip():
                        data = json.loads(line)
                        if data.get('timestamp', 0) >= cutoff_time:
                            output_file.write(line)
                        else:
                            removed_count += 1
            
            # Reemplazar archivo original
            temp_file.replace(self.contexts_file)
            
            # Invalidar cache
            self._invalidate_stats_cache()
            
            logger.info(f"Limpieza completada: {removed_count} contextos eliminados")
            return removed_count
            
        except Exception as e:
            logger.error(f"Error en limpieza de contextos: {e}")
            return 0

# Instancia global del almacenamiento de contextos
context_storage = ContextStorage()
