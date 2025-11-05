from dataclasses import dataclass, field
from .vehiculo import Vehiculo 

@dataclass
class Conductor:
    id: str
    nombre: str
    licencia: str
    vehiculo: Vehiculo
    disponible: bool = True