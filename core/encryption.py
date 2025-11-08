"""
Utilidades de cifrado para datos sensibles.

Implementa cifrado AES-256-GCM para proteger información sensible
en reposo (alergias, condiciones de salud, etc.).
"""

import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.conf import settings


class EncryptionService:
    """
    Servicio de cifrado/descifrado usando AES-256-GCM.
    
    AES-256-GCM proporciona:
    - Cifrado autenticado (confidencialidad + integridad)
    - Resistencia a manipulación de datos
    - Rendimiento eficiente
    """
    
    def __init__(self):
        """Inicializa el servicio con la clave de cifrado."""
        encryption_key = getattr(settings, 'ENCRYPTION_KEY', None)
        if not encryption_key:
            raise ValueError(
                "ENCRYPTION_KEY no está configurada en settings. "
                "Debe ser una clave de 32 bytes en base64."
            )
        
        try:
            # Decodificar la clave desde base64
            self.key = base64.b64decode(encryption_key)
            if len(self.key) != 32:  # AES-256 requiere 32 bytes
                raise ValueError("La clave debe ser de 32 bytes (256 bits)")
            self.aesgcm = AESGCM(self.key)
        except Exception as e:
            raise ValueError(f"Error al inicializar el cifrado: {e}")
    
    def encrypt(self, plaintext: str) -> str:
        """
        Cifra texto plano usando AES-256-GCM.
        
        Args:
            plaintext: Texto a cifrar
            
        Returns:
            String base64 con formato: nonce(12bytes) + ciphertext + tag(16bytes)
        """
        if not plaintext:
            return ""
        
        # Generar nonce aleatorio de 96 bits (12 bytes) - recomendado para GCM
        nonce = os.urandom(12)
        
        # Cifrar el texto
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext = self.aesgcm.encrypt(nonce, plaintext_bytes, None)
        
        # Combinar nonce + ciphertext+tag y codificar en base64
        encrypted_data = nonce + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Descifra texto cifrado con AES-256-GCM.
        
        Args:
            encrypted_text: String base64 con nonce + ciphertext + tag
            
        Returns:
            Texto plano descifrado
            
        Raises:
            ValueError: Si el texto está corrupto o fue manipulado
        """
        if not encrypted_text:
            return ""
        
        try:
            # Decodificar desde base64
            encrypted_data = base64.b64decode(encrypted_text)
            
            # Extraer nonce (primeros 12 bytes) y ciphertext+tag (resto)
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            
            # Descifrar y verificar integridad
            plaintext_bytes = self.aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext_bytes.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error al descifrar: datos corruptos o manipulados - {e}")


# Instancia global del servicio
_encryption_service = None


def get_encryption_service() -> EncryptionService:
    """
    Obtiene la instancia singleton del servicio de cifrado.
    
    Returns:
        EncryptionService: Instancia del servicio
    """
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService()
    return _encryption_service


def encrypt_field(plaintext: str) -> str:
    """
    Función de conveniencia para cifrar un campo.
    
    Args:
        plaintext: Texto a cifrar
        
    Returns:
        Texto cifrado en base64
    """
    service = get_encryption_service()
    return service.encrypt(plaintext)


def decrypt_field(encrypted_text: str) -> str:
    """
    Función de conveniencia para descifrar un campo.
    
    Args:
        encrypted_text: Texto cifrado en base64
        
    Returns:
        Texto plano
    """
    service = get_encryption_service()
    return service.decrypt(encrypted_text)
