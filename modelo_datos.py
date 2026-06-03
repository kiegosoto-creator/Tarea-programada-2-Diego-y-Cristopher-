"""
================================================================================
Archivo: modelo_datos.py
Proposito:
    Contiene las estructuras de datos globales del sistema:
    - La matriz principal de donadores (lista de listas).
    - El diccionario de lugares de donacion por provincia.
    - La tupla de tipos de sangre.
    - El diccionario de justificaciones de rechazo (Gemini).
    - El diccionario de provincias (codigo -> nombre).

    Las funciones que mutan las estructuras NO usan la palabra clave
    'global' (preferencia academica). En su lugar mutan en sitio las
    listas y diccionarios definidos a nivel de modulo.

Estas estructuras son las exigidas por la consigna y no deben ser
sustituidas por clases ni objetos.
================================================================================
"""

# ----------------------------------------------------------------------
# Tupla con los tipos de sangre. En la matriz se almacena el INDICE
# de cada tipo en esta tupla, no el string.
# ----------------------------------------------------------------------
TiposDeSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")


# ----------------------------------------------------------------------
# Provincias de Costa Rica segun el primer digito de la cedula.
# Orden segun el Registro Civil del Tribunal Supremo de Elecciones.
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Diccionario inicial de lugares de donacion segun provincia.
# Clave = codigo de provincia (int)
# Valor = lista de strings con los hospitales/centros de donacion.
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Justificaciones de rechazo segun la informacion de Gemini en el
# PDF (pagina 14). El indice 0 representa "donador activo".
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Posiciones de los campos en cada fila de la matriz de donadores.
# Constantes para evitar "numeros magicos" en el codigo.
# ----------------------------------------------------------------------
IdxNombre = 0          # [nombre, apellido1, apellido2] - lista de 3 strings
IdxCedula = 1          # int
IdxTipoSangre = 2      # int (indice en TiposDeSangre)
IdxSexo = 3            # bool (True = Hombre, False = Mujer)
IdxFechaNac = 4        # tupla (DD, MM, AAAA)
IdxPeso = 5            # float
IdxCorreo = 6          # str
IdxTelefono = 7        # str
IdxEstado = 8          # int (1 = activo, 0 = inactivo)
IdxJustificacion = 9   # int (0-7)


# ----------------------------------------------------------------------
# Estructuras de datos en memoria RAM. Se inicializan vacias y se
# pueblan al cargar desde memoria secundaria o al insertar donadores.
#
# Importante: NO se reasignan estas referencias durante la ejecucion
# del programa, solo se mutan con .clear() / .append() / .update() para
# evitar el uso de 'global'.
# ----------------------------------------------------------------------
Donadores = []          # Matriz: lista de listas
LugaresDonacion = {}    # Diccionario: codigo_provincia -> lista de lugares


def InicializarModelo():
    """
    Reinicia las estructuras globales a su estado inicial sin usar
    'global'. Se aprovecha que Donadores y LugaresDonacion son objetos
    mutables: se vacian y se vuelven a llenar en sitio.
    """
    Donadores.clear()
    LugaresDonacion.clear()
    for Codigo, ListaLugares in LugaresDonacionInicial.items():
        # Copiamos la lista para no exponer la referencia original.
        LugaresDonacion[Codigo] = list(ListaLugares)


def HayBaseDeDatos():
    """
    Indica si la matriz de donadores tiene al menos un registro.
    Se usa para decidir que botones del menu principal habilitar.

    Returns:
        bool: True si hay donadores cargados, False en caso contrario.
    """
    return len(Donadores) > 0
