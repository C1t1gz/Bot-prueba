"""
Utilidades de seguridad para verificación de Discord
"""

import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

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
    public_key = os.getenv("DISCORD_PUBLIC_KEY")
    if not public_key:
        return False
        
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(timestamp.encode() + body, bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False
    except Exception:
        return False
