"""
================================================================================
Archivo: logica_negocio.py
Proposito:
    Reglas de negocio del Banco de Sangre que no son validaciones de
    formato sino logica del dominio:

    - Compatibilidades sanguineas (quien puede donar a quien y de quien
      puede recibir).
    - Mapeo de provincia de la cedula al lugar de donacion correspondiente.
    - Mensajes de recomendacion segun tipo de sangre (Conoce tu tipo de sangre).
    - Generacion de donadores aleatorios.
================================================================================
"""

from modelo_datos import (
    TiposDeSangre,
    Provincias,
    LugaresDonacion,
    Justificaciones,
)


# ----------------------------------------------------------------------
# Compatibilidades sanguineas - tabla de la pagina 16 del enunciado.
# Clave: tipo de sangre.
# Valor: lista de tipos a los que puede donar / de los que puede recibir.
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Mensajes de recomendacion segun tipo de sangre (resaltado en amarillo
# en la seccion "Conoce tu tipo de sangre" del enunciado).
# ----------------------------------------------------------------------
RecomendacionPorTipo = {
    "A+":  "Se le recomienda que done sangre entera y plaquetas.",
    "A-":  "Se le recomienda que done sangre entera y globulos rojos dobles.",
    "B+":  "Puede lograr el mayor impacto con donaciones de sangre entera y "
           "de globulos rojos dobles.",
    "B-":  "Se le recomienda que done sangre entera o plaquetas.",
    "O+":  "Se le recomienda donar globulos rojos dobles y sangre entera.",
    "O-":  "Se le recomienda donar globulos rojos dobles y sangre entera. "
           "Ademas, usted es donante universal.",
    "AB+": "Se le recomienda hacer donaciones de plaquetas y de plasma.",
    "AB-": "Se le recomienda donar plaquetas y plasma.",
}


def ObtenerLugaresPorCedula(CedulaInt):
    """
    Dado el codigo de provincia (primer digito de la cedula) devuelve
    la lista de lugares de donacion correspondientes leyendo del
    diccionario global.

    Args:
        CedulaInt (int): cedula sin guiones (ej. 123456789).

    Returns:
        list[str]: lugares disponibles para la provincia indicada.
                   Lista vacia si no hay lugares registrados.
    """
    # Obtenemos el primer digito como entero (codigo de provincia).
    Codigo = int(str(CedulaInt).zfill(9)[0])
    return list(LugaresDonacion.get(Codigo, []))


def NombreProvincia(Codigo):
    """
    Devuelve el nombre de la provincia segun el codigo.

    Args:
        Codigo (int): codigo de provincia (1-8).

    Returns:
        str: nombre de la provincia o "Desconocida" si no existe.
    """
    return Provincias.get(Codigo, "Desconocida")


def TipoSangreAIndice(TipoStr):
    """
    Convierte el string del tipo de sangre al indice en la tupla global.

    Args:
        TipoStr (str): por ejemplo "O+".

    Returns:
        int: indice (0-7) en TiposDeSangre, o -1 si no existe.
    """
    try:
        return TiposDeSangre.index(TipoStr)
    except ValueError:
        return -1


def IndiceATipoSangre(Indice):
    """
    Convierte el indice almacenado en la matriz al string del tipo.

    Args:
        Indice (int): indice 0-7.

    Returns:
        str: tipo de sangre (ej. "AB-") o cadena vacia si el indice es invalido.
    """
    if 0 <= Indice < len(TiposDeSangre):
        return TiposDeSangre[Indice]
    return ""


def MensajeCompatibilidad(TipoStr):
    """
    Construye el mensaje que se muestra al usuario tras insertar
    indicando a quien puede donar segun su tipo de sangre y la
    recomendacion de donacion (sangre entera, plaquetas, etc).

    Args:
        TipoStr (str): tipo de sangre del nuevo donador.

    Returns:
        str: mensaje completo con la lista de tipos compatibles y la
             recomendacion personalizada.
    """
    if TipoStr not in PuedeDonarA:
        return "Tipo de sangre no reconocido."

    ListaCompatibles = ", ".join(PuedeDonarA[TipoStr])
    Recomendacion = RecomendacionPorTipo.get(TipoStr, "")
    return (f"Dado su tipo de sangre {TipoStr}, usted puede donar a: "
            f"{ListaCompatibles}.\n{Recomendacion}")


def BuscarDonadorPorCedula(CedulaInt):
    """
    Recorre la matriz global y devuelve el indice de la fila que tenga
    la cedula indicada. -1 si no existe.

    Args:
        CedulaInt (int): cedula a buscar.

    Returns:
        int: indice en la matriz o -1.
    """
    # Importacion local para evitar dependencias circulares al cargarse
    # el modulo (modelo_datos -> logica_negocio en algunas funciones).
    from modelo_datos import Donadores, IdxCedula

    for Indice, Fila in enumerate(Donadores):
        if Fila[IdxCedula] == CedulaInt:
            return Indice
    return -1


def ExisteCedula(CedulaInt):
    """
    Indica si una cedula ya esta registrada en la matriz.

    Args:
        CedulaInt (int): cedula a verificar.

    Returns:
        bool: True si existe.
    """
    return BuscarDonadorPorCedula(CedulaInt) != -1


def GenerarDonadoresAleatorios(Cantidad):
    """
    Genera dinamicamente 'Cantidad' donadores con datos aleatorios
    respetando todas las restricciones (tipo de sangre como indice de
    la tupla global, peso entre 50 y 120, edad entre 18 y 70, cedula
    formato valido y unica, telefono valido, correo con dominio
    permitido).

    Aproximadamente el 20% de los donadores generados quedan como NO
    activos (estado=0) con una justificacion aleatoria del 1 al 7.

    Args:
        Cantidad (int): numero de donadores a generar (debe ser > 0).

    Returns:
        int: cantidad efectivamente agregada a la matriz.
    """
    import random
    from datetime import date
    from modelo_datos import Donadores, IdxCedula
    from validaciones import CedulaStrAInt

    if Cantidad <= 0:
        return 0

    # Pools de datos para construir nombres y correos verosimiles.
    Nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia",
               "Diego", "Lucia", "Pedro", "Camila", "Miguel",
               "Valentina", "Jose", "Isabella", "Fernando", "Laura",
               "Andres", "Daniela", "Roberto", "Paula", "Esteban",
               "Carolina", "Manuel", "Gabriela", "Ricardo"]
    PrimerosApellidos = ["Lopez", "Rodriguez", "Mora", "Vargas",
                         "Jimenez", "Solis", "Rojas", "Cruz",
                         "Hernandez", "Castillo", "Quiros", "Salas",
                         "Soto", "Aguilar", "Brenes", "Ramirez",
                         "Calderon"]
    SegundosApellidos = ["Sanchez", "Martinez", "Perez", "Gomez",
                         "Aguero", "Calderon", "Mendez", "Pacheco",
                         "Vargas", "Murillo", "Zamora", "Cordero",
                         "Bonilla", "Ramirez", "Araya", "Villalobos"]
    DominiosPermitidos = ["gmail.com", "costarricense.cr",
                          "racsa.go.cr", "ccss.sa.cr"]
    PrimerosDigitosTelefono = [2, 4, 6, 7, 8, 9]
    DiasPorMes = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                  7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    Hoy = date.today()
    AnioMin = Hoy.year - 70
    AnioMax = Hoy.year - 18
    CedulasExistentes = set(Fila[IdxCedula] for Fila in Donadores)
    Agregados = 0

    for _ in range(Cantidad):
        # 1) Cedula unica con formato valido (primer digito 1-8).
        Intentos = 0
        while True:
            CodProv = random.randint(1, 8)
            P2 = random.randint(0, 9999)
            P3 = random.randint(0, 9999)
            CedulaStr = f"{CodProv}-{P2:04d}-{P3:04d}"
            CedulaInt = CedulaStrAInt(CedulaStr)
            if CedulaInt not in CedulasExistentes:
                CedulasExistentes.add(CedulaInt)
                break
            Intentos += 1
            if Intentos > 200:
                return Agregados

        # 2) Nombre completo (lista de 3 strings).
        NombrePila = random.choice(Nombres)
        Apellido1 = random.choice(PrimerosApellidos)
        Apellido2 = random.choice(SegundosApellidos)
        ListaNombre = [NombrePila, Apellido1, Apellido2]

        # 3) Tipo de sangre como INDICE en TiposDeSangre.
        IndiceTipo = random.randint(0, len(TiposDeSangre) - 1)

        # 4) Sexo: booleano.
        EsHombre = random.choice([True, False])

        # 5) Fecha de nacimiento dentro del rango de mayor de edad.
        AnioNac = random.randint(AnioMin, AnioMax)
        MesNac = random.randint(1, 12)
        DiaNac = random.randint(1, DiasPorMes[MesNac])
        FechaNac = (DiaNac, MesNac, AnioNac)

        # 6) Peso valido (estrictamente > 50 y < 120).
        Peso = round(random.uniform(51.0, 119.0), 1)

        # 7) Correo con uno de los dominios permitidos.
        Login = f"{NombrePila.lower()}{random.randint(1, 999)}"
        Correo = f"{Login}@{random.choice(DominiosPermitidos)}"

        # 8) Telefono con primer digito permitido.
        PrimerDigito = random.choice(PrimerosDigitosTelefono)
        Resto = random.randint(0, 9999999)
        TelefonoStr = f"{PrimerDigito}{Resto:07d}"
        Telefono = f"{TelefonoStr[:4]}-{TelefonoStr[4:]}"

        # 9) Estado: 80% activos, 20% inactivos con justificacion 1-7.
        if random.random() < 0.2:
            Estado = 0
            Justificacion = random.randint(1, 7)
        else:
            Estado = 1
            Justificacion = 0

        NuevaFila = [
            ListaNombre, CedulaInt, IndiceTipo, EsHombre, FechaNac,
            Peso, Correo, Telefono, Estado, Justificacion,
        ]
        Donadores.append(NuevaFila)
        Agregados += 1

    return Agregados


def JustificacionCompleta(IndiceJustificacion):
    """
    Devuelve el texto completo de una justificacion de rechazo (en
    lugar de su codigo numerico).

    Args:
        IndiceJustificacion (int): 0-7.

    Returns:
        str: texto completo de la justificacion.
    """
    return Justificaciones.get(IndiceJustificacion, "Justificacion desconocida")
