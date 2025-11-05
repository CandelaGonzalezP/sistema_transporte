"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: C:\Users\cande\sistema_transporte\.\ViajeSeguro\
Fecha de generacion: 2025-11-05 08:19:28
Total de archivos integrados: 21
Total de directorios procesados: 6
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. __init__.py
#   2. main.py
#
# DIRECTORIO: comandos
#   3. __init__.py
#   4. comando_abc.py
#   5. crear_reserva_cmd.py
#   6. historial_comandos.py
#
# DIRECTORIO: entidades
#   7. __init__.py
#   8. cliente.py
#   9. conductor.py
#   10. reserva.py
#   11. vehiculo.py
#
# DIRECTORIO: excepciones
#   12. __init__.py
#   13. excepciones_transporte.py
#
# DIRECTORIO: observadores
#   14. __init__.py
#   15. observador_abc.py
#
# DIRECTORIO: servicios
#   16. __init__.py
#   17. admin_service.py
#   18. flota_service.py
#   19. persistencia_service.py
#   20. reserva_service.py
#   21. vehiculo_factory.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/21: __init__.py
# Directorio: .
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 2/21: main.py
# Directorio: .
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\main.py
# ==============================================================================

import os
from datetime import datetime, timedelta
from ViajeSeguro.entidades.cliente import Cliente
from ViajeSeguro.excepciones.excepciones_transporte import ViajeSeguroException, PersistenciaException
from ViajeSeguro.servicios.vehiculo_factory import VehiculoFactory
from ViajeSeguro.servicios.flota_service import FlotaService
from ViajeSeguro.servicios.reserva_service import ReservaService
from ViajeSeguro.servicios.admin_service import AdminService
from ViajeSeguro.servicios.persistencia_service import PersistenciaService
from ViajeSeguro.comandos.historial_comandos import HistorialComandos
from ViajeSeguro.comandos.crear_reserva_cmd import CrearReservaComando

def main():
    """
    Función principal que orquesta el sistema 'ViajeSeguro'
    demostrando los patrones de diseño.
    """
    try:
        print("==============================================")
        print("   Sistema de Transporte 'ViajeSeguro' (Python)")
        print(" Patrones: Entity-Service, Factory, Observer, Command")
        print("==============================================\n")

        # ============================================
        # 1. INICIALIZAR SERVICIOS (Inyección de Dependencias)
        # ============================================

        # Servicios base y Patrones
        vehiculo_factory = VehiculoFactory()       # <-- PATRÓN FACTORY
        flota_service = FlotaService()             # <-- PATRÓN OBSERVER (Sujeto)
        reserva_service = ReservaService()
        historial_comandos = HistorialComandos()   # <-- PATRÓN COMMAND (Invocador)
        persistencia_service = PersistenciaService()

        admin_service = AdminService(flota_service, reserva_service) # <-- PATRÓN OBSERVER (Observador)

        # ============================================
        # 2. CONFIGURAR PATRÓN OBSERVER
        # ============================================
        print("1. Configurando Patrón Observer...")
        flota_service.registrar(admin_service)

        # ============================================
        # 3. USAR PATRÓN FACTORY
        # ============================================
        print("\n2. Creando vehículos con Patrón Factory...")
        auto1 = vehiculo_factory.crear_vehiculo("Auto", "ABC-123", "Toyota", "Corolla")
        camioneta1 = vehiculo_factory.crear_vehiculo("Camioneta", "DEF-456", "Ford", "Ranger")

        flota_service.agregar_vehiculo(auto1)
        flota_service.agregar_vehiculo(camioneta1)

        conductor1 = flota_service.agregar_conductor("Juan Pérez", "L-12345", auto1)
        conductor2 = flota_service.agregar_conductor("María López", "L-67890", camioneta1)
        print(f"Flota inicializada con {len(flota_service.conductores)} conductores.")

        # ============================================
        # 4. CREAR CLIENTE Y USAR PATRÓN COMMAND
        # ============================================
        print("\n3. Creando reserva con Patrón Command...")
        cliente1 = Cliente(id="C1", nombre="Ana García", email="ana@mail.com")

        reserva1 = reserva_service.crear_entidad_reserva(
            cliente1,
            datetime.now() + timedelta(days=1),
            "Calle Falsa 123",
            "Avenida Siempre Viva 742"
        )

        comando_crear = CrearReservaComando(reserva_service, flota_service, reserva1) 

        historial_comandos.ejecutar_comando(comando_crear)
        print(f"Reserva {reserva1.id} creada exitosamente.")
        print(f"Estado de la reserva {reserva1.id}: {reserva_service.buscar_reserva(reserva1.id).estado.name}")

        # ============================================
        # 5. USAR PATRÓN OBSERVER (Disparar evento)
        # ============================================
        print("\n4. Disparando evento con Patrón Observer...")
        print(f"Conductor '{conductor1.nombre}' se pone NO DISPONIBLE.")
        flota_service.actualizar_disponibilidad_conductor(conductor1.id, False)

        print(f"\nConductor '{conductor2.nombre}' se pone DISPONIBLE.")
        flota_service.actualizar_disponibilidad_conductor(conductor2.id, True)

        # ============================================
        # 6. ASIGNAR VIAJE
        # ============================================
        print("\n5. Administrador asigna la reserva...")
        admin_service.asignar_reserva(reserva1.id, conductor2.id)
        print(f"Reserva {reserva1.id} asignada a {conductor2.nombre}.")
        print(f"Estado de la reserva {reserva1.id}: {reserva_service.buscar_reserva(reserva1.id).estado.name}")

        # ============================================
        # 7. DESHACER CON PATRÓN COMMAND
        # ============================================
        print("\n6. Deshaciendo última acción con Patrón Command...")
        historial_comandos.deshacer_ultimo_comando()
        print(f"Acción 'Crear Reserva {reserva1.id}' deshecha.")
        print(f"Estado de la reserva {reserva1.id}: {reserva_service.buscar_reserva(reserva1.id).estado.name}")

        # ============================================
        # 8. PERSISTENCIA
        # ============================================
        print("\n7. Persistiendo reservas...")
        comando_crear_2 = CrearReservaComando(reserva_service, flota_service, reserva1) 
        historial_comandos.ejecutar_comando(comando_crear_2)
        
        admin_service.asignar_reserva(reserva1.id, conductor2.id)
        print(f"Reserva {reserva1.id} re-asignada a {conductor2.nombre}.")
        
        nombre_archivo = "registro_viajes_admin"
        persistencia_service.persistir(nombre_archivo, reserva_service.get_reservas())

        print("\n8. Leyendo registro persistido...")
        reservas_leidas = persistencia_service.leer(nombre_archivo)
        print(f"Reservas recuperadas: {len(reservas_leidas)}")
        for r in reservas_leidas:
            print(f"  - Reserva ID: {r.id}, Estado: {r.estado.name}, Conductor: {r.conductor.nombre}")

        print("\n==============================================")
        print("   EJEMPLO COMPLETADO EXITOSAMENTE")
        print("==============================================")

    except ViajeSeguroException as e:
        print("\n--- ERROR DE NEGOCIO ---")
        print(e.get_full_message())
    except PersistenciaException as e:
        print("\n--- ERROR DE PERSISTENCIA ---")
        print(e.get_full_message())
        if e.__cause__:
            print(f"Causa raíz: {e.__cause__}")
    except Exception as e:
        print(f"\n--- ERROR INESPERADO ---")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


################################################################################
# DIRECTORIO: comandos
################################################################################

# ==============================================================================
# ARCHIVO 3/21: __init__.py
# Directorio: comandos
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 4/21: comando_abc.py
# Directorio: comandos
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\comando_abc.py
# ==============================================================================

from abc import ABC, abstractmethod
from ..excepciones.excepciones_transporte import ViajeSeguroException 

class Comando(ABC):
    @abstractmethod
    def ejecutar(self):
        """Ejecuta la acción del comando."""
        pass

    @abstractmethod
    def deshacer(self):
        """Revierte la acción del comando."""
        pass

# ==============================================================================
# ARCHIVO 5/21: crear_reserva_cmd.py
# Directorio: comandos
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\crear_reserva_cmd.py
# ==============================================================================

from .comando_abc import Comando 
from ..servicios.reserva_service import ReservaService 
from ..servicios.flota_service import FlotaService  
from ..entidades.reserva import Reserva 
from ..excepciones.excepciones_transporte import ReservaInvalidaException 

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

# ==============================================================================
# ARCHIVO 6/21: historial_comandos.py
# Directorio: comandos
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\historial_comandos.py
# ==============================================================================

from .comando_abc import Comando 
from ViajeSeguro.excepciones.excepciones_transporte import ViajeSeguroException


class HistorialComandos:
    """Invocador del patrón Command. Mantiene una pila de comandos."""
    
    def __init__(self):
        self._historial: list[Comando] = []

    def ejecutar_comando(self, comando: Comando):
        """Ejecuta un comando y lo guarda en el historial."""
        try:
            comando.ejecutar()
            self._historial.append(comando)
        except ViajeSeguroException:
            pass 

    def deshacer_ultimo_comando(self):
        """Deshace el último comando ejecutado."""
        if not self._historial:
            print("No hay acciones para deshacer.")
            return

        try:
            ultimo_comando = self._historial.pop()
            ultimo_comando.deshacer()
        except ViajeSeguroException as e:
            print(f"Error al deshacer: {e.get_full_message()}")


################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 7/21: __init__.py
# Directorio: entidades
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 8/21: cliente.py
# Directorio: entidades
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\cliente.py
# ==============================================================================

from dataclasses import dataclass

@dataclass
class Cliente:
    id: str
    nombre: str
    email: str

# ==============================================================================
# ARCHIVO 9/21: conductor.py
# Directorio: entidades
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\conductor.py
# ==============================================================================

from dataclasses import dataclass, field
from .vehiculo import Vehiculo 

@dataclass
class Conductor:
    id: str
    nombre: str
    licencia: str
    vehiculo: Vehiculo
    disponible: bool = True

# ==============================================================================
# ARCHIVO 10/21: reserva.py
# Directorio: entidades
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\reserva.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 11/21: vehiculo.py
# Directorio: entidades
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\entidades\vehiculo.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 12/21: __init__.py
# Directorio: excepciones
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\excepciones\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 13/21: excepciones_transporte.py
# Directorio: excepciones
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\excepciones\excepciones_transporte.py
# ==============================================================================

class ViajeSeguroException(Exception):
    """Excepción base para todas las excepciones del sistema."""
    def __init__(self, message, error_code, user_message):
        super().__init__(message)
        self.error_code = error_code
        self.user_message = user_message
    
    def get_full_message(self):
        return f"{self.error_code} - {self.user_message}"

class NoHayConductoresException(ViajeSeguroException):
    """Lanzada cuando no hay conductores disponibles para asignar."""
    def __init__(self, message="No hay conductores disponibles"):
        super().__init__(message, "ERROR 01", message)

class ReservaInvalidaException(ViajeSeguroException):
    """Lanzada cuando una reserva es inválida (ej. fecha pasada)."""
    def __init__(self, message="La reserva es inválida"):
        super().__init__(message, "ERROR 02", message)

class PersistenciaException(ViajeSeguroException):
    """Lanzada durante errores de E/S (lectura/escritura)."""
    def __init__(self, message, tipo_operacion, cause=None):
        if tipo_operacion == "LECTURA":
            code = "ERROR 05"
        else:
            code = "ERROR 04" 
            
        super().__init__(message, code, f"Error de {tipo_operacion}: {message}")
        self.tipo_operacion = tipo_operacion
        self.__cause__ = cause


################################################################################
# DIRECTORIO: observadores
################################################################################

# ==============================================================================
# ARCHIVO 14/21: __init__.py
# Directorio: observadores
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\observadores\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 15/21: observador_abc.py
# Directorio: observadores
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\observadores\observador_abc.py
# ==============================================================================

from abc import ABC, abstractmethod
from ViajeSeguro.entidades.conductor import Conductor
from typing import Any

class Observador(ABC):
    @abstractmethod
    def actualizar(self, sujeto: Any, conductor: Conductor):
        """Recibe la actualización del sujeto."""
        pass

class Sujeto(ABC):
    @abstractmethod
    def registrar(self, observador: Observador):
        """Registra un observador."""
        pass
    
    @abstractmethod
    def remover(self, observador: Observador):
        """Remueve un observador."""
        pass
    
    @abstractmethod
    def notificar(self, conductor: Conductor):
        """Notifica a todos los observadores."""
        pass


################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 16/21: __init__.py
# Directorio: servicios
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 17/21: admin_service.py
# Directorio: servicios
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\admin_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 18/21: flota_service.py
# Directorio: servicios
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\flota_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 19/21: persistencia_service.py
# Directorio: servicios
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\persistencia_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 20/21: reserva_service.py
# Directorio: servicios
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\reserva_service.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 21/21: vehiculo_factory.py
# Directorio: servicios
# Ruta completa: C:\Users\cande\sistema_transporte\.\ViajeSeguro\servicios\vehiculo_factory.py
# ==============================================================================

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


################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 21
# Generado: 2025-11-05 08:19:28
################################################################################
