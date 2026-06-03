"""
================================================================================
Tarea Programada #2 - Donemos Sangre, demos vida...
Taller de Programacion - I Semestre 2026
Escuela de Ingenieria en Computacion, Tecnologico de Costa Rica

Integrantes:
    - Cristhoper Jara Salazar
    - Diego Kim

Archivo: Main.py
Proposito:
    Punto de entrada de la aplicacion. Carga la base de datos desde memoria
    secundaria (si existe), instancia el modelo global y lanza la ventana
    principal del sistema.

Uso:
    python Main.py
================================================================================
"""

import tkinter as tk

from modelo_datos import InicializarModelo
from persistencia import CargarBaseDeDatos
from gui.ventana_principal import VentanaPrincipal


def Main():
    """
    Funcion principal de la aplicacion.

    1. Crea la ventana raiz de Tkinter.
    2. Intenta cargar la base de datos desde memoria secundaria.
       - Si existe, los 7 botones del menu principal se activan.
       - Si no existe, solo se activan los botones 1, 2, 5 y 7.
    3. Lanza el bucle principal de la interfaz grafica.
    """
    InicializarModelo()
    BaseDeDatosCargada = CargarBaseDeDatos()

    Raiz = tk.Tk()
    VentanaPrincipal(Raiz, BaseDeDatosCargada=BaseDeDatosCargada)
    Raiz.mainloop()


if __name__ == "__main__":
    Main()
