import pickle
import os
from excepciones.excepciones_transporte import PersistenciaException

try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.path.dirname(os.path.abspath("servicios/persistencia_service.py"))

_project_root = os.path.dirname(_script_dir)

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