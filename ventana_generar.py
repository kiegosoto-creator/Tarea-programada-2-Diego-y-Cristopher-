"""
================================================================================
Archivo: gui/ventana_generar.py
Proposito:
    Ventana "Generar donadores": solicita la cantidad de donadores a
    crear aleatoriamente y los agrega a la matriz respetando todas las
    restricciones (cedulas unicas, peso valido, tipo de sangre leido
    de la tupla global, edad valida, correo y telefono con formato
    valido). Aproximadamente 20% quedan como NO activos con
    justificacion aleatoria del 1 al 7.
================================================================================
"""

import tkinter as tk
from tkinter import messagebox

from logica_negocio import GenerarDonadoresAleatorios
from persistencia import GuardarBaseDeDatos


class VentanaGenerar(tk.Toplevel):
    """Ventana Toplevel para generar donadores aleatoriamente."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Generar donadores")
        self.geometry("460x260")
        self.resizable(False, False)
        self.configure(bg="#fafafa")

        self.VarCantidad = tk.StringVar()
        self._ConstruirFormulario()
        self.transient(Padre)
        self.grab_set()

    def _ConstruirFormulario(self):
        """Crea la caja de texto para la cantidad y los botones."""
        Marco = tk.Frame(self, bg="#fafafa", padx=24, pady=18)
        Marco.pack(fill="both", expand=True)

        tk.Label(Marco, text="Generar donadores aleatorios",
                 font=("Arial", 14, "bold"), bg="#fafafa",
                 fg="#b00", pady=8).pack()

        tk.Label(Marco,
                 text="Indique cuantos donadores desea crear.\n"
                      "Cada uno tendra datos aleatorios validos. "
                      "Aproximadamente\nel 20% quedaran inactivos con "
                      "una justificacion aleatoria.",
                 bg="#fafafa", font=("Arial", 10),
                 justify="center").pack(pady=8)

        MarcoInput = tk.Frame(Marco, bg="#fafafa")
        MarcoInput.pack(pady=8)
        tk.Label(MarcoInput, text="Cantidad:",
                 bg="#fafafa", font=("Arial", 11)).pack(side="left", padx=4)
        tk.Entry(MarcoInput, textvariable=self.VarCantidad,
                 width=10, font=("Arial", 11),
                 justify="center").pack(side="left", padx=4)

        MarcoBotones = tk.Frame(Marco, bg="#fafafa")
        MarcoBotones.pack(pady=12)
        tk.Button(MarcoBotones, text="Generar", command=self._Generar,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2",
                  activebackground="#b00", bd=2).pack(side="left", padx=8)
        tk.Button(MarcoBotones, text="Regresar", command=self.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2",
                  activebackground="#888", bd=2).pack(side="left", padx=8)

    def _Generar(self):
        """
        Lee la cantidad ingresada, valida que sea > 0 y llama a
        GenerarDonadoresAleatorios. Muestra un resumen con cuantos
        se crearon. Persiste la BD al terminar.
        """
        TextoCantidad = self.VarCantidad.get().strip()
        if not TextoCantidad:
            messagebox.showerror("Error",
                                 "Debe indicar una cantidad.",
                                 parent=self)
            return
        try:
            Cantidad = int(TextoCantidad)
        except ValueError:
            messagebox.showerror("Error",
                                 "La cantidad debe ser un numero entero.",
                                 parent=self)
            return
        if Cantidad <= 0:
            messagebox.showerror("Error",
                                 "La cantidad debe ser mayor a 0.",
                                 parent=self)
            return

        Agregados = GenerarDonadoresAleatorios(Cantidad)
        GuardarBaseDeDatos()

        messagebox.showinfo(
            "Generacion completada",
            f"Se generaron {Agregados} donadores aleatoriamente.\n"
            "Aproximadamente el 20% quedan como NO activos con una "
            "justificacion aleatoria (codigos 1 al 7 de Gemini).",
            parent=self)
        self.VarCantidad.set("")
