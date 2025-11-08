"""
Campo de modelo Django personalizado para almacenar datos cifrados.

Utiliza AES-256-GCM para cifrado transparente en la capa de aplicación.
"""

from django.db import models
from core.encryption import encrypt_field, decrypt_field


class EncryptedTextField(models.TextField):
    """
    Campo de texto que cifra/descifra automáticamente usando AES-256-GCM.
    
    Los datos se cifran antes de guardar en la base de datos y se descifran
    automáticamente al recuperarlos. El cifrado es transparente para el código
    de la aplicación.
    
    Uso:
        class MyModel(models.Model):
            sensitive_data = EncryptedTextField(blank=True)
    """
    
    description = "Campo de texto cifrado con AES-256-GCM"
    
    def from_db_value(self, value, expression, connection):
        """
        Convierte el valor de la base de datos a Python (descifra).
        
        Args:
            value: Valor cifrado desde la base de datos
            
        Returns:
            Texto plano descifrado
        """
        if value is None:
            return value
        if value == "":
            return ""
        
        try:
            return decrypt_field(value)
        except Exception as e:
            # Log del error pero retorna vacío para evitar crasheos
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error descifrando campo: {e}")
            return ""
    
    def to_python(self, value):
        """
        Convierte el valor a Python (para formularios y validación).
        
        Args:
            value: Valor del campo
            
        Returns:
            Texto plano
        """
        if isinstance(value, str) or value is None:
            return value
        return str(value)
    
    def get_prep_value(self, value):
        """
        Prepara el valor para guardarlo en la base de datos (cifra).
        
        Args:
            value: Texto plano
            
        Returns:
            Texto cifrado en base64
        """
        if value is None:
            return value
        if value == "":
            return ""
        
        # Cifrar el valor antes de guardarlo
        return encrypt_field(str(value))
