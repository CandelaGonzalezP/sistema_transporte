"""
Archivo integrador generado automaticamente
Directorio: C:\Users\cande\sistema_transporte\.\ViajeSeguro\observadores
Fecha: 2025-11-05 08:19:28
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\observadores\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: observador_abc.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\observadores\observador_abc.py
# ================================================================================

from abc import ABC, abstractmethod
from ViajeSeguro.entidades.conductor import Conductor
from typing import Any

class Observador(ABC):
    @abstractmethod
    def actualizar(self, sujeto: Any, conductor: Conductor):
        """Recibe la actualización del sujeto."""
        pass

class Sujeto(ABC):
    @abstractmethod
    def registrar(self, observador: Observador):
        """Registra un observador."""
        pass
    
    @abstractmethod
    def remover(self, observador: Observador):
        """Remueve un observador."""
        pass
    
    @abstractmethod
    def notificar(self, conductor: Conductor):
        """Notifica a todos los observadores."""
        pass

