"""
Archivo integrador generado automaticamente
Directorio: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios
Fecha: 2025-11-05 08:19:28
Total de archivos integrados: 6
"""

# ================================================================================
# ARCHIVO 1/6: __init__.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/6: admin_service.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\admin_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/6: flota_service.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\flota_service.py
# ================================================================================

import uuid
from typing import Optional
from ViajeSeguro.entidades.conductor import Conductor
from ViajeSeguro.entidades.vehiculo import Vehiculo
from ViajeSeguro.observadores.observador_abc import Sujeto, Observador
from ViajeSeguro.excepciones.excepciones_transporte import NoHayConductoresException

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

# ================================================================================
# ARCHIVO 4/6: persistencia_service.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\persistencia_service.py
# ================================================================================

import pickle
import os
from ViajeSeguro.excepciones.excepciones_transporte import PersistenciaException

try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.path.dirname(os.path.abspath("ViajeSeguro/servicios/persistencia_service.py"))

_viajeseguro_root = os.path.dirname(_script_dir)

_project_root = os.path.dirname(_viajeseguro_root)

_BASE_DIR_ABS = os.path.join(_project_root, "data")


class PersistenciaService:
    """
    Servicio para persistir (guardar) y leer (cargar) datos de disco.
    Usa 'pickle' (serialización de Python).
    
    Utiliza rutas absolutas para ser independiente del directorio de trabajo.
    """
    
    BASE_DIR = _BASE_DIR_ABS 

    def __init__(self):
        os.makedirs(self.BASE_DIR, exist_ok=True)

    def _get_path(self, nombre_archivo: str) -> str:
        return os.path.join(self.BASE_DIR, f"{nombre_archivo}.dat")

    def persistir(self, nombre_archivo: str, datos: any):
        """Serializa y guarda datos en un archivo."""
        ruta = self._get_path(nombre_archivo)
        
        try:
            with open(ruta, 'wb') as f:
                pickle.dump(datos, f)
            print(f"Datos guardados exitosamente en {os.path.abspath(ruta)}")
            
        except IOError as e:
            raise PersistenciaException(
                message=f"Error de E/S al escribir en {ruta}",
                tipo_operacion="ESCRITURA",
                cause=e
            )

    def leer(self, nombre_archivo: str) -> any:
        """Lee y deserializa datos de un archivo."""
        ruta = self._get_path(nombre_archivo)

        if not os.path.exists(ruta):
            raise PersistenciaException(
                message=f"Archivo no encontrado: {ruta}",
                tipo_operacion="LECTURA",
                cause=FileNotFoundError()
            )

        try:
            with open(ruta, 'rb') as f:
                datos = pickle.load(f)
            print(f"Datos leídos exitosamente de {os.path.abspath(ruta)}")
            return datos
            
        except (IOError, pickle.PickleError, EOFError) as e:
            raise PersistenciaException(
                message=f"Error de E/S o archivo corrupto al leer {ruta}",
                tipo_operacion="LECTURA",
                cause=e
            )

# ================================================================================
# ARCHIVO 5/6: reserva_service.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\reserva_service.py
# ================================================================================

import uuid
from datetime import datetime
from ViajeSeguro.entidades.reserva import Reserva, EstadoReserva
from ViajeSeguro.entidades.cliente import Cliente
from ViajeSeguro.entidades.conductor import Conductor
from ViajeSeguro.excepciones.excepciones_transporte import ReservaInvalidaException

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

# ================================================================================
# ARCHIVO 6/6: vehiculo_factory.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\vehiculo_factory.py
# ================================================================================

from ViajeSeguro.entidades.vehiculo import Vehiculo, Auto, Camioneta

class VehiculoFactory:
    """Patrón Factory: Centraliza la creación de vehículos."""
    
    def crear_vehiculo(self, tipo: str, patente: str, marca: str, modelo: str) -> Vehiculo:
        if tipo.lower() == "auto":
            return Auto(patente=patente, marca=marca, modelo=modelo)
        elif tipo.lower() == "camioneta":
            return Camioneta(patente=patente, marca=marca, modelo=modelo)
        else:
            raise ValueError(f"Tipo de vehículo desconocido: {tipo}")

