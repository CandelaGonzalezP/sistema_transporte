import uuid
from typing import Optional
from entidades.conductor import Conductor
from entidades.vehiculo import Vehiculo
from observadores.observador_abc import Sujeto, Observador
from excepciones.excepciones_transporte import NoHayConductoresException

class FlotaService(Sujeto):
    """
    Servicio que gestiona la flota de conductores y vehículos.
    Actúa como SUJETO (Observable) en el patrón Observer.
    """
    
    def __init__(self):
        self._vehiculos: list[Vehiculo] = []
        self._conductores: dict[str, Conductor] = {}
        self._observadores: list[Observador] = []

    @property
    def conductores(self) -> list[Conductor]:
        return list(self._conductores.values())

    
    def agregar_vehiculo(self, vehiculo: Vehiculo):
        self._vehiculos.append(vehiculo)
        print(f"Vehículo {vehiculo.get_tipo()} {vehiculo.patente} agregado.")

    def agregar_conductor(self, nombre: str, licencia: str, vehiculo: Vehiculo) -> Conductor:
        conductor_id = f"COND-{uuid.uuid4().hex[:4]}"
        conductor = Conductor(id=conductor_id, nombre=nombre, licencia=licencia, vehiculo=vehiculo)
        self._conductores[conductor.id] = conductor
        print(f"Conductor {nombre} agregado con ID {conductor_id}.")
        return conductor

    def actualizar_disponibilidad_conductor(self, conductor_id: str, disponible: bool):
        conductor = self._conductores.get(conductor_id)
        if conductor:
            conductor.disponible = disponible
            self.notificar(conductor)
        else:
            raise NoHayConductoresException(f"Conductor ID {conductor_id} no encontrado.")
            
    def buscar_conductor(self, conductor_id: str) -> Optional[Conductor]:
        return self._conductores.get(conductor_id)

    def get_conductor_disponible(self) -> Optional[Conductor]:
        for conductor in self._conductores.values():
            if conductor.disponible:
                return conductor
        return None


    def registrar(self, observador: Observador):
        self._observadores.append(observador)
        print(f"Observador {observador.__class__.__name__} registrado.")

    def remover(self, observador: Observador):
        self._observadores.remove(observador)

    def notificar(self, conductor: Conductor):
        """Notifica a todos los observadores sobre un cambio en el conductor."""
        print(f"[Sujeto] Notificando a {len(self._observadores)} observadores...")
        for observador in self._observadores:
            observador.actualizar(self, conductor)