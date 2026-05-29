"""
================================================================================
Archivo: gui/ventana_lugar_donacion.py
Proposito:
    Ventana "Insertar lugar de donacion segun provincia". Solicita
    el nombre de la provincia (Combobox leyendo del diccionario global)
    y el nuevo lugar (Text). Antes de insertar verifica que el lugar
    no exista ya en esa provincia.
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

import modelo_datos
from modelo_datos import Provincias
from persistencia import GuardarBaseDeDatos


class VentanaLugarDonacion(tk.Toplevel):
    """Ventana Toplevel para insertar un lugar de donacion."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Insertar lugar de donacion")
        self.geometry("520x340")
        self.resizable(False, False)
        self.configure(bg="#fafafa")

        self.VarProvincia = tk.StringVar()
        self._ConstruirFormulario()
        self.transient(Padre)
        self.grab_set()

    def _ConstruirFormulario(self):
        """Combobox de provincia + area de texto + botones."""
        Marco = tk.Frame(self, bg="#fafafa", padx=24, pady=18)
        Marco.pack(fill="both", expand=True)

        tk.Label(Marco, text="Insertar lugar de donacion",
                 font=("Arial", 14, "bold"), bg="#fafafa",
                 fg="#b00", pady=8).pack()

        OpcionesProvincia = [f"{C} - {N}" for C, N in sorted(Provincias.items())]
        MarcoProv = tk.Frame(Marco, bg="#fafafa", pady=4)
        MarcoProv.pack(fill="x", pady=4)
        tk.Label(MarcoProv, text="Provincia:", bg="#fafafa",
                 font=("Arial", 11), width=12,
                 anchor="w").pack(side="left")
        ttk.Combobox(MarcoProv, textvariable=self.VarProvincia,
                     values=OpcionesProvincia, state="readonly",
                     width=30, font=("Arial", 11)).pack(side="left", padx=4)

        tk.Label(Marco, text="Nuevo lugar de donacion:",
                 bg="#fafafa", font=("Arial", 11),
                 anchor="w").pack(fill="x", pady=(8, 2))
        self.AreaTexto = tk.Text(Marco, height=4, width=50,
                                 font=("Arial", 11), wrap="word")
        self.AreaTexto.pack(fill="x")

        MarcoBotones = tk.Frame(Marco, bg="#fafafa")
        MarcoBotones.pack(pady=12)
        tk.Button(MarcoBotones, text="Insertar", command=self._Insertar,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2", bd=2).pack(side="left", padx=8)
        tk.Button(MarcoBotones, text="Salir", command=self.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2", bd=2).pack(side="left", padx=8)

    def _Insertar(self):
        """Verifica no duplicado y agrega al diccionario global."""
        SeleccionProvincia = self.VarProvincia.get().strip()
        NuevoLugar = self.AreaTexto.get("1.0", "end").strip()

        if not SeleccionProvincia:
            messagebox.showerror("Error",
                                 "Debe seleccionar una provincia.",
                                 parent=self)
            return
        if not NuevoLugar:
            messagebox.showerror("Error",
                                 "Debe indicar el nombre del nuevo lugar.",
                                 parent=self)
            return

        CodigoProvincia = int(SeleccionProvincia.split(" - ")[0])
        ListaActual = modelo_datos.LugaresDonacion.setdefault(
            CodigoProvincia, [])

        Existentes = [L.lower() for L in ListaActual]
        if NuevoLugar.lower() in Existentes:
            messagebox.showwarning(
                "Lugar duplicado",
                f"El lugar '{NuevoLugar}' ya esta registrado en la "
                f"provincia de {Provincias[CodigoProvincia]}.",
                parent=self)
            return

        ListaActual.append(NuevoLugar)
        GuardarBaseDeDatos()
        messagebox.showinfo(
            "Lugar agregado",
            f"'{NuevoLugar}' agregado a la lista de lugares de la "
            f"provincia de {Provincias[CodigoProvincia]}.",
            parent=self)
        self.AreaTexto.delete("1.0", "end")
