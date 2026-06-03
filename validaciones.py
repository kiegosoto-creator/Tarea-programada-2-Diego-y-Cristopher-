"""
================================================================================
Archivo: validaciones.py
Proposito:
    Funciones puras de validacion del formulario "Insertar donador"
    (y reutilizadas en "Actualizar"). Cada funcion principal devuelve
    una tupla (es_valido: bool, mensaje: str) para que la GUI pueda
    mostrar el mensaje de error directamente al usuario.

    Validaciones implementadas (todas exigidas por el enunciado):
        - Cedula: #-####-####, primer digito != 0.
        - Fecha: DD/MM/AAAA + validez calendarica.
        - Mayoria de edad por mes y anio.
        - Correo: 4 dominios permitidos (costarricense.cr, racsa.go.cr,
                  ccss.sa.cr, gmail.com).
        - Telefono: ####-####, primer digito no 0,1,3,5.
        - Peso: numerico, estrictamente 50 < peso < 120.
        - Nombre/apellido: letras (con tildes y enie) y espacios.

    Ademas se incluyen utilidades para convertir entre el formato
    visual de la cedula y su representacion entera en la matriz.
================================================================================
"""

import re
from datetime import date


# ----------------------------------------------------------------------
# Expresiones regulares pre-compiladas (mas eficiente que recompilar
# en cada llamada).
# ----------------------------------------------------------------------

# Cedula: #-####-####  donde el primer digito no puede ser 0.
RegexCedula = re.compile(r"^[1-9]-\d{4}-\d{4}$")

# Fecha: DD/MM/AAAA  (solo formato; los valores se validan con date).
RegexFecha = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")

# Correo: 4 dominios permitidos.
RegexCorreo = re.compile(
    r"^[A-Za-z0-9._%+-]+@"
    r"(costarricense\.cr|racsa\.go\.cr|ccss\.sa\.cr|gmail\.com)$"
)

# Telefono: ####-####  primer digito en {2,4,6,7,8,9}.
# (Excluidos por el enunciado: 0, 1, 3, 5).
RegexTelefono = re.compile(r"^[246789]\d{3}-\d{4}$")

# Nombre/apellido: letras (incluyendo tildes y enie) y espacios.
RegexNombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$")


# ----------------------------------------------------------------------
# Validaciones principales
# ----------------------------------------------------------------------

def ValidarCedula(Texto):
    """
    Valida el formato de la cedula de identidad.

    Reglas:
        - Formato exacto: #-####-####.
        - El primer digito no puede ser 0.

    Args:
        Texto (str): cedula tal como la ingreso el usuario.

    Returns:
        tuple (bool, str): (True, "") si es valida; (False, mensaje) si no.
    """
    if not Texto or not Texto.strip():
        return False, "La cedula no puede estar vacia."

    if not RegexCedula.match(Texto.strip()):
        return False, ("La cedula debe tener el formato #-####-#### "
                       "y el primer digito no puede ser 0.")

    return True, ""


def ValidarFecha(Texto):
    """
    Valida el formato y la validez calendarica de la fecha.

    Reglas:
        - Formato: DD/MM/AAAA.
        - Debe corresponder a una fecha real (rechaza 30/02/2000, etc).
        - El anio debe ser razonable (entre 1900 y el anio actual).

    Args:
        Texto (str): fecha tal como la ingreso el usuario.

    Returns:
        tuple (bool, str): (True, "") si es valida; (False, mensaje) si no.
    """
    if not Texto or not Texto.strip():
        return False, "La fecha de nacimiento no puede estar vacia."

    Coincidencia = RegexFecha.match(Texto.strip())
    if not Coincidencia:
        return False, "La fecha debe tener el formato DD/MM/AAAA."

    Dia, Mes, Anio = (int(Parte) for Parte in Coincidencia.groups())

    # Verificacion calendarica con la libreria estandar.
    try:
        date(Anio, Mes, Dia)
    except ValueError:
        return False, "La fecha indicada no existe en el calendario."

    AnioActual = date.today().year
    if Anio < 1900 or Anio > AnioActual:
        return False, f"El anio debe estar entre 1900 y {AnioActual}."

    return True, ""


def EsMayorDeEdad(Dia, Mes, Anio, Hoy=None):
    """
    Determina si la persona es mayor de edad (>= 18 anios) tomando
    en cuenta mes y dia, no solo el anio.

    Args:
        Dia (int): dia de nacimiento.
        Mes (int): mes de nacimiento.
        Anio (int): anio de nacimiento.
        Hoy (date, opcional): fecha de referencia (por defecto hoy).

    Returns:
        bool: True si ya cumplio 18 anios al dia 'Hoy'.
    """
    if Hoy is None:
        Hoy = date.today()
    return CalcularEdad(Dia, Mes, Anio, Hoy) >= 18


def CalcularEdad(Dia, Mes, Anio, Hoy=None):
    """
    Calcula la edad en anios cumplidos a partir de la fecha de
    nacimiento, considerando mes y dia.

    Args:
        Dia (int): dia de nacimiento.
        Mes (int): mes de nacimiento.
        Anio (int): anio de nacimiento.
        Hoy (date, opcional): fecha de referencia.

    Returns:
        int: edad en anios cumplidos (>= 0).
    """
    if Hoy is None:
        Hoy = date.today()

    Edad = Hoy.year - Anio
    # Si el cumpleanios de este anio aun no llega, restamos uno.
    if (Hoy.month, Hoy.day) < (Mes, Dia):
        Edad -= 1

    return max(Edad, 0)


def ValidarCorreo(Texto):
    """
    Valida que el correo cumpla con los 4 dominios permitidos:
        - costarricense.cr
        - racsa.go.cr
        - ccss.sa.cr
        - gmail.com

    Args:
        Texto (str): correo a validar.

    Returns:
        tuple (bool, str): (True, "") si es valido; (False, mensaje) si no.
    """
    if not Texto or not Texto.strip():
        return False, "El correo no puede estar vacio."

    if not RegexCorreo.match(Texto.strip()):
        return False, ("El correo debe pertenecer a uno de los dominios "
                       "permitidos: costarricense.cr, racsa.go.cr, "
                       "ccss.sa.cr o gmail.com.")

    return True, ""


def ValidarTelefono(Texto):
    """
    Valida el formato del telefono.

    Reglas:
        - Formato: ####-####.
        - El primer digito no puede ser 0, 1, 3 ni 5.

    Args:
        Texto (str): telefono a validar.

    Returns:
        tuple (bool, str): (True, "") si es valido; (False, mensaje) si no.
    """
    if not Texto or not Texto.strip():
        return False, "El telefono no puede estar vacio."

    if not RegexTelefono.match(Texto.strip()):
        return False, ("El telefono debe tener el formato ####-#### "
                       "y el primer digito no puede ser 0, 1, 3 ni 5.")

    return True, ""


def ValidarPeso(Texto):
    """
    Valida que el peso sea un numero estrictamente mayor a 50 y
    estrictamente menor a 120 (kilogramos).

    Args:
        Texto (str): peso ingresado por el usuario (admite decimales).

    Returns:
        tuple (bool, str, float): (True, "", peso) si es valido;
                                   (False, mensaje, 0.0) si no.
    """
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
    """
    Devuelve el mensaje de retroalimentacion correspondiente al peso,
    segun los 3 casos definidos en el enunciado.

    Args:
        Peso (float): peso en kilogramos.

    Returns:
        str: mensaje a mostrar al usuario.
    """
    if Peso <= 50:
        return "Usted debe pesar mas de 50 kgms para poder ser donador."

    if Peso >= 120:
        return "Dado su sobre peso, no es posible donar sangre."

    return "Usted posee un peso adecuado, correcto para ser donador de sangre."


def ValidarNombre(Texto):
    """
    Valida que el nombre/apellido no este vacio y solo contenga letras
    (incluyendo tildes y enie) y espacios entre palabras.

    Args:
        Texto (str): nombre o apellido a validar.

    Returns:
        tuple (bool, str): (True, "") si es valido; (False, mensaje) si no.
    """
    if not Texto or not Texto.strip():
        return False, "Este campo no puede estar vacio."

    if not RegexNombre.match(Texto.strip()):
        return False, ("Solo se permiten letras y espacios "
                       "(incluyendo tildes y la enie).")

    return True, ""


# ----------------------------------------------------------------------
# Utilidades de conversion de cedula
# ----------------------------------------------------------------------

def CedulaACodigoProvincia(CedulaStr):
    """
    Extrae el codigo de provincia (primer digito) de una cedula con
    formato #-####-####. Asume que la cedula ya fue validada.

    Args:
        CedulaStr (str): cedula validada previamente.

    Returns:
        int: codigo de provincia (1-8).
    """
    return int(CedulaStr.strip()[0])


def CedulaStrAInt(CedulaStr):
    """
    Convierte la cedula del formato visual #-####-#### a entero, que
    es como se almacena en la matriz.

    Ejemplo: "1-2345-6789" -> 123456789.

    Args:
        CedulaStr (str): cedula con guiones.

    Returns:
        int: cedula sin guiones.
    """
    return int(CedulaStr.strip().replace("-", ""))


def CedulaIntAStr(CedulaInt):
    """
    Convierte la cedula entera al formato visual #-####-####.

    Ejemplo: 123456789 -> "1-2345-6789".

    Args:
        CedulaInt (int): cedula sin guiones (9 digitos).

    Returns:
        str: cedula formateada.
    """
    Texto = str(CedulaInt).zfill(9)
    return f"{Texto[0]}-{Texto[1:5]}-{Texto[5:9]}"
