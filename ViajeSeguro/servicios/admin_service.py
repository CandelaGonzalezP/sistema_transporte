from ViajeSeguro.observadores.observador_abc import Observador
from .flota_service import FlotaService 
from .reserva_service import ReservaService 
from ViajeSeguro.entidades.conductor import Conductor
from ViajeSeguro.excepciones.excepciones_transporte import NoHayConductoresException, ReservaInvalidaException
from typing import Any

class AdminService(Observador):
    """
    Servicio de administración.
    Actúa como OBSERVADOR en el patrón Observer.
    """

    def __init__(self, flota_service: FlotaService, reserva_service: ReservaService):
        self._flota_service = flota_service
        self._reserva_service = reserva_service

    def asignar_reserva(self, reserva_id: str, conductor_id: str):
        """Lógica de negocio del Administrador."""
        conductor = self._flota_service.buscar_conductor(conductor_id)
        if not conductor:
            raise NoHayConductoresException(f"Conductor ID {conductor_id} no existe.")
        
        if not conductor.disponible:
            raise NoHayConductoresException(f"Conductor {conductor.nombre} no está disponible.")
            
        try:
            self._reserva_service.asignar_conductor(reserva_id, conductor)
            self._flota_service.actualizar_disponibilidad_conductor(conductor_id, False)
        except ReservaInvalidaException as e:
            raise e # Relanzamos


    def actualizar(self, sujeto: Any, conductor: Conductor):
        """
        Este método es llamado por el Sujeto (FlotaService) cuando hay un cambio.
        """
        estado = "DISPONIBLE" if conductor.disponible else "NO DISPONIBLE"
        print("------------------------------------------------------")
        print(f" [PANEL DE ADMIN] ACTUALIZACIÓN EN TIEMPO REAL:")
        print(f"   Conductor: {conductor.nombre} (ID: {conductor.id})")
        print(f"   Vehículo:  {conductor.vehiculo.get_tipo()} ({conductor.vehiculo.get_patente()})")
        print(f"   NUEVO ESTADO: {estado}")
        print("------------------------------------------------------")