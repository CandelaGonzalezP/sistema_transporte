# ViajeSeguro - Sistema de Gestión de Reservas
**Proyecto:** Candela Gonzalez - ING INF - UM

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
- [Contribuciones](#contribuciones)
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

---

## Tecnologías y Patrones

### Tecnologías

-   **Lenguaje**: Python 3.10+
-   **Clases de Datos**: `dataclasses`
-   **Interfaces**: `abc` (Abstract Base Classes)
-   **Serialización**: `pickle`
-   **Tipado**: `typing` (Type Hints)

### Patrones de Diseño

#### 1. Entity-Service Pattern
Separación completa entre entidades (datos) y servicios (lógica).

#### 2. Dependency Injection (DI)
Todos los servicios reciben dependencias vía constructor (ver `main.py`). Este enfoque se prefiere sobre el patrón Singleton por ser más explícito, flexible y fácil de testear.

#### 3. Factory Pattern
`VehiculoFactory` encapsula la creación de `Auto` y `Camioneta`.

#### 4. Observer Pattern
`FlotaService` (Sujeto) notifica a `AdminService` (Observador) sobre cambios de disponibilidad del conductor.

#### 5. Command Pattern
`CrearReservaComando` encapsula una solicitud de reserva, permitiendo que `HistorialComandos` la ejecute y la deshaga.

---

## Estructura del Proyecto

```
ViajeSeguro/
├── README.md                          # Documentación principal
├── HISTORIAS_USUARIOS.md              # Historias de usuario del proyecto
├── .gitignore                         # Archivos ignorados por Git
├── main.py                            # Punto de entrada de la aplicación
│
├── comandos/                          # Patrón Command
│   ├── __init__.py
│   ├── comando_abc.py                 # Interfaz abstracta de Comando
│   ├── crear_reserva_cmd.py           # Comando concreto: Crear Reserva
│   └── historial_comandos.py          # Invocador (mantiene historial)
│
├── entidades/                         # Entidades de dominio (solo datos)
│   ├── __init__.py
│   ├── cliente.py                     # Cliente (@dataclass)
│   ├── conductor.py                   # Conductor (@dataclass)
│   ├── reserva.py                     # Reserva y EstadoReserva (enum)
│   └── vehiculo.py                    # Vehiculo (ABC), Auto, Camioneta
│
├── excepciones/                       # Manejo de excepciones
│   ├── __init__.py
│   └── excepciones_transporte.py      # Jerarquía de excepciones personalizadas
│
├── observadores/                      # Patrón Observer
│   ├── __init__.py
│   └── observador_abc.py              # Interfaces: Observador y Sujeto
│
├── servicios/                         # Lógica de negocio
│   ├── __init__.py
│   ├── admin_service.py               # Servicio de administración (Observador)
│   ├── flota_service.py               # Servicio de flota (Sujeto)
│   ├── persistencia_service.py        # Persistencia con pickle
│   ├── reserva_service.py             # Servicio de reservas
│   └── vehiculo_factory.py            # Fábrica de vehículos (Factory)
│
└── data/                              # Archivos de persistencia (.dat)
    └── registro_viajes_admin.dat      # (generado en tiempo de ejecución)
```

---

## Modelo de Dominio

### Diagrama de Relaciones

```
Cliente [1] ──── [0..*] Reserva
Reserva [1] ──── [0..1] Conductor
Conductor [1] ──── [1] Vehiculo

FlotaService [1] ──── [0..*] Conductor
FlotaService [1] ──── [0..*] Vehiculo

(Observer)
FlotaService (Sujeto) [1] ──── [0..*] Observador (AdminService)

(Command)
HistorialComandos (Invocador) [1] ──── [0..*] Comando (CrearReservaComando)
CrearReservaComando [1] ──── [1] ReservaService
CrearReservaComando [1] ──── [1] FlotaService
CrearReservaComando [1] ──── [1] Reserva

(Factory)
VehiculoFactory ──(crea)──> Vehiculo
Vehiculo <|── Auto
Vehiculo <|── Camioneta
```

---

## Instalación y Configuración

### Requisitos Previos

-   **Python**: 3.10 o superior

### Instalación

No se requieren paquetes externos (es código Python puro).

1.  **Clona o descarga el repositorio:**
    ```bash
    git clone https://github.com/CandelaGonzalezP/sistema_transporte.git
    cd ViajeSeguro
    ```

2.  **Verifica la estructura:**
    Asegúrate de tener todos los directorios (`comandos/`, `entidades/`, `excepciones/`, `observadores/`, `servicios/`).

3.  **Crea la carpeta de datos (opcional):**
    ```bash
    mkdir data
    ```
    *(El script la creará automáticamente si no existe)*

---

## Guía de Uso

### Ejecutar la Aplicación

Desde la raíz del proyecto (`ViajeSeguro/`):

```bash
python main.py
```

### Salida Esperada

El programa demostrará:

1. **Configuración del Observer**: AdminService se suscribe a FlotaService
2. **Creación de vehículos**: Usando VehiculoFactory (Factory Pattern)
3. **Creación de reserva**: Usando CrearReservaComando (Command Pattern)
4. **Cambios de disponibilidad**: AdminService recibe notificaciones (Observer Pattern)
5. **Asignación de viaje**: AdminService asigna conductor a reserva
6. **Deshacer acción**: Se revierte la creación de la reserva (Command Pattern)
7. **Persistencia**: Se guardan y leen las reservas desde disco

### Ejemplo de Salida

```
==============================================
   Sistema de Transporte 'ViajeSeguro'   
 Patrones: Entity-Service, Factory, Observer, Command
==============================================

1. Configurando Patrón Observer...
Observador AdminService registrado.

2. Creando vehículos con Patrón Factory...
Vehículo Auto ABC-123 agregado.
Vehículo Camioneta DEF-456 agregado.
Conductor Juan Pérez agregado con ID COND-1a2b.
Conductor María López agregado con ID COND-3c4d.
Flota inicializada con 2 conductores.

3. Creando reserva con Patrón Command...
[Comando] Ejecutado: Crear Reserva ID RES-5e6f
Reserva RES-5e6f creada exitosamente.
Estado de la reserva RES-5e6f: PENDIENTE

4. Disparando evento con Patrón Observer...
Conductor 'Juan Pérez' se pone NO DISPONIBLE.
[Sujeto] Notificando a 1 observadores...
------------------------------------------------------
 [PANEL DE ADMIN] ACTUALIZACIÓN EN TIEMPO REAL:
   Conductor: Juan Pérez (ID: COND-1a2b)
   Vehículo:  Auto (ABC-123)
   NUEVO ESTADO: NO DISPONIBLE
------------------------------------------------------

...
```

---

## Documentación Técnica (Patrones)

### Patrón Factory

**Ubicación**: `servicios/vehiculo_factory.py`

**Propósito**: Centralizar la creación de objetos `Vehiculo` sin exponer la lógica de instanciación.

**Ejemplo de uso**:
```python
factory = VehiculoFactory()
auto = factory.crear_vehiculo("Auto", "ABC-123", "Toyota", "Corolla")
camioneta = factory.crear_vehiculo("Camioneta", "DEF-456", "Ford", "Ranger")
```

**Ventajas**:
- Fácil agregar nuevos tipos de vehículos (ej. `Moto`) sin modificar código cliente
- Encapsula la lógica de creación

---

### Patrón Observer

**Ubicación**: `observadores/observador_abc.py`, `servicios/flota_service.py`, `servicios/admin_service.py`

**Participantes**:
- **Sujeto (Observable)**: `FlotaService` - notifica cambios de disponibilidad
- **Observador**: `AdminService` - recibe notificaciones

**Flujo**:
1. AdminService se registra en FlotaService: `flota_service.registrar(admin_service)`
2. Cuando cambia la disponibilidad de un conductor: `flota_service.actualizar_disponibilidad_conductor(id, estado)`
3. FlotaService llama a `notificar(conductor)`
4. AdminService recibe `actualizar(sujeto, conductor)` y muestra panel de actualización

**Ventajas**:
- Desacoplamiento total entre FlotaService y AdminService
- Fácil agregar nuevos observadores (ej. NotificacionService)

---

### Patrón Command

**Ubicación**: `comandos/comando_abc.py`, `comandos/crear_reserva_cmd.py`, `comandos/historial_comandos.py`

**Participantes**:
- **Comando**: `CrearReservaComando` - encapsula la acción
- **Invocador**: `HistorialComandos` - ejecuta y mantiene historial
- **Receptor**: `ReservaService`, `FlotaService` - realizan las acciones

**Flujo**:
1. Se crea el comando: `comando = CrearReservaComando(reserva_service, flota_service, reserva)`
2. Se ejecuta: `historial.ejecutar_comando(comando)`
3. Se deshace: `historial.deshacer_ultimo_comando()`

**Ventajas**:
- Acciones reversibles (undo/redo)
- Historial auditable de operaciones
- Fácil implementar macros o transacciones complejas

---

## Códigos de Error

| Código | Excepción | Descripción |
|--------|-----------|-------------|
| **ERROR 01** | `NoHayConductoresException` | No hay conductores disponibles para asignar |
| **ERROR 02** | `ReservaInvalidaException` | La reserva es inválida (ej. fecha pasada o estado incorrecto) |
| **ERROR 04** | `PersistenciaException` | Error de E/S al escribir en disco |
| **ERROR 05** | `PersistenciaException` | Archivo no encontrado o corrupto al leer |

### Manejo de Errores

Todas las excepciones incluyen:
- **Código de error**: Para logging y debugging
- **Mensaje técnico**: Para desarrolladores
- **Mensaje de usuario**: Para mostrar al usuario final

**Ejemplo**:
```python
try:
    admin_service.asignar_reserva("RES-123", "COND-456")
except NoHayConductoresException as e:
    print(e.get_full_message())  # "ERROR 01 - Conductor ID COND-456 no está disponible."
```

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios siguiendo los patrones existentes
4. Asegúrate de que el código siga la arquitectura Entity-Service
5. Haz commit de tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
6. Push a la rama (`git push origin feature/nueva-funcionalidad`)
7. Abre un Pull Request

### Reglas de Contribución

- Mantener la separación Entity-Service
- Documentar nuevos patrones de diseño
- Agregar excepciones personalizadas cuando sea necesario
- Incluir ejemplos de uso en el código

---

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

```
MIT License

Copyright (c) 2025 Candela Gonzalez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Contacto

**Autora**: Candela Gonzalez  
**Institución**: Universidad de Mendoza - Ingeniería Informática  
**Proyecto**: Sistema ViajeSeguro