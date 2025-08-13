"""
Módulo simple de RAG que busca por palabras clave en base.txt
"""
from pathlib import Path
from typing import List
import re

BASE_PATH = Path(__file__).parent / "base.txt"

class SimpleRAG:
    """
    Clase para realizar búsquedas simples en base.txt usando palabras clave.
    """
    def __init__(self):
        """
        Inicializa la instancia cargando las líneas de base.txt.
        No recibe parámetros.
        """
        self.lines = self._load_base()
    
    def _load_base(self) -> List[str]:
        """
        Carga el archivo base.txt y devuelve las líneas no vacías.
        No recibe parámetros.
        Retorna:
            List[str]: Lista de líneas útiles de base.txt.
        """
        if not BASE_PATH.exists():
            print("⚠️ No se encontró base.txt")
            return []
            
        with open(BASE_PATH, 'r', encoding='utf-8') as f:
            # Filtrar líneas vacías y comentarios
            return [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith('#')
            ]
    
    def search(self, query: str, top_k: int = 3) -> List[str]:
        """
        Busca las líneas más relevantes según palabras clave.
        Parámetros:
            query (str): Consulta de búsqueda.
            top_k (int, opcional): Número máximo de resultados a devolver (por defecto 3).
        Retorna:
            List[str]: Lista de líneas relevantes de base.txt.
        """
        if not self.lines:
            return []
            
        # Extraer palabras clave de la consulta (eliminar signos de puntuación)
        words = set(re.findall(r'\b\w+\b', query.lower()))
        if not words:
            return []
        
        # Calcular puntuación para cada línea
        scored_lines = []
        for line in self.lines:
            line_lower = line.lower()
            # Contar coincidencias de palabras clave
            score = sum(1 for word in words if word in line_lower)
            if score > 0:
                scored_lines.append((score, line))
        
        # Ordenar por puntuación (mayor a menor) y devolver las top_k
        scored_lines.sort(reverse=True, key=lambda x: x[0])
        return [line for _, line in scored_lines[:top_k]]

# Instancia global para facilitar el uso
rag = SimpleRAG()

def get_relevant_chunks(query: str, top_k: int = 3) -> List[str]:
    """
    Función de conveniencia para buscar los fragmentos más relevantes en base.txt.
    Parámetros:
        query (str): Consulta de búsqueda.
        top_k (int, opcional): Número máximo de resultados a devolver (por defecto 3).
    Retorna:
        List[str]: Lista de fragmentos relevantes.
    """
    return rag.search(query, top_k)

# Si se ejecuta directamente, probar la búsqueda
if __name__ == "__main__":
    while True:
        query = input("Buscar: ")
        if not query:
            break
        results = get_relevant_chunks(query)
        print(f"\nResultados para '{query}':")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r}")
        print()
