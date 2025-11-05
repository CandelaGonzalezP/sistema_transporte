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