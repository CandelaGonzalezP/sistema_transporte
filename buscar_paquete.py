"""
Script para buscar el paquete python_forestacion desde el directorio raiz del proyecto.
Incluye funcionalidad para integrar archivos Python en cada nivel del arbol de directorios.
"""
import os
import sys
from datetime import datetime


def buscar_paquete(directorio_raiz: str, nombre_paquete: str) -> list:
    """
    Busca un paquete Python en el directorio raiz y subdirectorios.

    Args:
        directorio_raiz: Directorio desde donde iniciar la busqueda
        nombre_paquete: Nombre del paquete a buscar

    Returns:
        Lista de rutas donde se encontro el paquete
    """
    paquetes_encontrados = []

    for raiz, directorios, archivos in os.walk(directorio_raiz):
        # Verificar si el directorio actual es el paquete buscado
        nombre_dir = os.path.basename(raiz)

        if nombre_dir == nombre_paquete:
            # Verificar que sea un paquete Python (contiene __init__.py)
            if '__init__.py' in archivos:
                paquetes_encontrados.append(raiz)
                print(f"[+] Paquete encontrado: {raiz}")
            else:
                print(f"[!] Directorio encontrado pero no es un paquete Python: {raiz}")

    return paquetes_encontrados


def obtener_archivos_python(directorio: str) -> list:
    """
    Obtiene todos los archivos Python en un directorio (sin recursion).

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de archivos .py
    """
    archivos_python = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isfile(ruta_completa) and item.endswith('.py'):
                # Excluir archivos integradores para evitar recursion infinita
                if item not in ['integrador.py', 'integradorFinal.py']:
                    archivos_python.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(archivos_python)


def obtener_subdirectorios(directorio: str) -> list:
    """
    Obtiene todos los subdirectorios inmediatos de un directorio.

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de subdirectorios
    """
    subdirectorios = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isdir(ruta_completa):
                # Excluir directorios especiales
                if not item.startswith('.') and item not in ['__pycache__', 'venv', '.venv']:
                    subdirectorios.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(subdirectorios)


def leer_contenido_archivo(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo Python.

    Args:
        ruta_archivo: Ruta completa del archivo

    Returns:
        Contenido del archivo como string
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as error:
        print(f"[!] Error al leer {ruta_archivo}: {error}")
        return f"# Error al leer este archivo: {error}\n"


def crear_archivo_integrador(directorio: str, archivos_python: list) -> bool:
    """
    Crea un archivo integrador.py con el contenido de todos los archivos Python.

    Args:
        directorio: Directorio donde crear el archivo integrador
        archivos_python: Lista de rutas de archivos Python a integrar

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_python:
        return False

    ruta_integrador = os.path.join(directorio, 'integrador.py')

    try:
        with open(ruta_integrador, 'w', encoding='utf-8') as integrador:
            # Encabezado
            integrador.write('"""\n')
            integrador.write(f"Archivo integrador generado automaticamente\n")
            integrador.write(f"Directorio: {directorio}\n")
            integrador.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador.write(f"Total de archivos integrados: {len(archivos_python)}\n")
            integrador.write('"""\n\n')

            # Integrar cada archivo
            for idx, archivo in enumerate(archivos_python, 1):
                nombre_archivo = os.path.basename(archivo)
                integrador.write(f"# {'=' * 80}\n")
                integrador.write(f"# ARCHIVO {idx}/{len(archivos_python)}: {nombre_archivo}\n")
                integrador.write(f"# Ruta: {archivo}\n")
                integrador.write(f"# {'=' * 80}\n\n")

                contenido = leer_contenido_archivo(archivo)
                integrador.write(contenido)
                integrador.write("\n\n")

        print(f"[OK] Integrador creado: {ruta_integrador}")
        print(f"     Archivos integrados: {len(archivos_python)}")
        return True

    except Exception as error:
        print(f"[!] Error al crear integrador en {directorio}: {error}")
        return False


def procesar_directorio_recursivo(directorio: str, nivel: int = 0, archivos_totales: list = None) -> list:
    """
    Procesa un directorio de forma recursiva, creando integradores en cada nivel.
    Utiliza DFS (Depth-First Search) para llegar primero a los niveles mas profundos.

    Args:
        directorio: Directorio a procesar
        nivel: Nivel de profundidad actual (para logging)
        archivos_totales: Lista acumulativa de todos los archivos procesados

    Returns:
        Lista de todos los archivos Python procesados en el arbol
    """
    if archivos_totales is None:
        archivos_totales = []

    indentacion = "  " * nivel
    print(f"{indentacion}[INFO] Procesando nivel {nivel}: {os.path.basename(directorio)}")

    # Obtener subdirectorios
    subdirectorios = obtener_subdirectorios(directorio)

    # Primero, procesar recursivamente todos los subdirectorios (DFS)
    for subdir in subdirectorios:
        procesar_directorio_recursivo(subdir, nivel + 1, archivos_totales)

    # Despues de procesar subdirectorios, procesar archivos del nivel actual
    archivos_python = obtener_archivos_python(directorio)

    if archivos_python:
        print(f"{indentacion}[+] Encontrados {len(archivos_python)} archivo(s) Python")
        crear_archivo_integrador(directorio, archivos_python)
        # Agregar archivos a la lista total
        archivos_totales.extend(archivos_python)
    else:
        print(f"{indentacion}[INFO] No hay archivos Python en este nivel")

    return archivos_totales


def crear_integrador_final(directorio_raiz: str, archivos_totales: list) -> bool:
    """
    Crea un archivo integradorFinal.py con TODO el codigo fuente de todas las ramas.

    Args:
        directorio_raiz: Directorio donde crear el archivo integrador final
        archivos_totales: Lista completa de todos los archivos Python procesados

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_totales:
        print("[!] No hay archivos para crear el integrador final")
        return False

    ruta_integrador_final = os.path.join(directorio_raiz, 'integradorFinal.py')

    # Organizar archivos por directorio para mejor estructura
    archivos_por_directorio = {}
    for archivo in archivos_totales:
        directorio = os.path.dirname(archivo)
        if directorio not in archivos_por_directorio:
            archivos_por_directorio[directorio] = []
        archivos_por_directorio[directorio].append(archivo)

    try:
        with open(ruta_integrador_final, 'w', encoding='utf-8') as integrador_final:
            # Encabezado principal
            integrador_final.write('"""\n')
            integrador_final.write("INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write(f"Directorio raiz: {directorio_raiz}\n")
            integrador_final.write(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write(f"Total de archivos integrados: {len(archivos_totales)}\n")
            integrador_final.write(f"Total de directorios procesados: {len(archivos_por_directorio)}\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write('"""\n\n')

            # Tabla de contenidos
            integrador_final.write("# " + "=" * 78 + "\n")
            integrador_final.write("# TABLA DE CONTENIDOS\n")
            integrador_final.write("# " + "=" * 78 + "\n\n")

            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)
                    integrador_final.write(f"#   {contador_global}. {nombre_archivo}\n")
                    contador_global += 1
                integrador_final.write("#\n")

            integrador_final.write("\n\n")

            # Contenido completo organizado por directorio
            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)

                # Separador de directorio
                integrador_final.write("\n" + "#" * 80 + "\n")
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                integrador_final.write("#" * 80 + "\n\n")

                # Procesar cada archivo del directorio
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)

                    integrador_final.write(f"# {'=' * 78}\n")
                    integrador_final.write(f"# ARCHIVO {contador_global}/{len(archivos_totales)}: {nombre_archivo}\n")
                    integrador_final.write(f"# Directorio: {dir_relativo}\n")
                    integrador_final.write(f"# Ruta completa: {archivo}\n")
                    integrador_final.write(f"# {'=' * 78}\n\n")

                    contenido = leer_contenido_archivo(archivo)
                    integrador_final.write(contenido)
                    integrador_final.write("\n\n")

                    contador_global += 1

            # Footer
            integrador_final.write("\n" + "#" * 80 + "\n")
            integrador_final.write("# FIN DEL INTEGRADOR FINAL\n")
            integrador_final.write(f"# Total de archivos: {len(archivos_totales)}\n")
            integrador_final.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write("#" * 80 + "\n")

        print(f"\n[OK] Integrador final creado: {ruta_integrador_final}")
        print(f"     Total de archivos integrados: {len(archivos_totales)}")
        print(f"     Total de directorios procesados: {len(archivos_por_directorio)}")

        # Mostrar tamanio del archivo
        tamanio = os.path.getsize(ruta_integrador_final)
        if tamanio < 1024:
            tamanio_str = f"{tamanio} bytes"
        elif tamanio < 1024 * 1024:
            tamanio_str = f"{tamanio / 1024:.2f} KB"
        else:
            tamanio_str = f"{tamanio / (1024 * 1024):.2f} MB"
        print(f"     Tamanio del archivo: {tamanio_str}")

        return True

    except Exception as error:
        print(f"[!] Error al crear integrador final: {error}")
        return False


def integrar_arbol_directorios(directorio_raiz: str) -> None:
    """
    Inicia el proceso de integracion para todo el arbol de directorios.

    Args:
        directorio_raiz: Directorio raiz desde donde comenzar
    """
    print("\n" + "=" * 80)
    print("INICIANDO INTEGRACION DE ARCHIVOS PYTHON")
    print("=" * 80)
    print(f"Directorio raiz: {directorio_raiz}\n")

    # Procesar directorios y obtener lista de todos los archivos
    archivos_totales = procesar_directorio_recursivo(directorio_raiz)

    print("\n" + "=" * 80)
    print("INTEGRACION POR NIVELES COMPLETADA")
    print("=" * 80)

    # Crear integrador final con todos los archivos
    if archivos_totales:
        print("\n" + "=" * 80)
        print("CREANDO INTEGRADOR FINAL")
        print("=" * 80)
        crear_integrador_final(directorio_raiz, archivos_totales)

    print("\n" + "=" * 80)
    print("PROCESO COMPLETO FINALIZADO")
    print("=" * 80)


def main():
    """Funcion principal del script."""
    # Obtener el directorio raiz del proyecto (donde esta este script)
    directorio_raiz = os.path.dirname(os.path.abspath(__file__))

    # Verificar argumentos de linea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()

        if comando == "integrar":
            # Modo de integracion de archivos
            if len(sys.argv) > 2:
                directorio_objetivo = sys.argv[2]
                if not os.path.isabs(directorio_objetivo):
                    directorio_objetivo = os.path.join(directorio_raiz, directorio_objetivo)
            else:
                directorio_objetivo = directorio_raiz

            if not os.path.isdir(directorio_objetivo):
                print(f"[!] El directorio no existe: {directorio_objetivo}")
                return 1

            integrar_arbol_directorios(directorio_objetivo)
            return 0

        elif comando == "help" or comando == "--help" or comando == "-h":
            print("Uso: python buscar_paquete.py [COMANDO] [OPCIONES]")
            print("")
            print("Comandos disponibles:")
            print("  (sin argumentos)     Busca el paquete python_forestacion")
            print("  integrar [DIR]       Integra archivos Python en el arbol de directorios")
            print("                       DIR: directorio raiz (por defecto: directorio actual)")
            print("  help                 Muestra esta ayuda")
            print("")
            print("Ejemplos:")
            print("  python buscar_paquete.py")
            print("  python buscar_paquete.py integrar")
            print("  python buscar_paquete.py integrar python_forestacion")
            return 0

        else:
            print(f"[!] Comando desconocido: {comando}")
            print("    Use 'python buscar_paquete.py help' para ver los comandos disponibles")
            return 1

    # Modo por defecto: buscar paquete
    print(f"[INFO] Buscando desde: {directorio_raiz}")
    print(f"[INFO] Buscando paquete: python_forestacion")
    print("")

    # Buscar el paquete
    paquetes = buscar_paquete(directorio_raiz, "python_forestacion")

    print("")
    if paquetes:
        print(f"[OK] Se encontraron {len(paquetes)} paquete(s):")
        for paquete in paquetes:
            print(f"  - {paquete}")

            # Mostrar estructura basica del paquete
            print(f"    Contenido:")
            try:
                contenido = os.listdir(paquete)
                for item in sorted(contenido)[:10]:  # Mostrar primeros 10 items
                    ruta_item = os.path.join(paquete, item)
                    if os.path.isdir(ruta_item):
                        print(f"      [DIR]  {item}")
                    else:
                        print(f"      [FILE] {item}")
                if len(contenido) > 10:
                    print(f"      ... y {len(contenido) - 10} items mas")
            except PermissionError:
                print(f"      [!] Sin permisos para leer el directorio")
    else:
        print("[!] No se encontro el paquete python_forestacion")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())