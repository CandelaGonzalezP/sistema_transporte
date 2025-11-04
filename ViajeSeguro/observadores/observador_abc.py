from abc import ABC, abstractmethod
from entidades.conductor import Conductor
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