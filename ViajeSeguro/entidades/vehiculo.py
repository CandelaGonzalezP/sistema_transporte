from abc import ABC, abstractmethod
from dataclasses import dataclass

class Vehiculo(ABC):
    @abstractmethod 
    def get_patente(self) -> str:
        pass

    @abstractmethod  
    def get_capacidad(self) -> int:
        pass

    @abstractmethod 
    def get_tipo(self) -> str:
        pass

@dataclass
class Auto(Vehiculo):
    patente: str
    marca: str
    modelo: str
    capacidad: int = 4 

    def get_patente(self) -> str:
        return self.patente

    def get_capacidad(self) -> int:
        return self.capacidad
    
    def get_tipo(self) -> str:
        return "Auto"

@dataclass
class Camioneta(Vehiculo):
    patente: str
    marca: str
    modelo: str
    capacidad: int = 7 

    def get_patente(self) -> str:
        return self.patente

    def get_capacidad(self) -> int:
        return self.capacidad
    
    def get_tipo(self) -> str:
        return "Camioneta"