"""
================================================================================
Archivo: reportes.py
Proposito:
    Generacion de los 8 reportes en HTML5 exigidos por el enunciado:

      1. Donantes por provincia (ordenados por nombre completo).
      2. Por rango de edad (18-65).
      3. Por tipo de sangre de una provincia dada.
      4. Lista completa de donadores (ordenada por provincia).
      5. Mujeres donantes O- menores de 45 anios (ordenadas por edad).
      6. A quien puede donar (ascendente por provincia).
      7. De quien puede recibir (descendente por provincia).
      8. Donantes NO activos (con justificacion completa).
      + Reporte de Lugares de donacion.

    Todos los archivos se generan en la misma carpeta del programa,
    sobrescribiendo el anterior si ya existe.

    Convencion de codigo:
        - Variables y constantes en NombreCamello.
        - Sin uso de 'global'.
        - Cada funcion publica devuelve True/False segun si pudo
          escribir el archivo.
================================================================================
"""

from datetime import datetime

import modelo_datos
from modelo_datos import (
    Donadores,
    Provincias,
    TiposDeSangre,
    IdxNombre,
    IdxCedula,
    IdxTipoSangre,
    IdxSexo,
    IdxFechaNac,
    IdxPeso,
    IdxCorreo,
    IdxTelefono,
    IdxEstado,
    IdxJustificacion,
)
from validaciones import (
    CalcularEdad,
    CedulaIntAStr,
    CedulaACodigoProvincia,
)
from logica_negocio import (
    IndiceATipoSangre,
    NombreProvincia,
    TipoSangreAIndice,
    JustificacionCompleta,
    PuedeDonarA,
    PuedeRecibirDe,
)


# ----------------------------------------------------------------------
# Plantilla HTML5 base.
# ----------------------------------------------------------------------
PlantillaHtml = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <title>{Titulo}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 24px;
                background-color: #fafafa; color: #222; }}
        header {{ border-bottom: 3px solid #b00; padding-bottom: 8px;
                  margin-bottom: 16px; }}
        h1 {{ color: #b00; margin: 0; }}
        .fecha {{ color: #555; font-size: 0.9em; }}
        table {{ border-collapse: collapse; width: 100%;
                 background-color: white; }}
        th, td {{ border: 1px solid #999; padding: 6px 10px;
                  text-align: left; }}
        th {{ background-color: #b00; color: white; }}
        tr:nth-child(even) td {{ background-color: #f4f4f4; }}
        footer {{ margin-top: 24px; font-size: 0.85em; color: #777;
                  text-align: center; border-top: 1px solid #ccc;
                  padding-top: 8px; }}
        .sin-datos {{ font-style: italic; color: #777; padding: 12px; }}
    </style>
</head>
<body>
    <header>
        <h1>{Titulo}</h1>
        <p class="fecha">Generado el {FechaHora}</p>
    </header>
    <section>
        <article>
            {Contenido}
        </article>
    </section>
    <footer>
        Banco Nacional de Sangre - Donar sangre, es donar vida
    </footer>
</body>
</html>
"""


# ----------------------------------------------------------------------
# Helpers privados
# ----------------------------------------------------------------------

def _FechaHoraActual():
    """Devuelve fecha/hora del sistema formateada."""
    return datetime.now().strftime("%d/%m/%Y a las %H:%M:%S")


def _FormatearFecha(Tupla):
    """Convierte tupla (DD, MM, AAAA) en string 'DD/MM/AAAA'."""
    Dia, Mes, Anio = Tupla
    return f"{Dia:02d}/{Mes:02d}/{Anio:04d}"


def _NombreCompleto(ListaNombre):
    """Une [nombre, ap1, ap2] en un solo string."""
    return " ".join(ListaNombre)


def _SexoATexto(EsHombre):
    """Convierte bool a 'Masculino'/'Femenino'."""
    return "Masculino" if EsHombre else "Femenino"


def _ConstruirTablaHtml(Encabezados, Filas):
    """Construye <table> o mensaje 'sin datos'."""
    if not Filas:
        return '<p class="sin-datos">No hay registros que mostrar.</p>'

    HtmlEncabezados = "".join(f"<th>{T}</th>" for T in Encabezados)

    LineasFilas = []
    for Fila in Filas:
        Celdas = "".join(f"<td>{C}</td>" for C in Fila)
        LineasFilas.append(f"<tr>{Celdas}</tr>")

    return ("<table>"
            f"<thead><tr>{HtmlEncabezados}</tr></thead>"
            f"<tbody>{''.join(LineasFilas)}</tbody>"
            "</table>")


def _ConstruirHtml(Titulo, Encabezados, Filas):
    """Arma el HTML5 final."""
    Contenido = _ConstruirTablaHtml(Encabezados, Filas)
    return PlantillaHtml.format(
        Titulo=Titulo,
        FechaHora=_FechaHoraActual(),
        Contenido=Contenido,
    )


def _EscribirArchivo(NombreArchivo, ContenidoHtml):
    """Escribe el archivo HTML."""
    try:
        with open(NombreArchivo, "w", encoding="utf-8") as Archivo:
            Archivo.write(ContenidoHtml)
        return True
    except OSError:
        return False


def _FiltrarActivos():
    """Devuelve lista de pares (indice, fila) de donadores activos."""
    return [
        (Indice, Fila)
        for Indice, Fila in enumerate(Donadores)
        if Fila[IdxEstado] == 1
    ]


# ----------------------------------------------------------------------
# REPORTE 1: Donantes activos por provincia (ordenados por nombre).
# ----------------------------------------------------------------------
def ReporteDonantesPorProvincia(CodigoProvincia):
    """
    Donantes activos de la provincia indicada, ordenados por nombre.
    Columnas: Cedula, Nombre completo, Fecha nac, Telefono, Correo.
    """
    DonadoresFiltrados = []
    for _, Fila in _FiltrarActivos():
        CedulaStr = CedulaIntAStr(Fila[IdxCedula])
        if CedulaACodigoProvincia(CedulaStr) == CodigoProvincia:
            DonadoresFiltrados.append(Fila)

    DonadoresFiltrados.sort(key=lambda F: _NombreCompleto(F[IdxNombre]))

    FilasReporte = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for F in DonadoresFiltrados
    ]

    Titulo = (f"Donantes activos de la provincia de "
              f"{NombreProvincia(CodigoProvincia)}")
    Encabezados = ["Cedula", "Nombre completo", "Fecha de nacimiento",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteDonantesPorProvincia.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE 2: Por rango de edad (18-65).
# ----------------------------------------------------------------------
def ReportePorRangoEdad(EdadInicial, EdadFinal=None):
    """Donantes activos cuya edad este en [EdadInicial, EdadFinal]."""
    if EdadFinal is None:
        EdadFinal = EdadInicial

    EdadMin = max(18, min(EdadInicial, EdadFinal))
    EdadMax = min(65, max(EdadInicial, EdadFinal))

    Filtrados = []
    for _, F in _FiltrarActivos():
        D, M, A = F[IdxFechaNac]
        E = CalcularEdad(D, M, A)
        if EdadMin <= E <= EdadMax:
            Filtrados.append((E, F))

    Filtrados.sort(key=lambda Par: Par[0])

    FilasReporte = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for _, F in Filtrados
    ]

    if EdadInicial == EdadFinal:
        Titulo = f"Donantes activos con {EdadInicial} anios de edad"
    else:
        Titulo = (f"Donantes activos entre {EdadInicial} y "
                  f"{EdadFinal} anios de edad")

    Encabezados = ["Cedula", "Nombre completo", "Fecha de nacimiento",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReportePorRangoEdad.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE 3: Por tipo de sangre y provincia.
# ----------------------------------------------------------------------
def ReportePorTipoYProvincia(TipoSangreStr, CodigoProvincia):
    """Donantes activos del tipo de sangre y provincia indicadas."""
    IndiceTipo = TipoSangreAIndice(TipoSangreStr)
    if IndiceTipo == -1:
        return False

    Filtrados = []
    for _, F in _FiltrarActivos():
        if F[IdxTipoSangre] != IndiceTipo:
            continue
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        if CedulaACodigoProvincia(CedulaStr) == CodigoProvincia:
            Filtrados.append(F)

    Filtrados.sort(key=lambda F: _NombreCompleto(F[IdxNombre]))

    FilasReporte = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for F in Filtrados
    ]

    Titulo = (f"Donantes activos {TipoSangreStr} en "
              f"{NombreProvincia(CodigoProvincia)}")
    Encabezados = ["Cedula", "Nombre completo", "Fecha de nacimiento",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReportePorTipoYProvincia.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE 4: Lista completa ordenada por provincia.
# ----------------------------------------------------------------------
def ReporteListaCompleta():
    """Todos los donantes activos ordenados por provincia."""
    Anotados = []
    for _, F in _FiltrarActivos():
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Anotados.append((Codigo, F))

    Anotados.sort(key=lambda Par: (Par[0],
                                   _NombreCompleto(Par[1][IdxNombre])))

    FilasReporte = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         _FormatearFecha(F[IdxFechaNac]),
         f"{F[IdxPeso]:.1f} kg",
         _SexoATexto(F[IdxSexo]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for _, F in Anotados
    ]

    Titulo = "Lista completa de donantes activos (ordenada por provincia)"
    Encabezados = ["Cedula", "Nombre completo", "Tipo de sangre",
                   "Fecha de nacimiento", "Peso", "Sexo", "Telefono",
                   "Correo"]
    return _EscribirArchivo("ReporteListaCompleta.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE 5: Mujeres donantes O- menores de 45 (ordenadas por edad).
# ----------------------------------------------------------------------
def ReporteMujeresONegativo():
    """Mujeres activas O- con edad < 45, ordenadas por edad asc."""
    IndiceONeg = TipoSangreAIndice("O-")

    Candidatas = []
    for _, F in _FiltrarActivos():
        if F[IdxSexo] is True:           # Masculino: excluir
            continue
        if F[IdxTipoSangre] != IndiceONeg:
            continue
        D, M, A = F[IdxFechaNac]
        E = CalcularEdad(D, M, A)
        if E < 45:
            Candidatas.append((E, F))

    Candidatas.sort(key=lambda Par: Par[0])

    FilasReporte = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for _, F in Candidatas
    ]

    Titulo = "Mujeres donantes O- menores de 45 anios"
    Encabezados = ["Cedula", "Nombre completo", "Fecha de nacimiento",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteMujeresONegativo.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE 6: A quien puede donar (asc por provincia).
# ----------------------------------------------------------------------
def ReporteAQuienPuedeDonar(TipoSangreStr):
    """Donadores activos del tipo dado, ordenados asc por provincia."""
    IndiceTipo = TipoSangreAIndice(TipoSangreStr)
    if IndiceTipo == -1:
        return False
    if TipoSangreStr not in PuedeDonarA:
        return False
    Destinos = ", ".join(PuedeDonarA[TipoSangreStr])

    Candidatos = []
    for _, F in _FiltrarActivos():
        if F[IdxTipoSangre] != IndiceTipo:
            continue
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Candidatos.append((Codigo, F))

    Candidatos.sort(key=lambda Par: (Par[0],
                                     _NombreCompleto(Par[1][IdxNombre])))

    FilasReporte = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for _, F in Candidatos
    ]

    Titulo = (f"Donantes {TipoSangreStr}: pueden donar a "
              f"{Destinos} (orden ascendente por provincia)")
    Encabezados = ["Cedula", "Nombre completo", "Tipo de sangre",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteAQuienPuedeDonar.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE 7: De quien puede recibir (desc por provincia).
# ----------------------------------------------------------------------
def ReporteDeQuienPuedeRecibir(TipoSangreStr):
    """Donadores activos del tipo dado, ordenados desc por provincia."""
    IndiceTipo = TipoSangreAIndice(TipoSangreStr)
    if IndiceTipo == -1:
        return False
    if TipoSangreStr not in PuedeRecibirDe:
        return False
    Origenes = ", ".join(PuedeRecibirDe[TipoSangreStr])

    Candidatos = []
    for _, F in _FiltrarActivos():
        if F[IdxTipoSangre] != IndiceTipo:
            continue
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Candidatos.append((Codigo, F))

    Candidatos.sort(key=lambda Par: (-Par[0],
                                     _NombreCompleto(Par[1][IdxNombre])))

    FilasReporte = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for _, F in Candidatos
    ]

    Titulo = (f"Donantes {TipoSangreStr}: pueden recibir de "
              f"{Origenes} (orden descendente por provincia)")
    Encabezados = ["Cedula", "Nombre completo", "Tipo de sangre",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteDeQuienPuedeRecibir.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE 8: Donantes NO activos con justificacion completa.
# ----------------------------------------------------------------------
def ReporteDonantesNoActivos():
    """Donantes inactivos con la explicacion completa de su justificacion."""
    Inactivos = [F for F in Donadores if F[IdxEstado] == 0]
    Inactivos.sort(key=lambda F: (F[IdxJustificacion],
                                  _NombreCompleto(F[IdxNombre])))

    FilasReporte = [
        [JustificacionCompleta(F[IdxJustificacion]),
         CedulaIntAStr(F[IdxCedula]),
         _NombreCompleto(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         _FormatearFecha(F[IdxFechaNac]),
         f"{F[IdxPeso]:.1f} kg",
         _SexoATexto(F[IdxSexo]),
         F[IdxTelefono],
         F[IdxCorreo]]
        for F in Inactivos
    ]

    Titulo = "Donantes NO activos (con justificacion del rechazo)"
    Encabezados = ["Justificacion", "Cedula", "Nombre completo",
                   "Tipo de sangre", "Fecha de nacimiento", "Peso",
                   "Sexo", "Telefono", "Correo"]
    return _EscribirArchivo("reporte_no_activos.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE EXTRA: Lugares de donacion.
# ----------------------------------------------------------------------
def ReporteLugaresDonacion():
    """
    Tabla con cada provincia, cantidad de donadores (activos+inactivos)
    y los recintos posibles de recaudacion. Orden ascendente por
    codigo de provincia segun Registro Civil del TSE.
    """
    Conteo = {}
    for F in Donadores:
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Conteo[Codigo] = Conteo.get(Codigo, 0) + 1

    FilasReporte = []
    for Codigo in sorted(Provincias.keys()):
        Lugares = modelo_datos.LugaresDonacion.get(Codigo, [])
        TextoLugares = ", ".join(Lugares) if Lugares else "-"
        FilasReporte.append([
            NombreProvincia(Codigo),
            str(Conteo.get(Codigo, 0)),
            TextoLugares,
        ])

    Titulo = "Lugares de donacion por provincia"
    Encabezados = ["Provincia",
                   "Cantidad de donadores registrados (activos e inactivos)",
                   "Recintos posibles de recaudacion"]
    return _EscribirArchivo("ReporteLugaresDonacion.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))


# ----------------------------------------------------------------------
# REPORTE EXTRA: Lugares de donacion.
# ----------------------------------------------------------------------
def ReporteLugaresDonacion():
    """
    Tabla con cada provincia, cantidad de donadores (activos+inactivos)
    y los recintos posibles de recaudacion. Orden ascendente por
    codigo de provincia segun Registro Civil del TSE.
    """
    Conteo = {}
    for F in Donadores:
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Conteo[Codigo] = Conteo.get(Codigo, 0) + 1

    FilasReporte = []
    for Codigo in sorted(Provincias.keys()):
        Lugares = modelo_datos.LugaresDonacion.get(Codigo, [])
        TextoLugares = ", ".join(Lugares) if Lugares else "-"
        FilasReporte.append([
            NombreProvincia(Codigo),
            str(Conteo.get(Codigo, 0)),
            TextoLugares,
        ])

    Titulo = "Lugares de donacion por provincia"
    Encabezados = ["Provincia",
                   "Cantidad de donadores registrados (activos e inactivos)",
                   "Recintos posibles de recaudacion"]
    return _EscribirArchivo("ReporteLugaresDonacion.html",
                             _ConstruirHtml(Titulo, Encabezados, FilasReporte))
