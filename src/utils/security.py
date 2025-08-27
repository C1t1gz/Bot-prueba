"""
Utilidades de seguridad para verificación de Discord
"""

import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from src.utils.logger import logger

def verify_discord_signature(signature: str, timestamp: str, body: bytes) -> bool:
    """
    Verifica la firma de una solicitud recibida desde Discord.
    
    Args:
        signature (str): Firma de la solicitud
        timestamp (str): Timestamp de la solicitud
        body (bytes): Cuerpo de la solicitud
        
    Returns:
        bool: True si la firma es válida, False en caso contrario
    """
    logger.debug(f"Verificando firma de Discord: signature={signature[:10]}..., timestamp={timestamp}")
    
    public_key = os.getenv("DISCORD_PUBLIC_KEY")
    if not public_key:
        logger.error("DISCORD_PUBLIC_KEY no encontrada en variables de entorno")
        return False
        
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(timestamp.encode() + body, bytes.fromhex(signature))
        logger.debug("Firma de Discord verificada correctamente")
        return True
    except BadSignatureError:
        logger.warning("Firma de Discord inválida (BadSignatureError)")
        return False
    except Exception as e:
        logger.error(f"Error verificando firma de Discord: {e}")
        return False
