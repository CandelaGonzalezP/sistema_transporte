from entidades.vehiculo import Vehiculo, Auto, Camioneta

class VehiculoFactory:
    """Patrón Factory: Centraliza la creación de vehículos."""
    
    def crear_vehiculo(self, tipo: str, patente: str, marca: str, modelo: str) -> Vehiculo:
        if tipo.lower() == "auto":
            return Auto(patente=patente, marca=marca, modelo=modelo)
        elif tipo.lower() == "camioneta":
            return Camioneta(patente=patente, marca=marca, modelo=modelo)
        else:
            raise ValueError(f"Tipo de vehículo desconocido: {tipo}")