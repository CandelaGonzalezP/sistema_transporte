import uuid
from datetime import datetime
from entidades.reserva import Reserva, EstadoReserva
from entidades.cliente import Cliente
from entidades.conductor import Conductor
from excepciones.excepciones_transporte import ReservaInvalidaException

class ReservaService:
    """Servicio que maneja la lógica de negocio de las reservas."""
    
    def __init__(self):
        self._reservas: dict[str, Reserva] = {}

    def crear_entidad_reserva(self, cliente: Cliente, fecha_hora: datetime, origen: str, destino: str) -> Reserva:
        """Crea la entidad Reserva (pero no la guarda)."""
        reserva_id = f"RES-{uuid.uuid4().hex[:4]}"
        return Reserva(
            id=reserva_id,
            cliente=cliente,
            fecha_hora=fecha_hora,
            origen=origen,
            destino=destino
        )

    def crear_reserva(self, reserva: Reserva):
        """Guarda la reserva en el sistema."""
        if reserva.fecha_hora < datetime.now():
            raise ReservaInvalidaException("La fecha de reserva no puede ser en el pasado.")
        
        if reserva.id in self._reservas and self._reservas[reserva.id].estado == EstadoReserva.CANCELADA:
             self._reservas[reserva.id].estado = EstadoReserva.PENDIENTE
             self._reservas[reserva.id].conductor = None 
             self._reservas[reserva.id].vehiculo = None
        else:
             self._reservas[reserva.id] = reserva


    def asignar_conductor(self, reserva_id: str, conductor: Conductor):
        reserva = self.buscar_reserva(reserva_id)
        if not reserva:
            raise ReservaInvalidaException(f"Reserva ID {reserva_id} no encontrada.")
            
        if reserva.estado != EstadoReserva.PENDIENTE:
            raise ReservaInvalidaException(f"La reserva {reserva_id} ya ha sido tratada (Estado: {reserva.estado.name}).")
            
        reserva.conductor = conductor
        reserva.vehiculo = conductor.vehiculo
        reserva.estado = EstadoReserva.ASIGNADA

    def cancelar_reserva(self, reserva_id: str):
        reserva = self.buscar_reserva(reserva_id)
        if not reserva:
            raise ReservaInvalidaException(f"Reserva ID {reserva_id} no encontrada.")
        
        reserva.estado = EstadoReserva.CANCELADA

    def buscar_reserva(self, reserva_id: str) -> Reserva | None:
        return self._reservas.get(reserva_id)

    def get_reservas(self) -> list[Reserva]:
        return list(self._reservas.values())