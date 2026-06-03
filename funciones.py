"""
================================================================================
Tarea Programada #2 - Donemos Sangre, demos vida...
Taller de Programacion - I Semestre 2026

Integrantes:
    - Cristhoper Jara Salazar
    - Diego Kim

Archivo: funciones.py
Proposito:
    Concentra TODA la logica del Banco Nacional de Sangre. Este es
    uno de los 3 archivos que componen el proyecto (junto con
    archivos.py y principal.py).

    Incluye:
        Seccion 1: Estructuras de datos globales (matriz, diccionario,
                   tupla, constantes Idx*).
        Seccion 2: Validaciones con expresiones regulares.
        Seccion 3: Logica de negocio (compatibilidades, generacion
                   aleatoria, busqueda).
        Seccion 4: Generacion de reportes HTML5.

    Convencion de codigo:
        - Variables, funciones y parametros en NombreCamello.
        - Sin uso de la palabra clave 'global'. Las estructuras
          globales se mutan en sitio con .clear() / .append() /
          .update() para evitar 'global'.
        - Documentacion interna en cada funcion (docstring).
================================================================================
"""

import re
import random
from datetime import date, datetime


# ============================================================================
# SECCION 1: ESTRUCTURAS DE DATOS GLOBALES
# ============================================================================

# Tupla con los tipos de sangre. En la matriz se almacena el INDICE
# de cada tipo en esta tupla, no el string.
TiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# Provincias de Costa Rica segun el primer digito de la cedula.
Provincias = {
    1: "San Jose",
    2: "Alajuela",
    3: "Cartago",
    4: "Heredia",
    5: "Guanacaste",
    6: "Puntarenas",
    7: "Limon",
    8: "Naturalizado",
}

# Diccionario inicial de lugares de donacion por provincia.
LugaresDonacionInicial = {
    1: ["El Banco Nacional de Sangre",
        "Hospital Mexico",
        "Hospital San Juan de Dios"],
    2: ["Hospital San Rafael de Alajuela",
        "Hospital de San Ramon",
        "Hospital del Canton Norteno"],
    3: ["Hospital Max Peralta"],
    4: ["Hospital San Vicente de Paul"],
    5: ["Hospital La Anexion en Nicoya",
        "Hospital Enrique Baltodano de Liberia"],
    6: ["Hospital Monsenor Sanabria"],
    7: ["Hospital Tony Facio",
        "Hospital de Guapiles"],
}

# Justificaciones de rechazo segun Gemini.
Justificaciones = {
    0: "Donador activo (sin justificacion de rechazo)",
    1: "Enfermedades Infecciosas/Cronicas: Portadores de VIH, Hepatitis B o C, "
       "sifilis, tuberculosis, o pacientes diabeticos insulinodependientes, "
       "asi como afecciones graves de corazon, rinion o pulmon.",
    2: "Conductas de Riesgo: Nuevas parejas sexuales o mas de una pareja "
       "sexual en los ultimos 3 meses, relaciones sexuales por dinero o drogas.",
    3: "Factores de Salud Fisica: Hemoglobina/hematocrito bajo o alto, "
       "presion arterial inestable, fiebre, o infecciones recientes.",
    4: "Procedimientos Medicos: Haber recibido transfusiones, trasplantes, "
       "cirugias mayores, tatuajes, piercing o endoscopias recientes.",
    5: "Uso de Medicamentos: Consumo de farmacos inyectables sin receta o "
       "ciertos medicamentos.",
    6: "Estilo de Vida y Viajes: Uso de drogas recreativas, consumo de alcohol "
       "en las ultimas 24 horas, o viajes a zonas endemicas de malaria/dengue.",
    7: "Situaciones Especificas: Embarazo, lactancia o menstruacion (se "
       "evalua cada caso).",
}

# Posiciones de los campos en la matriz de donadores.
IdxNombre = 0          # [nombre, apellido1, apellido2]
IdxCedula = 1          # int
IdxTipoSangre = 2      # int (indice en TiposDeSangre)
IdxSexo = 3            # bool (True = Hombre, False = Mujer)
IdxFechaNac = 4        # tupla (DD, MM, AAAA)
IdxPeso = 5            # float
IdxCorreo = 6          # str
IdxTelefono = 7        # str
IdxEstado = 8          # int (1 = activo, 0 = inactivo)
IdxJustificacion = 9   # int (0-7)

# Estructuras mutables en RAM.
Donadores = []
LugaresDonacion = {}


def InicializarModelo():
    """Reinicia las estructuras globales a su estado inicial."""
    Donadores.clear()
    LugaresDonacion.clear()
    for Codigo, ListaLugares in LugaresDonacionInicial.items():
        LugaresDonacion[Codigo] = list(ListaLugares)


def HayBaseDeDatos():
    """True si hay al menos un donador en la matriz."""
    return len(Donadores) > 0


# ============================================================================
# SECCION 2: VALIDACIONES CON EXPRESIONES REGULARES
# ============================================================================

RegexCedula = re.compile(r"^[1-9]-\d{4}-\d{4}$")
RegexFecha = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")
RegexCorreo = re.compile(
    r"^[A-Za-z0-9._%+-]+@"
    r"(costarricense\.cr|racsa\.go\.cr|ccss\.sa\.cr|gmail\.com)$"
)
RegexTelefono = re.compile(r"^[246789]\d{3}-\d{4}$")
RegexNombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$")


def ValidarCedula(Texto):
    """Valida formato #-####-#### con primer digito != 0."""
    if not Texto or not Texto.strip():
        return False, "La cedula no puede estar vacia."
    if not RegexCedula.match(Texto.strip()):
        return False, ("La cedula debe tener el formato #-####-#### "
                       "y el primer digito no puede ser 0.")
    return True, ""


def ValidarFecha(Texto):
    """Valida formato DD/MM/AAAA + validez calendarica."""
    if not Texto or not Texto.strip():
        return False, "La fecha de nacimiento no puede estar vacia."
    Coincidencia = RegexFecha.match(Texto.strip())
    if not Coincidencia:
        return False, "La fecha debe tener el formato DD/MM/AAAA."
    Dia, Mes, Anio = (int(P) for P in Coincidencia.groups())
    try:
        date(Anio, Mes, Dia)
    except ValueError:
        return False, "La fecha indicada no existe en el calendario."
    AnioActual = date.today().year
    if Anio < 1900 or Anio > AnioActual:
        return False, f"El anio debe estar entre 1900 y {AnioActual}."
    return True, ""


def EsMayorDeEdad(Dia, Mes, Anio, Hoy=None):
    """True si tiene >= 18 anios cumplidos por mes y dia."""
    if Hoy is None:
        Hoy = date.today()
    return CalcularEdad(Dia, Mes, Anio, Hoy) >= 18


def CalcularEdad(Dia, Mes, Anio, Hoy=None):
    """Edad en anios cumplidos."""
    if Hoy is None:
        Hoy = date.today()
    Edad = Hoy.year - Anio
    if (Hoy.month, Hoy.day) < (Mes, Dia):
        Edad -= 1
    return max(Edad, 0)


def ValidarCorreo(Texto):
    """Valida correo con uno de los 4 dominios permitidos."""
    if not Texto or not Texto.strip():
        return False, "El correo no puede estar vacio."
    if not RegexCorreo.match(Texto.strip()):
        return False, ("El correo debe pertenecer a uno de los dominios "
                       "permitidos: costarricense.cr, racsa.go.cr, "
                       "ccss.sa.cr o gmail.com.")
    return True, ""


def ValidarTelefono(Texto):
    """Valida formato ####-#### con primer digito en {2,4,6,7,8,9}."""
    if not Texto or not Texto.strip():
        return False, "El telefono no puede estar vacio."
    if not RegexTelefono.match(Texto.strip()):
        return False, ("El telefono debe tener el formato ####-#### "
                       "y el primer digito no puede ser 0, 1, 3 ni 5.")
    return True, ""


def ValidarPeso(Texto):
    """Valida peso > 50 y < 120."""
    if not Texto or not Texto.strip():
        return False, "El peso no puede estar vacio.", 0.0
    try:
        Peso = float(Texto.strip().replace(",", "."))
    except ValueError:
        return False, "El peso debe ser un numero valido.", 0.0
    if Peso <= 0:
        return False, "El peso debe ser positivo.", 0.0
    if not (50 < Peso < 120):
        return False, ("El peso debe ser estrictamente mayor a 50 kgms y "
                       "menor a 120 kgms."), 0.0
    return True, "", Peso


def ClasificarPeso(Peso):
    """Devuelve el mensaje de retroalimentacion segun el peso."""
    if Peso <= 50:
        return "Usted debe pesar mas de 50 kgms para poder ser donador."
    if Peso >= 120:
        return "Dado su sobre peso, no es posible donar sangre."
    return "Usted posee un peso adecuado, correcto para ser donador de sangre."


def ValidarNombre(Texto):
    """Valida que solo contenga letras y espacios."""
    if not Texto or not Texto.strip():
        return False, "Este campo no puede estar vacio."
    if not RegexNombre.match(Texto.strip()):
        return False, ("Solo se permiten letras y espacios "
                       "(incluyendo tildes y la enie).")
    return True, ""


def CedulaACodigoProvincia(CedulaStr):
    """Devuelve el primer digito (codigo de provincia 1-8)."""
    return int(CedulaStr.strip()[0])


def CedulaStrAInt(CedulaStr):
    """Convierte '1-2345-6789' -> 123456789."""
    return int(CedulaStr.strip().replace("-", ""))


def CedulaIntAStr(CedulaInt):
    """Convierte 123456789 -> '1-2345-6789'."""
    Texto = str(CedulaInt).zfill(9)
    return f"{Texto[0]}-{Texto[1:5]}-{Texto[5:9]}"


# ============================================================================
# SECCION 3: LOGICA DE NEGOCIO
# ============================================================================

# Compatibilidades sanguineas (pagina 16 del enunciado).
PuedeDonarA = {
    "O-":  ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+":  ["O+", "A+", "B+", "AB+"],
    "A-":  ["A-", "A+", "AB-", "AB+"],
    "A+":  ["A+", "AB+"],
    "B-":  ["B-", "B+", "AB-", "AB+"],
    "B+":  ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"],
}

PuedeRecibirDe = {
    "O-":  ["O-"],
    "O+":  ["O-", "O+"],
    "A-":  ["O-", "A-"],
    "A+":  ["O-", "O+", "A-", "A+"],
    "B-":  ["O-", "B-"],
    "B+":  ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
}

RecomendacionPorTipo = {
    "A+":  "Se le recomienda que done sangre entera y plaquetas.",
    "A-":  "Se le recomienda que done sangre entera y globulos rojos dobles.",
    "B+":  "Puede lograr el mayor impacto con donaciones de sangre entera y "
           "de globulos rojos dobles.",
    "B-":  "Se le recomienda que done sangre entera o plaquetas.",
    "O+":  "Se le recomienda donar globulos rojos dobles y sangre entera.",
    "O-":  "Se le recomienda donar globulos rojos dobles y sangre entera. "
           "Ademas, usted es donante universal.",
    "AB+": "Se le recomienda hacer donaciones de plaquetas y de plasma. "
           "Ademas, usted es receptor universal.",
    "AB-": "Se le recomienda donar plaquetas y plasma.",
}


def ObtenerLugaresPorCedula(CedulaInt):
    """Devuelve la lista de lugares para la provincia del primer digito."""
    Codigo = int(str(CedulaInt).zfill(9)[0])
    return list(LugaresDonacion.get(Codigo, []))


def NombreProvincia(Codigo):
    """Devuelve el nombre de la provincia segun el codigo."""
    return Provincias.get(Codigo, "Desconocida")


def TipoSangreAIndice(TipoStr):
    """Convierte string -> indice 0-7 en TiposDeSangre. -1 si invalido."""
    try:
        return TiposDeSangre.index(TipoStr)
    except ValueError:
        return -1


def IndiceATipoSangre(Indice):
    """Convierte indice -> string."""
    if 0 <= Indice < len(TiposDeSangre):
        return TiposDeSangre[Indice]
    return ""


def MensajeCompatibilidad(TipoStr):
    """Mensaje con los tipos a los que puede donar + recomendacion."""
    if TipoStr not in PuedeDonarA:
        return "Tipo de sangre no reconocido."
    ListaCompatibles = ", ".join(PuedeDonarA[TipoStr])
    Recomendacion = RecomendacionPorTipo.get(TipoStr, "")
    return (f"Dado su tipo de sangre {TipoStr}, usted puede donar a: "
            f"{ListaCompatibles}.\n{Recomendacion}")


def BuscarDonadorPorCedula(CedulaInt):
    """Devuelve el indice de la fila con esa cedula, o -1."""
    for Indice, Fila in enumerate(Donadores):
        if Fila[IdxCedula] == CedulaInt:
            return Indice
    return -1


def ExisteCedula(CedulaInt):
    """True si la cedula ya esta registrada."""
    return BuscarDonadorPorCedula(CedulaInt) != -1


def JustificacionCompleta(IndiceJustificacion):
    """Texto completo de la justificacion."""
    return Justificaciones.get(IndiceJustificacion,
                               "Justificacion desconocida")


# Pools de datos para generacion aleatoria.
_NombresPila = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia",
                "Diego", "Lucia", "Pedro", "Camila", "Miguel",
                "Valentina", "Jose", "Isabella", "Fernando", "Laura",
                "Andres", "Daniela", "Roberto", "Paula", "Esteban",
                "Carolina", "Manuel", "Gabriela", "Ricardo", "Marcela",
                "Adrian", "Veronica", "Pablo", "Mariana", "Cristhoper"]
_PrimerosApellidos = ["Lopez", "Rodriguez", "Mora", "Vargas",
                      "Jimenez", "Solis", "Rojas", "Cruz",
                      "Hernandez", "Castillo", "Quiros", "Salas",
                      "Soto", "Aguilar", "Brenes", "Ramirez",
                      "Calderon", "Montero", "Ulate", "Gonzalez"]
_SegundosApellidos = ["Sanchez", "Martinez", "Perez", "Gomez",
                      "Aguero", "Calderon", "Mendez", "Pacheco",
                      "Vargas", "Murillo", "Zamora", "Cordero",
                      "Bonilla", "Ramirez", "Araya", "Villalobos",
                      "Esquivel", "Chacon", "Alfaro", "Picado"]
_DominiosPermitidos = ["gmail.com", "costarricense.cr",
                       "racsa.go.cr", "ccss.sa.cr"]
_PrimerosDigitosTelefono = [2, 4, 6, 7, 8, 9]
_DiasPorMes = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
               7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def GenerarDonadoresAleatorios(Cantidad):
    """
    Genera dinamicamente 'Cantidad' donadores aleatorios.

    Fixes aplicados respecto a la version anterior:
    1. La cantidad de inactivos ahora es EXACTA: int(Cantidad * 0.20),
       no probabilistica. Garantiza que con 20 donadores salgan 4
       inactivos siempre.
    2. Se usa random.SystemRandom() para cedulas y otros campos,
       que toma entropia del sistema operativo y produce numeros
       mucho mas uniformes que random.randint() basico.
    3. La primera y segunda parte de la cedula se distribuyen en el
       rango completo 0-9999 con padding correcto.

    Args:
        Cantidad (int): numero de donadores a generar (debe ser > 0).

    Returns:
        int: cantidad efectivamente agregada a la matriz.
    """
    if Cantidad <= 0:
        return 0

    # Generador con entropia del SO para mejor aleatoriedad.
    Rng = random.SystemRandom()

    Hoy = date.today()
    AnioMin = Hoy.year - 70
    AnioMax = Hoy.year - 18
    CedulasExistentes = set(Fila[IdxCedula] for Fila in Donadores)

    # Calcular la cantidad EXACTA de inactivos (20% redondeado).
    CantidadInactivos = int(Cantidad * 0.20)
    # Generar la lista de booleanos: True = activo, False = inactivo.
    # Y mezclarla para que la posicion sea aleatoria.
    EstadosPorPosicion = [False] * CantidadInactivos + \
                         [True] * (Cantidad - CantidadInactivos)
    Rng.shuffle(EstadosPorPosicion)

    Agregados = 0
    for IndicePosicion in range(Cantidad):
        # Cedula unica con formato valido.
        Intentos = 0
        while True:
            CodProv = Rng.randint(1, 8)
            P2 = Rng.randint(0, 9999)
            P3 = Rng.randint(0, 9999)
            CedulaStr = f"{CodProv}-{P2:04d}-{P3:04d}"
            CedulaInt = CedulaStrAInt(CedulaStr)
            if CedulaInt not in CedulasExistentes:
                CedulasExistentes.add(CedulaInt)
                break
            Intentos += 1
            if Intentos > 500:
                return Agregados

        # Nombre completo.
        ListaNombre = [Rng.choice(_NombresPila),
                       Rng.choice(_PrimerosApellidos),
                       Rng.choice(_SegundosApellidos)]
        # Tipo de sangre (indice 0-7).
        IndiceTipo = Rng.randint(0, len(TiposDeSangre) - 1)
        # Sexo.
        EsHombre = Rng.choice([True, False])
        # Fecha mayor de edad.
        AnioNac = Rng.randint(AnioMin, AnioMax)
        MesNac = Rng.randint(1, 12)
        DiaNac = Rng.randint(1, _DiasPorMes[MesNac])
        FechaNac = (DiaNac, MesNac, AnioNac)
        # Peso (51 - 119, una sola decimal).
        Peso = round(Rng.uniform(51.0, 119.0), 1)
        # Correo con dominio permitido.
        Login = (f"{ListaNombre[0].lower()}"
                 f"{Rng.randint(1, 999)}")
        Correo = f"{Login}@{Rng.choice(_DominiosPermitidos)}"
        # Telefono.
        PrimerDigito = Rng.choice(_PrimerosDigitosTelefono)
        Resto = Rng.randint(0, 9999999)
        TelefonoStr = f"{PrimerDigito}{Resto:07d}"
        Telefono = f"{TelefonoStr[:4]}-{TelefonoStr[4:]}"
        # Estado y justificacion (deterministico por posicion).
        if EstadosPorPosicion[IndicePosicion]:
            Estado, JustifVal = 1, 0
        else:
            Estado = 0
            JustifVal = Rng.randint(1, 7)

        Donadores.append([
            ListaNombre, CedulaInt, IndiceTipo, EsHombre, FechaNac,
            Peso, Correo, Telefono, Estado, JustifVal,
        ])
        Agregados += 1

    return Agregados


# ============================================================================
# SECCION 4: REPORTES HTML5
# ============================================================================

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


def _FechaHoraActual():
    """Fecha/hora del sistema formateada."""
    return datetime.now().strftime("%d/%m/%Y a las %H:%M:%S")


def _FormatearFecha(Tupla):
    """Tupla (DD, MM, AAAA) -> 'DD/MM/AAAA'."""
    Dia, Mes, Anio = Tupla
    return f"{Dia:02d}/{Mes:02d}/{Anio:04d}"


def _NombreCompletoStr(ListaNombre):
    """[nombre, ap1, ap2] -> 'nombre ap1 ap2'."""
    return " ".join(ListaNombre)


def _SexoATexto(EsHombre):
    """Bool -> 'Masculino' / 'Femenino'."""
    return "Masculino" if EsHombre else "Femenino"


def _ConstruirTablaHtml(Encabezados, Filas):
    """Construye <table> o mensaje 'sin datos'."""
    if not Filas:
        return '<p class="sin-datos">No hay registros que mostrar.</p>'
    HtmlEnc = "".join(f"<th>{T}</th>" for T in Encabezados)
    LineasFilas = []
    for Fila in Filas:
        Celdas = "".join(f"<td>{C}</td>" for C in Fila)
        LineasFilas.append(f"<tr>{Celdas}</tr>")
    return ("<table>"
            f"<thead><tr>{HtmlEnc}</tr></thead>"
            f"<tbody>{''.join(LineasFilas)}</tbody>"
            "</table>")


def _ConstruirHtml(Titulo, Encabezados, Filas):
    """Arma el HTML5 final con plantilla."""
    return PlantillaHtml.format(
        Titulo=Titulo,
        FechaHora=_FechaHoraActual(),
        Contenido=_ConstruirTablaHtml(Encabezados, Filas),
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
    """Lista de pares (indice, fila) de donadores activos."""
    return [(I, F) for I, F in enumerate(Donadores)
            if F[IdxEstado] == 1]


def ReporteDonantesPorProvincia(CodigoProvincia):
    """Reporte 1: donantes activos de la provincia, ordenados por nombre."""
    Filtrados = []
    for _, F in _FiltrarActivos():
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        if CedulaACodigoProvincia(CedulaStr) == CodigoProvincia:
            Filtrados.append(F)
    Filtrados.sort(key=lambda F: _NombreCompletoStr(F[IdxNombre]))
    Filas = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono], F[IdxCorreo]]
        for F in Filtrados
    ]
    Titulo = (f"Donantes activos de la provincia de "
              f"{NombreProvincia(CodigoProvincia)}")
    Encabezados = ["Cedula", "Nombre completo", "Fecha de nacimiento",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteDonantesPorProvincia.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReportePorRangoEdad(EdadInicial, EdadFinal=None):
    """Reporte 2: donantes activos en rango [EdadInicial, EdadFinal]."""
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
    Filas = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono], F[IdxCorreo]]
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
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReportePorTipoYProvincia(TipoSangreStr, CodigoProvincia):
    """Reporte 3: donantes activos de tipo X en provincia Y."""
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
    Filtrados.sort(key=lambda F: _NombreCompletoStr(F[IdxNombre]))
    Filas = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono], F[IdxCorreo]]
        for F in Filtrados
    ]
    Titulo = (f"Donantes activos {TipoSangreStr} en "
              f"{NombreProvincia(CodigoProvincia)}")
    Encabezados = ["Cedula", "Nombre completo", "Fecha de nacimiento",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReportePorTipoYProvincia.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReporteListaCompleta():
    """Reporte 4: lista completa de donantes activos por provincia."""
    Anotados = []
    for _, F in _FiltrarActivos():
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Anotados.append((Codigo, F))
    Anotados.sort(key=lambda Par: (Par[0],
                                   _NombreCompletoStr(Par[1][IdxNombre])))
    Filas = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         _FormatearFecha(F[IdxFechaNac]),
         f"{F[IdxPeso]:.1f} kg",
         _SexoATexto(F[IdxSexo]),
         F[IdxTelefono], F[IdxCorreo]]
        for _, F in Anotados
    ]
    Titulo = "Lista completa de donantes activos (ordenada por provincia)"
    Encabezados = ["Cedula", "Nombre completo", "Tipo de sangre",
                   "Fecha de nacimiento", "Peso", "Sexo", "Telefono",
                   "Correo"]
    return _EscribirArchivo("ReporteListaCompleta.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReporteMujeresONegativo():
    """Reporte 5: mujeres activas O- con edad < 45, por edad."""
    IndiceONeg = TipoSangreAIndice("O-")
    Candidatas = []
    for _, F in _FiltrarActivos():
        if F[IdxSexo] is True:
            continue
        if F[IdxTipoSangre] != IndiceONeg:
            continue
        D, M, A = F[IdxFechaNac]
        E = CalcularEdad(D, M, A)
        if E < 45:
            Candidatas.append((E, F))
    Candidatas.sort(key=lambda Par: Par[0])
    Filas = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         _FormatearFecha(F[IdxFechaNac]),
         F[IdxTelefono], F[IdxCorreo]]
        for _, F in Candidatas
    ]
    Titulo = "Mujeres donantes O- menores de 45 anios"
    Encabezados = ["Cedula", "Nombre completo", "Fecha de nacimiento",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteMujeresONegativo.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReporteAQuienPuedeDonar(TipoSangreStr):
    """
    Reporte 6: donadores activos del tipo X, asc por provincia.

    Muestra a los donantes ACTIVOS que SON tipo X (porque ellos son
    los que pueden donar a sus tipos compatibles PuedeDonarA[X]).
    """
    IndiceTipo = TipoSangreAIndice(TipoSangreStr)
    if IndiceTipo == -1 or TipoSangreStr not in PuedeDonarA:
        return False
    Destinos = ", ".join(PuedeDonarA[TipoSangreStr])
    Candidatos = []
    for _, F in _FiltrarActivos():
        if F[IdxTipoSangre] != IndiceTipo:
            continue
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Candidatos.append((Codigo, F))
    Candidatos.sort(
        key=lambda Par: (Par[0],
                         _NombreCompletoStr(Par[1][IdxNombre])))
    Filas = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         F[IdxTelefono], F[IdxCorreo]]
        for _, F in Candidatos
    ]
    Titulo = (f"Donantes {TipoSangreStr}: pueden donar a "
              f"{Destinos} (orden ascendente por provincia)")
    Encabezados = ["Cedula", "Nombre completo", "Tipo de sangre",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteAQuienPuedeDonar.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReporteDeQuienPuedeRecibir(TipoSangreStr):
    """
    Reporte 7: donadores activos COMPATIBLES como donantes para X.

    FIX: Antes filtraba mal (solo mismo tipo). Ahora filtra por los
    tipos en PuedeRecibirDe[X], que son los que pueden donar a X.
    Asi AB+ (receptor universal) muestra donantes de TODOS los tipos.

    Orden: descendente por provincia.
    """
    if TipoSangreStr not in PuedeRecibirDe:
        return False
    OrigenesCompatibles = PuedeRecibirDe[TipoSangreStr]
    IndicesCompatibles = set()
    for TipoCompatible in OrigenesCompatibles:
        Idx = TipoSangreAIndice(TipoCompatible)
        if Idx != -1:
            IndicesCompatibles.add(Idx)

    Candidatos = []
    for _, F in _FiltrarActivos():
        # FIX clave: el donador debe tener un tipo COMPATIBLE, no el
        # mismo tipo del receptor.
        if F[IdxTipoSangre] not in IndicesCompatibles:
            continue
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Candidatos.append((Codigo, F))

    # Descendente por provincia, luego por nombre.
    Candidatos.sort(
        key=lambda Par: (-Par[0],
                         _NombreCompletoStr(Par[1][IdxNombre])))
    Filas = [
        [CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         F[IdxTelefono], F[IdxCorreo]]
        for _, F in Candidatos
    ]
    Titulo = (f"Donantes que pueden donar a {TipoSangreStr}: tipos "
              f"compatibles {', '.join(OrigenesCompatibles)} "
              "(orden descendente por provincia)")
    Encabezados = ["Cedula", "Nombre completo", "Tipo de sangre",
                   "Telefono", "Correo"]
    return _EscribirArchivo("ReporteDeQuienPuedeRecibir.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReporteDonantesNoActivos():
    """Reporte 8: donantes inactivos con justificacion textual."""
    Inactivos = [F for F in Donadores if F[IdxEstado] == 0]
    Inactivos.sort(key=lambda F: (F[IdxJustificacion],
                                  _NombreCompletoStr(F[IdxNombre])))
    Filas = [
        [JustificacionCompleta(F[IdxJustificacion]),
         CedulaIntAStr(F[IdxCedula]),
         _NombreCompletoStr(F[IdxNombre]),
         IndiceATipoSangre(F[IdxTipoSangre]),
         _FormatearFecha(F[IdxFechaNac]),
         f"{F[IdxPeso]:.1f} kg",
         _SexoATexto(F[IdxSexo]),
         F[IdxTelefono], F[IdxCorreo]]
        for F in Inactivos
    ]
    Titulo = "Donantes NO activos (con justificacion del rechazo)"
    Encabezados = ["Justificacion", "Cedula", "Nombre completo",
                   "Tipo de sangre", "Fecha de nacimiento", "Peso",
                   "Sexo", "Telefono", "Correo"]
    return _EscribirArchivo("ReporteNoActivos.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))


def ReporteLugaresDonacion():
    """Reporte extra: lugares por provincia con conteo."""
    Conteo = {}
    for F in Donadores:
        CedulaStr = CedulaIntAStr(F[IdxCedula])
        Codigo = CedulaACodigoProvincia(CedulaStr)
        Conteo[Codigo] = Conteo.get(Codigo, 0) + 1
    Filas = []
    for Codigo in sorted(Provincias.keys()):
        Lugares = LugaresDonacion.get(Codigo, [])
        TextoLugares = ", ".join(Lugares) if Lugares else "-"
        Filas.append([NombreProvincia(Codigo),
                      str(Conteo.get(Codigo, 0)),
                      TextoLugares])
    Titulo = "Lugares de donacion por provincia"
    Encabezados = ["Provincia",
                   "Cantidad de donadores registrados (activos e inactivos)",
                   "Recintos posibles de recaudacion"]
    return _EscribirArchivo("ReporteLugaresDonacion.html",
                            _ConstruirHtml(Titulo, Encabezados, Filas))
