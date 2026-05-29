"""
================================================================================
Archivo: gui/ventana_eliminar.py
Proposito:
    Ventana "Eliminar donador". Solicita la cedula; si no existe
    muestra el mensaje correspondiente. Si existe, solicita la
    justificacion del rechazo (Combobox con las 7 razones de Gemini)
    y, al confirmar, cambia el estado a 0 (NO se borra la fila).
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

import modelo_datos
from modelo_datos import Justificaciones, IdxEstado, IdxJustificacion
import validaciones as Val
from logica_negocio import BuscarDonadorPorCedula
from persistencia import GuardarBaseDeDatos


class VentanaEliminar(tk.Toplevel):
    """Ventana Toplevel para eliminar (dar de baja) un donador."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Eliminar donador")
        self.geometry("620x340")
        self.resizable(False, False)
        self.configure(bg="#fafafa")

        self.IndiceDonadorActual = -1
        self.VarCedulaBusqueda = tk.StringVar()
        self.VarJustificacion = tk.StringVar()
        self.MarcoJustif = None

        self._ConstruirBuscador()
        self.transient(Padre)
        self.grab_set()

    def _ConstruirBuscador(self):
        """Caja de texto para cedula + boton 'Buscar'."""
        MarcoBuscar = tk.Frame(self, bg="#fafafa", padx=24, pady=18)
        MarcoBuscar.pack(fill="x")

        tk.Label(MarcoBuscar, text="Eliminar donador",
                 font=("Arial", 14, "bold"), bg="#fafafa",
                 fg="#b00", pady=4).pack()

        SubMarco = tk.Frame(MarcoBuscar, bg="#fafafa", pady=8)
        SubMarco.pack()
        tk.Label(SubMarco, text="Cedula (#-####-####):",
                 bg="#fafafa", font=("Arial", 11)).pack(side="left", padx=4)
        tk.Entry(SubMarco, textvariable=self.VarCedulaBusqueda,
                 width=15, font=("Arial", 11)).pack(side="left", padx=4)
        tk.Button(SubMarco, text="Buscar", command=self._Buscar,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=10, pady=2, cursor="hand2", bd=2).pack(side="left", padx=4)
        tk.Button(SubMarco, text="Regresar", command=self.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=10, pady=2, cursor="hand2", bd=2).pack(side="left", padx=4)

    def _Buscar(self):
        """Valida la cedula y muestra el Combobox de justificaciones."""
        TextoCedula = self.VarCedulaBusqueda.get().strip()
        Ok, Msg = Val.ValidarCedula(TextoCedula)
        if not Ok:
            messagebox.showerror("Cedula invalida", Msg, parent=self)
            return

        CedulaInt = Val.CedulaStrAInt(TextoCedula)
        Indice = BuscarDonadorPorCedula(CedulaInt)
        if Indice == -1:
            messagebox.showinfo(
                "Cedula no registrada",
                f"La persona con el numero de cedula: {TextoCedula} "
                "no esta registrado en la base de datos del Banco de "
                "Sangre aun.", parent=self)
            return

        if modelo_datos.Donadores[Indice][IdxEstado] == 0:
            messagebox.showinfo(
                "Donador inactivo",
                f"La persona con cedula {TextoCedula} ya esta marcada "
                "como NO activa.", parent=self)
            return

        self.IndiceDonadorActual = Indice
        self._ConstruirSeleccionJustificacion(Indice)

    def _ConstruirSeleccionJustificacion(self, IndiceDonador):
        """Combobox con las 7 razones de rechazo + Confirmar/Cancelar."""
        if self.MarcoJustif is not None:
            self.MarcoJustif.destroy()

        self.MarcoJustif = tk.Frame(self, bg="#fafafa", padx=24, pady=8)
        self.MarcoJustif.pack(fill="both", expand=True)

        OpcionesJustif = [f"{Codigo} - {Texto[:60]}..."
                          for Codigo, Texto in sorted(Justificaciones.items())
                          if Codigo > 0]

        tk.Label(self.MarcoJustif,
                 text="Seleccione la justificacion del rechazo:",
                 bg="#fafafa", font=("Arial", 11),
                 anchor="w").pack(fill="x", pady=4)

        ttk.Combobox(self.MarcoJustif, textvariable=self.VarJustificacion,
                     values=OpcionesJustif, state="readonly",
                     width=70, font=("Arial", 10)).pack(fill="x", pady=4)

        MarcoBotones = tk.Frame(self.MarcoJustif, bg="#fafafa", pady=12)
        MarcoBotones.pack()
        tk.Button(MarcoBotones, text="Confirmar",
                  command=self._ConfirmarEliminacion,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2", bd=2).pack(side="left", padx=8)
        tk.Button(MarcoBotones, text="Cancelar",
                  command=self._RechazarEliminacion,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2", bd=2).pack(side="left", padx=8)

    def _ConfirmarEliminacion(self):
        """Cambia estado a 0 y registra justificacion."""
        Seleccion = self.VarJustificacion.get().strip()
        if not Seleccion:
            messagebox.showerror("Error",
                                 "Debe seleccionar una justificacion.",
                                 parent=self)
            return

        CodigoJustif = int(Seleccion.split(" - ")[0])
        Fila = modelo_datos.Donadores[self.IndiceDonadorActual]
        Fila[IdxEstado] = 0
        Fila[IdxJustificacion] = CodigoJustif
        GuardarBaseDeDatos()

        messagebox.showinfo("Donador eliminado",
                            "Donador eliminado satisfactoriamente.",
                            parent=self)
        self.destroy()

    def _RechazarEliminacion(self):
        """Muestra 'Donador NO eliminado.' y se mantiene en la ventana."""
        messagebox.showinfo("Cancelado",
                            "Donador NO eliminado.", parent=self)
