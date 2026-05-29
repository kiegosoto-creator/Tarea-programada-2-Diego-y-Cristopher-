"""
================================================================================
Archivo: gui/ventana_principal.py
Proposito:
    Ventana raiz del sistema con los 7 botones del menu principal:

        1. Insertar donador
        2. Generar donadores
        3. Actualizar datos del donador
        4. Eliminar donador
        5. Insertar lugar de donacion segun provincia
        6. Reportes
        7. Salir

    Si NO hay base de datos cargada (matriz vacia), solo se habilitan
    los botones 1, 2, 5 y 7. En cuanto se agregue al menos un donador
    (via Insertar o Generar), se habilitan los 7.

Convencion del proyecto:
    - Variables y atributos en NombreCamello.
    - Sin uso de la palabra clave 'global'.
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modelo_datos import HayBaseDeDatos
from persistencia import GuardarBaseDeDatos


class VentanaPrincipal:
    """
    Ventana raiz del sistema. Recibe la raiz de Tkinter y un booleano
    que indica si la base de datos pudo cargarse desde memoria
    secundaria al iniciar la aplicacion.
    """

    # Identificadores de cada boton del menu. Se usan como indices para
    # decidir cuales se habilitan cuando la BD esta vacia.
    BotonesPermitidosSinBd = {1, 2, 5, 7}

    def __init__(self, Raiz, BaseDeDatosCargada):
        """
        Args:
            Raiz (tk.Tk): ventana raiz creada en Main.py.
            BaseDeDatosCargada (bool): True si se logro cargar la BD
                                       desde memoria secundaria.
        """
        self.Raiz = Raiz
        self.BotonesMenu = {}  # numero_de_boton -> widget Button

        self._ConfigurarVentana()
        self._ConstruirEncabezado()
        self._ConstruirBotones()
        self._AplicarEstadoBotones()

        # Cada vez que la raiz reciba foco, refrescamos los botones por si
        # la matriz cambio de tamanio dentro de una sub-ventana.
        self.Raiz.bind("<FocusIn>", self._AlRecibirFoco)

        # Indicar al usuario el estado inicial de la BD.
        if BaseDeDatosCargada:
            messagebox.showinfo("Base de datos",
                                "Base de datos cargada correctamente desde "
                                "memoria secundaria.")

    # ------------------------------------------------------------------
    # Construccion de la interfaz
    # ------------------------------------------------------------------

    def _ConfigurarVentana(self):
        """Aplica titulo, tamanio y centrado a la ventana raiz."""
        self.Raiz.title("Banco Nacional de Sangre - Sistema de Donadores")
        self.Raiz.geometry("520x560")
        self.Raiz.resizable(False, False)
        self.Raiz.configure(bg="#fafafa")

        # Cerrar con la X tambien debe ejecutar la logica de salida.
        self.Raiz.protocol("WM_DELETE_WINDOW", self._Salir)

    def _ConstruirEncabezado(self):
        """Coloca el titulo y subtitulo en la parte superior."""
        MarcoEncabezado = tk.Frame(self.Raiz, bg="#b00", pady=14)
        MarcoEncabezado.pack(fill="x")

        Titulo = tk.Label(
            MarcoEncabezado,
            text="Banco Nacional de Sangre",
            font=("Arial", 18, "bold"),
            bg="#b00", fg="white",
        )
        Titulo.pack()

        Subtitulo = tk.Label(
            MarcoEncabezado,
            text="Donar sangre es donar vida",
            font=("Arial", 11, "italic"),
            bg="#b00", fg="white",
        )
        Subtitulo.pack()

    def _ConstruirBotones(self):
        """
        Crea los 7 botones del menu principal y los registra en el
        diccionario self.BotonesMenu para poder manipular su estado.
        """
        Definiciones = [
            (1, "1. Insertar donador",                       self._AbrirInsertar),
            (2, "2. Generar donadores",                      self._AbrirGenerar),
            (3, "3. Actualizar datos del donador",           self._AbrirActualizar),
            (4, "4. Eliminar donador",                       self._AbrirEliminar),
            (5, "5. Insertar lugar de donacion",             self._AbrirInsertarLugar),
            (6, "6. Reportes",                               self._AbrirReportes),
            (7, "7. Salir",                                  self._Salir),
        ]

        MarcoBotones = tk.Frame(self.Raiz, bg="#fafafa", pady=18)
        MarcoBotones.pack(expand=True, fill="both", padx=40)

        for Numero, Texto, Comando in Definiciones:
            Boton = tk.Button(
                MarcoBotones,
                text=Texto,
                command=Comando,
                font=("Arial", 12),
                width=32, pady=8,
                bg="#fff", fg="#222",
                activebackground="#ffe0e0",
                relief="raised", bd=2,
                cursor="hand2",
            )
            Boton.pack(pady=4)
            self.BotonesMenu[Numero] = Boton

    # ------------------------------------------------------------------
    # Logica de habilitado de botones
    # ------------------------------------------------------------------

    def _AplicarEstadoBotones(self):
        """
        Habilita o deshabilita los botones segun haya o no donadores
        en la matriz. Si la matriz esta vacia, solo quedan activos los
        botones 1, 2, 5 y 7. Si hay al menos un donador, se activan
        los 7.
        """
        HayDatos = HayBaseDeDatos()
        for Numero, Boton in self.BotonesMenu.items():
            if HayDatos or Numero in VentanaPrincipal.BotonesPermitidosSinBd:
                Boton.config(state="normal")
            else:
                Boton.config(state="disabled")

    def _AlRecibirFoco(self, _Evento):
        """
        Callback ligado a <FocusIn>. Reaplica el estado de los botones
        para que, al cerrar una sub-ventana, el menu refleje si ya hay
        donadores cargados.
        """
        self._AplicarEstadoBotones()

    # ------------------------------------------------------------------
    # Callbacks de cada boton
    #
    # Cada uno intenta abrir su sub-ventana. Mientras una sub-ventana
    # no este implementada, se muestra un aviso informativo para que el
    # usuario sepa que el boton respondio.
    # ------------------------------------------------------------------

    def _AbrirInsertar(self):
        """Abre la ventana de insertar donador."""
        self._AbrirSubventana(
            "gui.ventana_insertar", "VentanaInsertar", "Insertar donador")

    def _AbrirGenerar(self):
        """Abre la ventana de generar donadores aleatoriamente."""
        self._AbrirSubventana(
            "gui.ventana_generar", "VentanaGenerar", "Generar donadores")

    def _AbrirActualizar(self):
        """Abre la ventana de actualizar datos del donador."""
        self._AbrirSubventana(
            "gui.ventana_actualizar", "VentanaActualizar",
            "Actualizar donador")

    def _AbrirEliminar(self):
        """Abre la ventana de eliminar donador."""
        self._AbrirSubventana(
            "gui.ventana_eliminar", "VentanaEliminar", "Eliminar donador")

    def _AbrirInsertarLugar(self):
        """Abre la ventana de insertar lugar de donacion."""
        self._AbrirSubventana(
            "gui.ventana_lugar_donacion", "VentanaLugarDonacion",
            "Insertar lugar de donacion")

    def _AbrirReportes(self):
        """Abre la ventana de reportes."""
        self._AbrirSubventana(
            "gui.ventana_reportes", "VentanaReportes", "Reportes")

    def _AbrirSubventana(self, RutaModulo, NombreClase, EtiquetaUsuario):
        """
        Helper generico: importa el modulo de la sub-ventana y la
        instancia. Si la sub-ventana todavia no esta implementada
        (su __init__ no construye widgets) se muestra un aviso.

        Args:
            RutaModulo (str): por ejemplo 'gui.ventana_insertar'.
            NombreClase (str): nombre de la clase dentro del modulo.
            EtiquetaUsuario (str): nombre amigable para el aviso.
        """
        try:
            Modulo = __import__(RutaModulo, fromlist=[NombreClase])
            Clase = getattr(Modulo, NombreClase)
            Instancia = Clase(self.Raiz)
            # Verificamos si la sub-ventana realmente creo widgets. Si
            # es un Toplevel valido tendra un titulo asignado.
            if not isinstance(Instancia, tk.Toplevel):
                messagebox.showinfo(
                    EtiquetaUsuario,
                    f"La ventana de '{EtiquetaUsuario}' aun esta en "
                    "construccion.")
        except (ImportError, AttributeError, TypeError) as Error:
            messagebox.showinfo(
                EtiquetaUsuario,
                f"La ventana de '{EtiquetaUsuario}' aun esta en "
                f"construccion.\n\nDetalle: {Error}")

    # ------------------------------------------------------------------
    # Salida
    # ------------------------------------------------------------------

    def _Salir(self):
        """
        Muestra el mensaje "Donar sangre, es donar vida", persiste la
        base de datos y cierra la aplicacion.
        """
        # Solo guardamos si hay datos en la matriz (evita crear un JSON
        # vacio si el usuario abrio el sistema sin hacer nada).
        if HayBaseDeDatos():
            GuardarBaseDeDatos()

        messagebox.showinfo("Hasta pronto",
                            "Donar sangre, es donar vida")
        self.Raiz.destroy()
