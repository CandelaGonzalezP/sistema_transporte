"""
Archivo integrador generado automaticamente
Directorio: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos
Fecha: 2025-11-05 08:19:28
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: comando_abc.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\comando_abc.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/4: crear_reserva_cmd.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\crear_reserva_cmd.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 4/4: historial_comandos.py
# Ruta: C:\Users\cande\sistema_transporte\.\ViajeSeguro\comandos\historial_comandos.py
# ================================================================================

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

