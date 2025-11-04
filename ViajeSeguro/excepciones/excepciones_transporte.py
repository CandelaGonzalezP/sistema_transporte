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