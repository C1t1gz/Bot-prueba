"""
Sistema de memoria persistente por usuario usando LangChain
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import threading

from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage

from src.utils.logger import logger

class PersistentMemoryManager:
    """
    Gestor de memoria persistente por usuario
    """
    
    def __init__(self, storage_dir: str = "data/memory"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache en memoria para acceso rápido
        self._memory_cache: Dict[str, ConversationBufferMemory] = {}
        
        # Lock para operaciones thread-safe
        self._lock = threading.Lock()
        
        logger.info(f"Sistema de memoria persistente inicializado en: {self.storage_dir}")
    
    def get_user_memory(self, user_id: str) -> ConversationBufferMemory:
        """
        Obtiene la memoria de un usuario, cargándola desde disco si es necesario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            ConversationBufferMemory: Memoria del usuario
        """
        with self._lock:
            # Verificar si ya está en cache
            if user_id in self._memory_cache:
                return self._memory_cache[user_id]
            
            # Cargar desde disco
            memory = self._load_memory_from_disk(user_id)
            self._memory_cache[user_id] = memory
            return memory
    
    def _load_memory_from_disk(self, user_id: str) -> ConversationBufferMemory:
        """
        Carga la memoria de un usuario desde disco
        """
        memory_file = self.storage_dir / f"memory_{user_id}.json"
        
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Crear memoria con historial cargado
                memory = ConversationBufferMemory(return_messages=True)
                
                # Restaurar mensajes del historial
                for msg_data in data.get('messages', []):
                    if msg_data['type'] == 'human':
                        memory.chat_memory.add_user_message(msg_data['content'])
                    elif msg_data['type'] == 'ai':
                        memory.chat_memory.add_ai_message(msg_data['content'])
                
                logger.debug(f"Memoria cargada para usuario {user_id}: {len(data.get('messages', []))} mensajes")
                return memory
                
            except Exception as e:
                logger.error(f"Error cargando memoria para usuario {user_id}: {e}")
        
        # Crear nueva memoria si no existe
        logger.debug(f"Creando nueva memoria para usuario {user_id}")
        return ConversationBufferMemory(return_messages=True)
    
    def save_user_memory(self, user_id: str, memory: ConversationBufferMemory) -> bool:
        """
        Guarda la memoria de un usuario en disco
        
        Args:
            user_id: ID del usuario
            memory: Memoria a guardar
            
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            with self._lock:
                memory_file = self.storage_dir / f"memory_{user_id}.json"
                
                # Convertir mensajes a formato serializable
                messages = []
                for msg in memory.chat_memory.messages:
                    if isinstance(msg, HumanMessage):
                        messages.append({
                            'type': 'human',
                            'content': msg.content,
                            'timestamp': datetime.now().isoformat()
                        })
                    elif isinstance(msg, AIMessage):
                        messages.append({
                            'type': 'ai',
                            'content': msg.content,
                            'timestamp': datetime.now().isoformat()
                        })
                
                # Guardar en disco
                data = {
                    'user_id': user_id,
                    'last_updated': datetime.now().isoformat(),
                    'message_count': len(messages),
                    'messages': messages
                }
                
                with open(memory_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                logger.debug(f"Memoria guardada para usuario {user_id}: {len(messages)} mensajes")
                return True
                
        except Exception as e:
            logger.error(f"Error guardando memoria para usuario {user_id}: {e}")
            return False
    
    def clear_user_memory(self, user_id: str) -> bool:
        """
        Borra la memoria de un usuario (tanto de cache como de disco)
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se borró correctamente
        """
        try:
            with self._lock:
                # Borrar de cache
                if user_id in self._memory_cache:
                    del self._memory_cache[user_id]
                
                # Borrar archivo de disco
                memory_file = self.storage_dir / f"memory_{user_id}.json"
                if memory_file.exists():
                    memory_file.unlink()
                
                logger.info(f"Memoria borrada para usuario {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error borrando memoria para usuario {user_id}: {e}")
            return False
    
    def get_user_memory_info(self, user_id: str) -> Optional[Dict]:
        """
        Obtiene información sobre la memoria de un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Dict con información de la memoria o None si no existe
        """
        memory_file = self.storage_dir / f"memory_{user_id}.json"
        
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                return {
                    'user_id': user_id,
                    'message_count': data.get('message_count', 0),
                    'last_updated': data.get('last_updated'),
                    'file_size': memory_file.stat().st_size
                }
                
            except Exception as e:
                logger.error(f"Error obteniendo información de memoria para usuario {user_id}: {e}")
        
        return None
    
    def get_all_memory_info(self) -> List[Dict]:
        """
        Obtiene información de todas las memorias de usuario
        
        Returns:
            List[Dict]: Lista con información de todas las memorias
        """
        memory_info = []
        
        try:
            for memory_file in self.storage_dir.glob("memory_*.json"):
                user_id = memory_file.stem.replace("memory_", "")
                info = self.get_user_memory_info(user_id)
                if info:
                    memory_info.append(info)
                    
        except Exception as e:
            logger.error(f"Error obteniendo información de todas las memorias: {e}")
        
        return memory_info
    
    def cleanup_old_memories(self, days_to_keep: int = 30) -> int:
        """
        Limpia memorias antiguas
        
        Args:
            days_to_keep: Número de días de memorias a mantener
            
        Returns:
            int: Número de memorias eliminadas
        """
        import time
        cutoff_time = time.time() - (days_to_keep * 24 * 3600)
        removed_count = 0
        
        try:
            for memory_file in self.storage_dir.glob("memory_*.json"):
                if memory_file.stat().st_mtime < cutoff_time:
                    user_id = memory_file.stem.replace("memory_", "")
                    if self.clear_user_memory(user_id):
                        removed_count += 1
                        
        except Exception as e:
            logger.error(f"Error limpiando memorias antiguas: {e}")
        
        return removed_count

# Instancia global del gestor de memoria persistente
persistent_memory = PersistentMemoryManager()
