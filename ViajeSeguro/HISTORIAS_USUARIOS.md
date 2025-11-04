# Historias de Usuario - ViajeSeguro

## Información del Proyecto
**Proyecto:** ViajeSeguro - Sistema de Gestión de Reservas  
**Autora:** Candela Gonzalez - ING INF - UM  
**Versión:** 1.0  
**Fecha:** Noviembre 2025

---

## Índice
1. [Gestión de Clientes](#gestión-de-clientes)
2. [Gestión de Conductores](#gestión-de-conductores)
3. [Gestión de Vehículos](#gestión-de-vehículos)
4. [Gestión de Reservas](#gestión-de-reservas)
5. [Administración del Sistema](#administración-del-sistema)
6. [Persistencia de Datos](#persistencia-de-datos)

---

## Gestión de Clientes

### HU-01: Registrar Cliente en el Sistema
**Como** cliente nuevo  
**Quiero** registrarme en el sistema proporcionando mi nombre y email  
**Para** poder solicitar servicios de transporte

**Criterios de Aceptación:**
- El cliente debe proporcionar: ID único, nombre completo y email
- El sistema debe validar que el email tenga un formato válido
- El sistema debe generar un ID único para el cliente
- El cliente debe quedar registrado y disponible para crear reservas

**Prioridad:** Alta  
**Estimación:** 2 puntos

---

### HU-02: Crear Reserva de Viaje
**Como** cliente registrado  
**Quiero** crear una reserva indicando origen, destino y fecha/hora  
**Para** solicitar un servicio de transporte

**Criterios de Aceptación:**
- El cliente debe estar registrado en el sistema
- La fecha/hora debe ser futura (no puede ser en el pasado)
- Se debe especificar origen y destino claramente
- La reserva se crea con estado PENDIENTE
- El sistema debe generar un ID único para la reserva (formato: RES-XXXX)
- Si la fecha es pasada, se lanza `ReservaInvalidaException` con código ERROR 02

**Prioridad:** Alta  
**Estimación:** 3 puntos

---

## Gestión de Conductores

### HU-03: Registrar Conductor en la Flota
**Como** administrador  
**Quiero** registrar un conductor con su licencia y vehículo asignado  
**Para** que pueda realizar viajes

**Criterios de Aceptación:**
- El conductor debe proporcionar: nombre, número de licencia
- Se debe asignar un vehículo específico al conductor
- El sistema genera un ID único (formato: COND-XXXX)
- Por defecto, el conductor se registra como "disponible"
- El conductor queda registrado en el FlotaService

**Prioridad:** Alta  
**Estimación:** 3 puntos

---

### HU-04: Actualizar Disponibilidad de Conductor
**Como** conductor  
**Quiero** actualizar mi estado de disponibilidad (disponible/no disponible)  
**Para** indicar si puedo aceptar nuevos viajes

**Criterios de Aceptación:**
- El conductor debe estar registrado en el sistema
- Se puede cambiar el estado entre disponible (true) y no disponible (false)
- El cambio de estado dispara una notificación a todos los observadores (Patrón Observer)
- Los administradores reciben una actualización en tiempo real del cambio
- Si el conductor no existe, se lanza `NoHayConductoresException` con código ERROR 01

**Prioridad:** Alta  
**Estimación:** 3 puntos

---

## Gestión de Vehículos

### HU-05: Crear Vehículo Tipo Auto
**Como** administrador  
**Quiero** crear un vehículo tipo Auto usando la fábrica de vehículos  
**Para** agregarlo a la flota disponible

**Criterios de Aceptación:**
- Se debe usar `VehiculoFactory` para crear el vehículo (Patrón Factory)
- El Auto debe tener: patente, marca, modelo
- La capacidad por defecto es 4 pasajeros
- El vehículo debe implementar los métodos: `get_patente()`, `get_capacidad()`, `get_tipo()`
- El tipo retornado debe ser "Auto"

**Prioridad:** Alta  
**Estimación:** 2 puntos

---

### HU-06: Crear Vehículo Tipo Camioneta
**Como** administrador  
**Quiero** crear un vehículo tipo Camioneta usando la fábrica de vehículos  
**Para** agregarlo a la flota para grupos más grandes

**Criterios de Aceptación:**
- Se debe usar `VehiculoFactory` para crear el vehículo (Patrón Factory)
- La Camioneta debe tener: patente, marca, modelo
- La capacidad por defecto es 7 pasajeros
- El vehículo debe implementar los métodos: `get_patente()`, `get_capacidad()`, `get_tipo()`
- El tipo retornado debe ser "Camioneta"
- La fábrica debe permitir agregar nuevos tipos sin modificar código existente

**Prioridad:** Alta  
**Estimación:** 2 puntos

---

## Gestión de Reservas

### HU-07: Asignar Conductor a Reserva
**Como** administrador  
**Quiero** asignar un conductor disponible a una reserva pendiente  
**Para** que el viaje pueda ser realizado

**Criterios de Aceptación:**
- La reserva debe estar en estado PENDIENTE
- El conductor debe estar DISPONIBLE
- Al asignar, la reserva cambia a estado ASIGNADA
- Se asigna el conductor Y su vehículo a la reserva
- El conductor cambia su disponibilidad a false
- Si no hay conductores disponibles, se lanza `NoHayConductoresException` (ERROR 01)
- Si la reserva ya fue tratada, se lanza `ReservaInvalidaException` (ERROR 02)

**Prioridad:** Alta  
**Estimación:** 5 puntos

---

### HU-08: Cancelar Reserva
**Como** cliente o administrador  
**Quiero** cancelar una reserva existente  
**Para** liberar recursos cuando el viaje ya no es necesario

**Criterios de Aceptación:**
- La reserva debe existir en el sistema
- El estado de la reserva cambia a CANCELADA
- Si se había asignado un conductor, debe ser liberado (disponible = true)
- Si la reserva no existe, se lanza `ReservaInvalidaException` (ERROR 02)

**Prioridad:** Media  
**Estimación:** 3 puntos

---

### HU-09: Ejecutar Comando de Crear Reserva
**Como** administrador  
**Quiero** crear una reserva usando el patrón Command  
**Para** poder deshacer la acción si fue un error

**Criterios de Aceptación:**
- Se debe usar `CrearReservaComando` (Patrón Command)
- El comando encapsula la acción de crear la reserva
- Al ejecutar, se crea la reserva en el sistema
- El comando se guarda en el historial de comandos
- Si falla, se captura `ReservaInvalidaException` y se muestra mensaje amigable

**Prioridad:** Alta  
**Estimación:** 4 puntos

---

### HU-10: Deshacer Última Acción (Undo)
**Como** administrador  
**Quiero** deshacer la última acción ejecutada (ej. crear reserva)  
**Para** corregir errores sin afectar la integridad del sistema

**Criterios de Aceptación:**
- Se debe usar `HistorialComandos.deshacer_ultimo_comando()` (Patrón Command)
- El último comando de la pila se ejecuta en reversa
- Si era una reserva creada, se cancela (estado CANCELADA)
- Si había un conductor asignado, se libera (disponible = true)
- Se notifica a los observadores del cambio de disponibilidad
- Si no hay acciones en el historial, se muestra mensaje informativo
- El comando deshecho se elimina de la pila

**Prioridad:** Alta  
**Estimación:** 5 puntos

---

## Administración del Sistema

### HU-11: Recibir Notificaciones de Disponibilidad en Tiempo Real
**Como** administrador  
**Quiero** recibir notificaciones automáticas cuando cambie la disponibilidad de un conductor  
**Para** tomar decisiones rápidas sobre asignación de viajes

**Criterios de Aceptación:**
- El AdminService debe implementar la interfaz `Observador` (Patrón Observer)
- El AdminService debe estar suscrito al FlotaService (Sujeto)
- Cuando un conductor cambia su disponibilidad, se dispara `notificar()`
- El AdminService recibe los datos: nombre, ID, vehículo y nuevo estado del conductor
- Se muestra un panel visual con la información en consola
- El sistema debe funcionar con múltiples observadores simultáneamente

**Prioridad:** Alta  
**Estimación:** 4 puntos

---

### HU-12: Buscar Conductor Disponible
**Como** administrador  
**Quiero** buscar rápidamente un conductor disponible  
**Para** asignar reservas de forma eficiente

**Criterios de Aceptación:**
- El sistema debe retornar el primer conductor con `disponible = true`
- Si no hay conductores disponibles, retorna `None`
- La búsqueda debe ser eficiente (sin iterar innecesariamente)
- Se puede usar para asignaciones automáticas

**Prioridad:** Media  
**Estimación:** 2 puntos

---

## Persistencia de Datos

### HU-13: Guardar Reservas en Disco
**Como** administrador  
**Quiero** persistir las reservas en disco al finalizar operaciones  
**Para** mantener un registro permanente de los viajes

**Criterios de Aceptación:**
- Se debe usar `PersistenciaService.persistir()` con pickle
- Los datos se guardan en formato binario (.dat)
- Los archivos se guardan en la carpeta `data/` (ruta absoluta)
- Si la carpeta no existe, se crea automáticamente
- Si ocurre un error de E/S, se lanza `PersistenciaException` (ERROR 04)
- Se muestra mensaje de confirmación con la ruta absoluta del archivo

**Prioridad:** Media  
**Estimación:** 3 puntos

---

### HU-14: Cargar Reservas desde Disco
**Como** administrador  
**Quiero** leer reservas previamente guardadas  
**Para** continuar operaciones después de cerrar el sistema

**Criterios de Aceptación:**
- Se debe usar `PersistenciaService.leer()`
- El sistema deserializa los datos usando pickle
- Si el archivo no existe, se lanza `PersistenciaException` (ERROR 05)
- Si el archivo está corrupto, se lanza `PersistenciaException` (ERROR 05)
- Se retorna una lista de objetos `Reserva` completamente reconstituidos
- Se muestra mensaje de confirmación con la cantidad de reservas leídas

**Prioridad:** Media  
**Estimación:** 3 puntos

---

## Historias Técnicas (Arquitectura)

### HU-15: Implementar Arquitectura Entity-Service
**Como** desarrollador  
**Quiero** separar entidades (datos) de servicios (lógica)  
**Para** mantener el código organizado y mantenible

**Criterios de Aceptación:**
- Todas las entidades son `@dataclass` sin lógica de negocio
- Entidades: Cliente, Conductor, Reserva, Vehiculo (Auto, Camioneta)
- Toda la lógica está en servicios: ReservaService, FlotaService, AdminService
- Los servicios reciben entidades como parámetros (no las crean internamente)
- Los servicios se inyectan dependencias vía constructor (Dependency Injection)

**Prioridad:** Alta  
**Estimación:** 8 puntos

---

### HU-16: Manejo Profesional de Excepciones
**Como** desarrollador  
**Quiero** una jerarquía clara de excepciones personalizadas  
**Para** facilitar el debugging y proporcionar mensajes útiles al usuario

**Criterios de Aceptación:**
- Todas las excepciones heredan de `ViajeSeguroException`
- Cada excepción incluye: código de error, mensaje técnico, mensaje para usuario
- Códigos implementados: ERROR 01, ERROR 02, ERROR 04, ERROR 05
- El método `get_full_message()` retorna el formato: "CÓDIGO - Mensaje"
- Las excepciones se capturan y manejan apropiadamente en main.py

**Prioridad:** Alta  
**Estimación:** 3 puntos

---

## Resumen de Prioridades

### Alta Prioridad (Críticas)
- HU-01: Registrar Cliente
- HU-02: Crear Reserva
- HU-03: Registrar Conductor
- HU-04: Actualizar Disponibilidad
- HU-05, HU-06: Crear Vehículos (Factory)
- HU-07: Asignar Conductor
- HU-09, HU-10: Comandos (Command Pattern)
- HU-11: Notificaciones (Observer)
- HU-15, HU-16: Arquitectura y Excepciones

### Media Prioridad
- HU-08: Cancelar Reserva
- HU-12: Buscar Conductor
- HU-13, HU-14: Persistencia

---

## Métricas del Proyecto

**Total de Historias:** 16  
**Puntos Totales Estimados:** 57 puntos  
**Patrones Implementados:** 4 (Factory, Observer, Command, Entity-Service)  
**Cobertura Funcional:** 100% de los requisitos del sistema