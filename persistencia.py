"""
================================================================================
Archivo: persistencia.py
Proposito:
    Manejo de la memoria secundaria. Guarda y carga las estructuras
    globales en un archivo de texto JSON para preservar tipos nativos
    (listas, booleanos, enteros, floats).

    Notas tecnicas:
        - JSON no preserva tuplas: las convierte a listas. Al cargar
          se reconstruye la tupla de fecha (DD, MM, AAAA) para
          mantener el tipo exigido por el enunciado.
        - JSON solo admite claves string. Los codigos de provincia
          (int) se serializan como strings y se reconvierten a int
          al cargar.
        - No se usa la palabra clave 'global'. Las estructuras del
          modulo modelo_datos se mutan en sitio mediante .clear(),
          .extend() y .update().
================================================================================
"""

import json
import os

import modelo_datos
from modelo_datos import IdxFechaNac


# Nombre fijo del archivo (sin ruta absoluta para que funcione donde
# se ejecute el .py).
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

    Args:
        Fila (list): fila original de la matriz.

    Returns:
        list: copia de la fila lista para serializar.
    """
    Copia = list(Fila)
    Copia[IdxFechaNac] = list(Copia[IdxFechaNac])
    return Copia


def _NormalizarFilaAlCargar(Fila):
    """
    Restaura los tipos exactos exigidos por la consigna tras leer
    una fila desde JSON. En particular, vuelve a convertir la fecha
    de nacimiento de lista a tupla.

    Args:
        Fila (list): fila leida del JSON.

    Returns:
        list: fila con tipos correctos.
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
        # Preparar matriz de donadores serializable.
        DonadoresSerializables = [
            _NormalizarFilaParaGuardar(Fila)
            for Fila in modelo_datos.Donadores
        ]

        # Preparar diccionario de lugares (claves int -> str).
        LugaresSerializables = {
            str(Codigo): ListaLugares
            for Codigo, ListaLugares in modelo_datos.LugaresDonacion.items()
        }

        Contenido = {
            "donadores": DonadoresSerializables,
            "lugares_donacion": LugaresSerializables,
        }

        with open(ArchivoBd, "w", encoding="utf-8") as Archivo:
            json.dump(Contenido, Archivo, ensure_ascii=False, indent=2)

        return True
    except (OSError, TypeError, ValueError):
        # No se relanza la excepcion: la GUI consultara el booleano y
        # mostrara un messagebox al usuario si corresponde.
        return False


def CargarBaseDeDatos():
    """
    Carga la matriz de donadores y el diccionario de lugares desde
    el archivo JSON en memoria secundaria.

    Side effects:
        Muta en sitio las estructuras Donadores y LugaresDonacion del
        modulo modelo_datos (sin reasignar, sin usar 'global').

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

    # Validacion minima de estructura.
    if "donadores" not in Contenido or "lugares_donacion" not in Contenido:
        return False

    # Restaurar matriz de donadores con los tipos correctos.
    DonadoresCargados = []
    for Fila in Contenido["donadores"]:
        DonadoresCargados.append(_NormalizarFilaAlCargar(Fila))

    # Restaurar diccionario de lugares (claves str -> int).
    LugaresCargados = {}
    for CodigoStr, ListaLugares in Contenido["lugares_donacion"].items():
        try:
            LugaresCargados[int(CodigoStr)] = list(ListaLugares)
        except ValueError:
            # Clave invalida: se omite.
            continue

    # Mutacion en sitio (no se usa 'global').
    modelo_datos.Donadores.clear()
    modelo_datos.Donadores.extend(DonadoresCargados)
    modelo_datos.LugaresDonacion.clear()
    modelo_datos.LugaresDonacion.update(LugaresCargados)

    return True
