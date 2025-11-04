from comandos.comando_abc import Comando
from excepciones.excepciones_transporte import ViajeSeguroException

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
         