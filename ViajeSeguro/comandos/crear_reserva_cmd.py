from comandos.comando_abc import Comando
from servicios.reserva_service import ReservaService
from servicios.flota_service import FlotaService  
from entidades.reserva import Reserva
from excepciones.excepciones_transporte import ReservaInvalidaException

class CrearReservaComando(Comando):
    """Comando para crear y deshacer la creación de una reserva."""
    
    def __init__(self, reserva_service: ReservaService, flota_service: FlotaService, reserva: Reserva): 
        self._reserva_service = reserva_service
        self._flota_service = flota_service  
        self._reserva = reserva
        
    def ejecutar(self):
        """Ejecuta la creación de la reserva."""
        try:
            self._reserva_service.crear_reserva(self._reserva)
            print(f"[Comando] Ejecutado: Crear Reserva ID {self._reserva.id}")
        except ReservaInvalidaException as e:
            print(f"[Comando] Falló al ejecutar: {e.get_full_message()}")
            raise e 

    def deshacer(self):
        """Deshace la creación (cancelando la reserva) Y LIBERA AL CONDUCTOR."""
        try:
            conductor_asignado = self._reserva.conductor
            
            self._reserva_service.cancelar_reserva(self._reserva.id)
            print(f"[Comando] Deshecho: Cancelar Reserva ID {self._reserva.id}")

            if conductor_asignado:
                print(f"[Comando] Liberando al conductor {conductor_asignado.nombre} en FlotaService...")
                self._flota_service.actualizar_disponibilidad_conductor(conductor_asignado.id, True)

        except (ReservaInvalidaException) as e:
            print(f"[Comando] Falló al deshacer: {e.get_full_message()}")
            raise e