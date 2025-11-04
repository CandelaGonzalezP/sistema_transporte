from dataclasses import dataclass, field
from entidades.vehiculo import Vehiculo

@dataclass
class Conductor:
    id: str
    nombre: str
    licencia: str
    vehiculo: Vehiculo
    disponible: bool = True