"""
================================================================================
Tarea Programada #2 - Donemos Sangre, demos vida...
Taller de Programacion - I Semestre 2026

Integrantes:
    - Cristhoper Jara Salazar
    - Diego Kim

Archivo: archivos.py
Proposito:
    Manejo de la memoria secundaria. Este es uno de los 3 archivos
    que componen el proyecto (junto con funciones.py y principal.py).
    Aqui se concentran las operaciones de lectura y escritura de la
    base de datos en formato JSON.

    Convencion de codigo:
        - Variables, funciones y parametros en NombreCamello.
        - Sin uso de la palabra clave 'global'. Las estructuras del
          modulo de funciones se mutan en sitio mediante .clear(),
          .extend() y .update().

    Notas tecnicas:
        - JSON no preserva tuplas: las convierte a listas. Al cargar
          se reconstruye la tupla de fecha (DD, MM, AAAA) para
          mantener el tipo exigido por el enunciado.
        - JSON solo admite claves string. Los codigos de provincia
          (int) se serializan como strings y se reconvierten a int
          al cargar.
================================================================================
"""

import json
import os

import funciones
from funciones import IdxFechaNac


# Nombre fijo del archivo de base de datos.
ArchivoBd = "banco_de_sangre.json"


def ExisteArchivoBd():
    """
    Verifica si el archivo de base de datos existe en el directorio
    de trabajo actual.

    Returns:
        bool: True si el archivo existe.
    """
    return os.path.isfile(ArchivoBd)


def _NormalizarFilaParaGuardar(Fila):
    """
    Convierte una fila de la matriz de donadores a una version
    serializable en JSON. La fecha de nacimiento (tupla) se convierte
    a lista para poder serializarla.
    """
    Copia = list(Fila)
    Copia[IdxFechaNac] = list(Copia[IdxFechaNac])
    return Copia


def _NormalizarFilaAlCargar(Fila):
    """
    Restaura los tipos exactos exigidos por la consigna tras leer
    una fila desde JSON. En particular, vuelve a convertir la fecha
    de nacimiento de lista a tupla.
    """
    Fila[IdxFechaNac] = tuple(Fila[IdxFechaNac])
    return Fila


def GuardarBaseDeDatos():
    """
    Persiste la matriz de donadores y el diccionario de lugares al
    archivo JSON.

    Returns:
        bool: True si se guardo correctamente, False si hubo error.
    """
    try:
        DonadoresSerializables = [
            _NormalizarFilaParaGuardar(Fila)
            for Fila in funciones.Donadores
        ]
        LugaresSerializables = {
            str(Codigo): ListaLugares
            for Codigo, ListaLugares in funciones.LugaresDonacion.items()
        }
        Contenido = {
            "donadores": DonadoresSerializables,
            "lugares_donacion": LugaresSerializables,
        }
        with open(ArchivoBd, "w", encoding="utf-8") as Archivo:
            json.dump(Contenido, Archivo, ensure_ascii=False, indent=2)
        return True
    except (OSError, TypeError, ValueError):
        return False


def CargarBaseDeDatos():
    """
    Carga la matriz de donadores y el diccionario de lugares desde
    el archivo JSON en memoria secundaria.

    Side effects:
        Muta en sitio las estructuras Donadores y LugaresDonacion del
        modulo funciones (sin reasignar, sin usar 'global').

    Returns:
        bool: True si se cargo correctamente; False si el archivo no
              existe o esta corrupto.
    """
    if not ExisteArchivoBd():
        return False
    try:
        with open(ArchivoBd, "r", encoding="utf-8") as Archivo:
            Contenido = json.load(Archivo)
    except (OSError, json.JSONDecodeError):
        return False
    if "donadores" not in Contenido or "lugares_donacion" not in Contenido:
        return False

    DonadoresCargados = []
    for Fila in Contenido["donadores"]:
        DonadoresCargados.append(_NormalizarFilaAlCargar(Fila))

    LugaresCargados = {}
    for CodigoStr, ListaLugares in Contenido["lugares_donacion"].items():
        try:
            LugaresCargados[int(CodigoStr)] = list(ListaLugares)
        except ValueError:
            continue

    # Mutacion en sitio (no se usa 'global').
    funciones.Donadores.clear()
    funciones.Donadores.extend(DonadoresCargados)
    funciones.LugaresDonacion.clear()
    funciones.LugaresDonacion.update(LugaresCargados)
    return True
