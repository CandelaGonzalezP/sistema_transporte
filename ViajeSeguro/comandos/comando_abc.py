from abc import ABC, abstractmethod
from excepciones.excepciones_transporte import ViajeSeguroException

class Comando(ABC):
    @abstractmethod
    def ejecutar(self):
        """Ejecuta la acción del comando."""
        pass

    @abstractmethod
    def deshacer(self):
        """Revierte la acción del comando."""
        pass