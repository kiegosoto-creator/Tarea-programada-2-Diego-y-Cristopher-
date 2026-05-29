"""
================================================================================
Archivo: gui/ventana_reportes.py
Proposito:
    Ventana "Reportes" con 9 botones (8 reportes + lugares) y el
    boton "Regresar". Cada boton abre una sub-ventana para pedir los
    parametros del reporte (provincia, edad, tipo de sangre, segun
    corresponda) y luego invoca la funcion correspondiente en
    reportes.py que genera el HTML5.
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modelo_datos import Provincias, TiposDeSangre
import reportes as R


class VentanaReportes(tk.Toplevel):
    """Ventana Toplevel que despliega los botones de los reportes."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Reportes")
        self.geometry("520x560")
        self.resizable(False, False)
        self.configure(bg="#fafafa")

        self._ConstruirBotones()
        self.transient(Padre)
        self.grab_set()

    def _ConstruirBotones(self):
        """Botones para cada uno de los reportes + 'Regresar'."""
        MarcoTitulo = tk.Frame(self, bg="#b00", pady=10)
        MarcoTitulo.pack(fill="x")
        tk.Label(MarcoTitulo, text="Reportes",
                 font=("Arial", 16, "bold"),
                 bg="#b00", fg="white").pack()

        MarcoBotones = tk.Frame(self, bg="#fafafa", padx=24, pady=14)
        MarcoBotones.pack(expand=True, fill="both")

        Definiciones = [
            ("1. Donantes por provincia", self._ReportePorProvincia),
            ("2. Por rango de edad", self._ReportePorEdad),
            ("3. Por tipo de sangre y provincia", self._ReportePorTipoYProvincia),
            ("4. Lista completa", self._ReporteCompleto),
            ("5. Mujeres O- menores de 45", self._ReporteMujeresONegativo),
            ("6. A quien puede donar", self._ReporteAQuienDona),
            ("7. De quien puede recibir", self._ReporteDeQuienRecibe),
            ("8. Donantes NO activos", self._ReporteNoActivos),
            ("9. Lugares de donacion", self._ReporteLugares),
        ]
        for Texto, Comando in Definiciones:
            tk.Button(MarcoBotones, text=Texto, command=Comando,
                      font=("Arial", 11), width=36, pady=4,
                      bg="#fff", fg="#222", relief="raised", bd=2,
                      cursor="hand2",
                      activebackground="#ffe0e0").pack(pady=3)

        tk.Button(MarcoBotones, text="Regresar", command=self.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=36, pady=4, cursor="hand2", bd=2).pack(pady=12)

    def _MostrarResultado(self, OkGenerado, NombreReporte):
        """Muestra 'Reporte creado satisfactoriamente' o 'Reporte no creado'."""
        if OkGenerado:
            messagebox.showinfo(NombreReporte,
                                "Reporte creado satisfactoriamente.",
                                parent=self)
        else:
            messagebox.showerror(NombreReporte,
                                 "Reporte no creado.", parent=self)

    def _AbrirSubVentanaProvincia(self, Titulo, GeneradorFn):
        """Sub-ventana con Combobox de provincia + Generar/Regresar."""
        Sub = tk.Toplevel(self)
        Sub.title(Titulo)
        Sub.geometry("420x180")
        Sub.configure(bg="#fafafa")
        Sub.transient(self)
        Sub.grab_set()

        VarProv = tk.StringVar()
        Opciones = [f"{C} - {N}" for C, N in sorted(Provincias.items())]

        tk.Label(Sub, text=Titulo, bg="#fafafa",
                 font=("Arial", 12, "bold"), fg="#b00",
                 pady=8).pack()
        tk.Label(Sub, text="Provincia:", bg="#fafafa",
                 font=("Arial", 11)).pack(pady=4)
        ttk.Combobox(Sub, textvariable=VarProv, values=Opciones,
                     state="readonly", width=30,
                     font=("Arial", 11)).pack()

        def Generar():
            if not VarProv.get():
                messagebox.showerror("Error",
                                     "Seleccione una provincia.",
                                     parent=Sub)
                return
            Codigo = int(VarProv.get().split(" - ")[0])
            Ok = GeneradorFn(Codigo)
            self._MostrarResultado(Ok, Titulo)
            Sub.destroy()

        MarcoBtn = tk.Frame(Sub, bg="#fafafa", pady=10)
        MarcoBtn.pack()
        tk.Button(MarcoBtn, text="Generar reporte", command=Generar,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)
        tk.Button(MarcoBtn, text="Regresar", command=Sub.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)

    def _ReportePorProvincia(self):
        """Pide la provincia y genera el reporte de donantes activos."""
        self._AbrirSubVentanaProvincia(
            "Donantes por provincia", R.ReporteDonantesPorProvincia)

    def _ReportePorEdad(self):
        """Pide edad inicial (18-65) y opcionalmente edad final."""
        Sub = tk.Toplevel(self)
        Sub.title("Por rango de edad")
        Sub.geometry("420x240")
        Sub.configure(bg="#fafafa")
        Sub.transient(self)
        Sub.grab_set()

        VarIni = tk.StringVar()
        VarFin = tk.StringVar()

        tk.Label(Sub, text="Por rango de edad (18 a 65)",
                 bg="#fafafa", font=("Arial", 12, "bold"),
                 fg="#b00", pady=8).pack()

        F1 = tk.Frame(Sub, bg="#fafafa")
        F1.pack(pady=4)
        tk.Label(F1, text="Edad inicial:", bg="#fafafa",
                 font=("Arial", 11), width=14, anchor="e").pack(side="left")
        EntIni = tk.Entry(F1, textvariable=VarIni, width=8,
                          font=("Arial", 11), justify="center")
        EntIni.pack(side="left", padx=4)

        F2 = tk.Frame(Sub, bg="#fafafa")
        F2.pack(pady=4)
        tk.Label(F2, text="Edad final:", bg="#fafafa",
                 font=("Arial", 11), width=14, anchor="e").pack(side="left")
        EntFin = tk.Entry(F2, textvariable=VarFin, width=8,
                          font=("Arial", 11), justify="center",
                          state="disabled")
        EntFin.pack(side="left", padx=4)

        def OnIniCambia(*_Args):
            Texto = VarIni.get().strip()
            try:
                Valor = int(Texto)
                if 18 <= Valor <= 65:
                    EntFin.config(state="normal")
                    return
            except ValueError:
                pass
            EntFin.config(state="disabled")
        VarIni.trace_add("write", OnIniCambia)

        def Generar():
            try:
                Ini = int(VarIni.get().strip())
            except ValueError:
                messagebox.showerror("Error",
                                     "Edad inicial debe ser entero 18-65.",
                                     parent=Sub)
                return
            if not (18 <= Ini <= 65):
                messagebox.showerror("Error",
                                     "Edad inicial debe ser entre 18 y 65.",
                                     parent=Sub)
                return

            Fin = None
            if VarFin.get().strip():
                try:
                    Fin = int(VarFin.get().strip())
                except ValueError:
                    messagebox.showerror("Error",
                                         "Edad final debe ser entero 18-65.",
                                         parent=Sub)
                    return
                if not (18 <= Fin <= 65):
                    messagebox.showerror("Error",
                                         "Edad final debe ser entre 18 y 65.",
                                         parent=Sub)
                    return

            Ok = R.ReportePorRangoEdad(Ini, Fin)
            self._MostrarResultado(Ok, "Por rango de edad")
            Sub.destroy()

        MarcoBtn = tk.Frame(Sub, bg="#fafafa", pady=12)
        MarcoBtn.pack()
        tk.Button(MarcoBtn, text="Generar reporte", command=Generar,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)
        tk.Button(MarcoBtn, text="Regresar", command=Sub.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)

    def _ReportePorTipoYProvincia(self):
        """Pide tipo de sangre y provincia."""
        Sub = tk.Toplevel(self)
        Sub.title("Por tipo y provincia")
        Sub.geometry("420x240")
        Sub.configure(bg="#fafafa")
        Sub.transient(self)
        Sub.grab_set()

        VarTipo = tk.StringVar()
        VarProv = tk.StringVar()
        OpcionesProv = [f"{C} - {N}" for C, N in sorted(Provincias.items())]

        tk.Label(Sub, text="Por tipo de sangre y provincia",
                 bg="#fafafa", font=("Arial", 12, "bold"),
                 fg="#b00", pady=8).pack()
        tk.Label(Sub, text="Tipo de sangre:", bg="#fafafa",
                 font=("Arial", 11)).pack(pady=2)
        ttk.Combobox(Sub, textvariable=VarTipo,
                     values=list(TiposDeSangre), state="readonly",
                     width=28, font=("Arial", 11)).pack()
        tk.Label(Sub, text="Provincia:", bg="#fafafa",
                 font=("Arial", 11)).pack(pady=2)
        ttk.Combobox(Sub, textvariable=VarProv, values=OpcionesProv,
                     state="readonly", width=28,
                     font=("Arial", 11)).pack()

        def Generar():
            if not VarTipo.get() or not VarProv.get():
                messagebox.showerror("Error",
                                     "Seleccione tipo y provincia.",
                                     parent=Sub)
                return
            Codigo = int(VarProv.get().split(" - ")[0])
            Ok = R.ReportePorTipoYProvincia(VarTipo.get(), Codigo)
            self._MostrarResultado(Ok, "Por tipo y provincia")
            Sub.destroy()

        MarcoBtn = tk.Frame(Sub, bg="#fafafa", pady=12)
        MarcoBtn.pack()
        tk.Button(MarcoBtn, text="Generar reporte", command=Generar,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)
        tk.Button(MarcoBtn, text="Regresar", command=Sub.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)

    def _ReporteCompleto(self):
        """Sin parametros: lista completa de donantes activos."""
        self._MostrarResultado(R.ReporteListaCompleta(),
                               "Lista completa")

    def _ReporteMujeresONegativo(self):
        """Sin parametros: mujeres O- menores de 45."""
        self._MostrarResultado(R.ReporteMujeresONegativo(),
                               "Mujeres O-")

    def _ReporteNoActivos(self):
        """Sin parametros: donantes inactivos con justificacion textual."""
        self._MostrarResultado(R.ReporteDonantesNoActivos(),
                               "Donantes NO activos")

    def _ReporteLugares(self):
        """Sin parametros: lugares de donacion con cantidades."""
        self._MostrarResultado(R.ReporteLugaresDonacion(),
                               "Lugares de donacion")

    def _AbrirSubVentanaTipoSangre(self, Titulo, GeneradorFn):
        """Sub-ventana con Combobox de tipo + Generar/Regresar."""
        Sub = tk.Toplevel(self)
        Sub.title(Titulo)
        Sub.geometry("420x180")
        Sub.configure(bg="#fafafa")
        Sub.transient(self)
        Sub.grab_set()

        VarTipo = tk.StringVar()
        tk.Label(Sub, text=Titulo, bg="#fafafa",
                 font=("Arial", 12, "bold"), fg="#b00",
                 pady=8).pack()
        tk.Label(Sub, text="Tipo de sangre:", bg="#fafafa",
                 font=("Arial", 11)).pack(pady=4)
        ttk.Combobox(Sub, textvariable=VarTipo,
                     values=list(TiposDeSangre), state="readonly",
                     width=28, font=("Arial", 11)).pack()

        def Generar():
            if not VarTipo.get():
                messagebox.showerror("Error",
                                     "Seleccione un tipo de sangre.",
                                     parent=Sub)
                return
            Ok = GeneradorFn(VarTipo.get())
            self._MostrarResultado(Ok, Titulo)
            Sub.destroy()

        MarcoBtn = tk.Frame(Sub, bg="#fafafa", pady=10)
        MarcoBtn.pack()
        tk.Button(MarcoBtn, text="Generar reporte", command=Generar,
                  bg="#b00", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)
        tk.Button(MarcoBtn, text="Regresar", command=Sub.destroy,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=14).pack(side="left", padx=4)

    def _ReporteAQuienDona(self):
        """Pide tipo de sangre, ordena asc por provincia."""
        self._AbrirSubVentanaTipoSangre(
            "A quien puede donar", R.ReporteAQuienPuedeDonar)

    def _ReporteDeQuienRecibe(self):
        """Pide tipo de sangre, ordena desc por provincia."""
        self._AbrirSubVentanaTipoSangre(
            "De quien puede recibir", R.ReporteDeQuienPuedeRecibir)
