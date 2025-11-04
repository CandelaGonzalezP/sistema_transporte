import enum
from dataclasses import dataclass, field
from datetime import datetime
from entidades.cliente import Cliente
from entidades.conductor import Conductor
from entidades.vehiculo import Vehiculo
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