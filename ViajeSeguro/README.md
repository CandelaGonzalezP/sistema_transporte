# ViajeSeguro - Sistema de Gestión de Reservas

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Architecture](https://img.shields.io/badge/Arquitectura-Entity--Service-blue?style=flat)
![Patterns](https://img.shields.io/badge/Patrones-Factory%2C%20Observer%2C%20Command-green?style=flat)
![Status](https://img.shields.io/badge/Estado-Desarrollo-success?style=flat)

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Contexto del Proyecto](#contexto-del-proyecto)
- [Características Principales](#características-principales)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Tecnologías y Patrones](#tecnologías-y-patrones)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelo de Dominio](#modelo-de-dominio)
- [Instalación y Configuración](#instalación-y-configuración)
- [Guía de Uso](#guía-de-uso)
- [Documentación Técnica (Patrones)](#documentación-técnica-patrones)
- [Códigos de Error](#códigos-de-error)
- [Licencia](#licencia)

---

## Descripción General

**ViajeSeguro** es un sistema integral de gestión de transporte (tipo *ride-sharing*) desarrollado en Python que permite administrar clientes, conductores, flotas de vehículos y reservas.

El sistema proporciona herramientas para:

-   Gestión de clientes y conductores.
-   Creación polimórfica de vehículos (Autos, Camionetas) usando el patrón Factory.
-   Sistema de reservas transaccional (crear, cancelar, deshacer) usando el patrón Command.
-   Monitoreo en tiempo real de la disponibilidad de conductores usando el patrón Observer.
-   Asignación de viajes por parte de administradores.
-   Persistencia de datos de reservas en disco usando `pickle`.

El proyecto implementa un patrón arquitectónico **Entity-Service** estricto (adaptado a Python) e incorpora los patrones de diseño clave solicitados para un código mantenible, escalable y robusto.

---

## Contexto del Proyecto

### ¿Qué problema resuelve?

En la gestión de servicios de transporte modernos, es crítico contar con un sistema que permita:

1.  **Control preciso de la flota**: Gestionar qué conductores están disponibles y qué vehículos están operativos.
2.  **Asignación eficiente**: Asignar reservas a conductores disponibles de forma rápida y confiable.
3.  **Trazabilidad**: Mantener un registro de todas las reservas, cancelaciones y acciones del sistema.
4.  **Flexibilidad de vehículos**: Poder agregar nuevos tipos de vehículos (autos, camionetas, motos) sin refactorizar el sistema (**Factory**).
5.  **Disponibilidad en Tiempo Real**: Notificar a los administradores cuando un conductor está listo para un nuevo viaje (**Observer**).
6.  **Acciones reversibles**: Permitir a los administradores deshacer acciones, como una reserva creada por error (**Command**).

### ¿Para quién está diseñado?

-   **Clientes**: Reservar viajes para fechas y destinos específicos.
-   **Conductores**: Ver sus viajes asignados y gestionar su estado de disponibilidad.
-   **Administradores**: Asignar vehículos y conductores según la demanda y monitorear el estado del sistema.

### Caso de Uso Principal

Un **Cliente** necesita reservar un viaje. Un **Administrador** ve la reserva pendiente y la asigna a un **Conductor** que figura como "Disponible" en el sistema. Cuando el Conductor cambia su estado (ej. termina un viaje), el Administrador es notificado en tiempo real (**Observer**). Si el Cliente cancela o el admin comete un error, se puede usar la función de deshacer (**Command**) para revertir la creación de la reserva.

---

## Características Principales

### 1. Gestión de Flota Polimórfica (Patrón Factory)

-   **Jerarquía de vehículos**: `Vehiculo` (ABC) con implementaciones `Auto` y `Camioneta`.
-   **Creación centralizada**: `VehiculoFactory` (`servicios/vehiculo_factory.py`) se encarga de instanciar los vehículos, permitiendo agregar nuevos tipos (ej. `Moto`) fácilmente sin tocar el código que lo utiliza.

### 2. Disponibilidad en Tiempo Real (Patrón Observer)

-   **Sujeto (Observable)**: `FlotaService` implementa la interfaz `Sujeto`. Mantiene la lista de conductores y notifica a los observadores cuando un conductor cambia su estado.
-   **Observador (Observer)**: `AdminService` implementa la interfaz `Observador`. Se suscribe a `FlotaService` y recibe actualizaciones instantáneas (en consola) cuando un conductor cambia su estado.
-   **Desacoplamiento**: El `FlotaService` (Sujeto) no sabe quién es el `AdminService` (Observador), solo sabe que debe notificar a su lista de observadores.

### 3. Gestión de Reservas Transaccional (Patrón Command)

-   **Acciones como Objetos**: Acciones como "Crear Reserva" son encapsuladas como objetos (`CrearReservaComando`).
-   **Historial de Comandos**: `HistorialComandos` (Invocador) mantiene una pila (`list`) de acciones ejecutadas.
-   **Deshacer (Undo)**: El sistema puede invocar `historial.deshacer_ultimo_comando()`, que llama al método `deshacer()` del último comando (ej. cancelando una reserva que se acaba de crear y liberando al conductor).

### 4. Manejo Profesional de Excepciones

Jerarquía completa de excepciones personalizadas (`excepciones/excepciones_transporte.py`):

-   `ViajeSeguroException` (base): Incluye código de error y mensaje para usuario.
-   `NoHayConductoresException`: Cuando se intenta asignar una reserva y no hay conductores.
-   `ReservaInvalidaException`: Cuando una reserva tiene datos incorrectos (ej. fecha pasada).
-   `PersistenciaException`: Errores de lectura/escritura de archivos.

### 5. Arquitectura Entity-Service

-   **Entidades**: Clases de datos puras (usando `@dataclass`) en `entidades/` (Cliente, Conductor, Reserva) que solo contienen estado.
-   **Servicios**: Toda la lógica de negocio en `servicios/` (ReservaService, FlotaService, AdminService).

---

## Arquitectura del Sistema

### Patrón Entity-Service (Adaptado a Python)

El proyecto sigue estrictamente el patrón **Entity-Service** que separa:

-   **Entidades (Dataclasses)**: Contienen **solo estado** (datos). Son "tontos" y no contienen lógica de negocio. Se definen en `entidades/`.
-   **Servicios (Clases de lógica)**: Contienen **toda la lógica**, validaciones, orquestación de patrones y manejo de excepciones. Se definen en `servicios/`.

### Beneficios de esta Arquitectura

✅ **Separación de responsabilidades**: El código es más limpio y organizado.
✅ **Testabilidad**: Los servicios son fáciles de probar de forma aislada (podríamos "inyectar" entidades falsas).
✅ **Mantenibilidad**: Cambios en la lógica (ej. cómo se asigna un conductor) no afectan la estructura de datos (la `Reserva`).
✅ **Escalabilidad**: Fácil agregar nuevas reglas de negocio o nuevos servicios.

### Diagrama de Patrones de Diseño

