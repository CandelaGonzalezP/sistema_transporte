"""
Archivo integrador generado automaticamente
Directorio: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades
Fecha: 2025-11-05 08:19:28
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: cliente.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\cliente.py
# ================================================================================

from dataclasses import dataclass

@dataclass
class Cliente:
    id: str
    nombre: str
    email: str

# ================================================================================
# ARCHIVO 3/5: conductor.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\conductor.py
# ================================================================================

from dataclasses import dataclass, field
from .vehiculo import Vehiculo 

@dataclass
class Conductor:
    id: str
    nombre: str
    licencia: str
    vehiculo: Vehiculo
    disponible: bool = True

# ================================================================================
# ARCHIVO 4/5: reserva.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\reserva.py
# ================================================================================

import enum
from dataclasses import dataclass, field
from datetime import datetime
from .cliente import Cliente 
from .conductor import Conductor 
from .vehiculo import Vehiculo 
from typing import Optional

class EstadoReserva(enum.Enum):
    PENDIENTE = 1
    ASIGNADA = 2
    EN_CURSO = 3
    COMPLETADA = 4
    CANCELADA = 5

@dataclass
class Reserva:
    id: str
    cliente: Cliente
    fecha_hora: datetime
    origen: str
    destino: str
    estado: EstadoReserva = EstadoReserva.PENDIENTE
    conductor: Optional[Conductor] = None
    vehiculo: Optional[Vehiculo] = None

# ================================================================================
# ARCHIVO 5/5: vehiculo.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\vehiculo.py
# ================================================================================

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

