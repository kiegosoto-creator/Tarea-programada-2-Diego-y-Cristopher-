"""
================================================================================
Archivo: gui/ventana_actualizar.py
Proposito:
    Ventana "Actualizar datos del donador". Solicita la cedula; si no
    existe muestra el mensaje correspondiente. Si existe, muestra el
    formulario completo con la cedula en solo lectura y permite
    modificar el resto. Confirma o rechaza la actualizacion.
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

import modelo_datos
from modelo_datos import (
    TiposDeSangre, IdxNombre, IdxCedula, IdxTipoSangre, IdxSexo,
    IdxFechaNac, IdxPeso, IdxCorreo, IdxTelefono,
)
import validaciones as Val
from logica_negocio import (
    TipoSangreAIndice, IndiceATipoSangre, BuscarDonadorPorCedula,
)
from persistencia import GuardarBaseDeDatos


class VentanaActualizar(tk.Toplevel):
    """Ventana Toplevel para actualizar un donador existente."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Actualizar donador")
        self.geometry("560x600")
        self.resizable(False, False)
        self.configure(bg="#fafafa")

        self.IndiceDonadorActual = -1
        self.VarCedulaBusqueda = tk.StringVar()
        self.MarcoFormulario = None

        self._ConstruirBuscador()
        self.transient(Padre)
        self.grab_set()

    def _ConstruirBuscador(self):
        """Caja de texto para cedula + boton 'Buscar'."""
        MarcoBuscar = tk.Frame(self, bg="#fafafa", padx=24, pady=18)
        MarcoBuscar.pack(fill="x")

        tk.Label(MarcoBuscar, text="Actualizar donador",
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
        """Valida la cedula y, si existe, llena el formulario."""
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
                "Sangre aun.",
                parent=self)
            return

        self.IndiceDonadorActual = Indice
        self._ConstruirFormularioEdicion(Indice)

    def _ConstruirFormularioEdicion(self, IndiceDonador):
        """Construye el formulario con los datos del donador, cedula readonly."""
        if self.MarcoFormulario is not None:
            self.MarcoFormulario.destroy()

        Fila = modelo_datos.Donadores[IndiceDonador]
        self.MarcoFormulario = tk.Frame(self, bg="#fafafa", padx=24, pady=8)
        self.MarcoFormulario.pack(fill="both", expand=True)

        self.VarNombre = tk.StringVar(value=" ".join(Fila[IdxNombre]))
        D, M, A = Fila[IdxFechaNac]
        self.VarFecha = tk.StringVar(value=f"{D:02d}/{M:02d}/{A:04d}")
        self.VarTipoSangre = tk.StringVar(
            value=IndiceATipoSangre(Fila[IdxTipoSangre]))
        self.VarSexo = tk.BooleanVar(value=Fila[IdxSexo])
        self.VarPeso = tk.StringVar(value=str(Fila[IdxPeso]))
        self.VarTelefono = tk.StringVar(value=Fila[IdxTelefono])
        self.VarCorreo = tk.StringVar(value=Fila[IdxCorreo])

        FilaActual = 0
        tk.Label(self.MarcoFormulario, text="Cedula:", bg="#fafafa",
                 font=("Arial", 11), anchor="w").grid(
                     row=FilaActual, column=0, sticky="w", pady=4)
        tk.Entry(self.MarcoFormulario,
                 textvariable=tk.StringVar(
                     value=Val.CedulaIntAStr(Fila[IdxCedula])),
                 width=30, font=("Arial", 11),
                 state="readonly").grid(
                     row=FilaActual, column=1, sticky="ew", pady=4)
        FilaActual += 1

        for Etiqueta, Variable in [
            ("Nombre completo:", self.VarNombre),
            ("Fecha (DD/MM/AAAA):", self.VarFecha),
        ]:
            tk.Label(self.MarcoFormulario, text=Etiqueta, bg="#fafafa",
                     font=("Arial", 11), anchor="w").grid(
                         row=FilaActual, column=0, sticky="w", pady=4)
            tk.Entry(self.MarcoFormulario, textvariable=Variable,
                     width=30, font=("Arial", 11)).grid(
                         row=FilaActual, column=1, sticky="ew", pady=4)
            FilaActual += 1

        tk.Label(self.MarcoFormulario, text="Tipo de sangre:", bg="#fafafa",
                 font=("Arial", 11), anchor="w").grid(
                     row=FilaActual, column=0, sticky="w", pady=4)
        ttk.Combobox(self.MarcoFormulario, textvariable=self.VarTipoSangre,
                     values=list(TiposDeSangre), state="readonly",
                     width=28, font=("Arial", 11)).grid(
                         row=FilaActual, column=1, sticky="ew", pady=4)
        FilaActual += 1

        tk.Label(self.MarcoFormulario, text="Sexo:", bg="#fafafa",
                 font=("Arial", 11), anchor="w").grid(
                     row=FilaActual, column=0, sticky="w", pady=4)
        MarcoSexo = tk.Frame(self.MarcoFormulario, bg="#fafafa")
        MarcoSexo.grid(row=FilaActual, column=1, sticky="w", pady=4)
        tk.Radiobutton(MarcoSexo, text="Masculino",
                       variable=self.VarSexo, value=True,
                       bg="#fafafa", font=("Arial", 11)).pack(side="left")
        tk.Radiobutton(MarcoSexo, text="Femenino",
                       variable=self.VarSexo, value=False,
                       bg="#fafafa", font=("Arial", 11)).pack(side="left")
        FilaActual += 1

        for Etiqueta, Variable in [
            ("Peso (kg):", self.VarPeso),
            ("Telefono (####-####):", self.VarTelefono),
            ("Correo:", self.VarCorreo),
        ]:
            tk.Label(self.MarcoFormulario, text=Etiqueta, bg="#fafafa",
                     font=("Arial", 11), anchor="w").grid(
                         row=FilaActual, column=0, sticky="w", pady=4)
            tk.Entry(self.MarcoFormulario, textvariable=Variable,
                     width=30, font=("Arial", 11)).grid(
                         row=FilaActual, column=1, sticky="ew", pady=4)
            FilaActual += 1

        MarcoBotones = tk.Frame(self.MarcoFormulario, bg="#fafafa", pady=12)
        MarcoBotones.grid(row=FilaActual, column=0, columnspan=2)
        tk.Button(MarcoBotones, text="Confirmar",
                  command=self._ConfirmarActualizacion,
                  bg="#080", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2", bd=2).pack(side="left", padx=8)
        tk.Button(MarcoBotones, text="Rechazar",
                  command=self._RechazarActualizacion,
                  bg="#888", fg="white", font=("Arial", 11, "bold"),
                  width=12, pady=4, cursor="hand2", bd=2).pack(side="left", padx=8)

    def _ConfirmarActualizacion(self):
        """Valida campos editados y actualiza la matriz."""
        Errores = []

        Partes = self.VarNombre.get().strip().split()
        if len(Partes) != 3:
            Errores.append("Nombre: debe ser 3 palabras (nombre + 2 apellidos).")

        OkF, MsgF = Val.ValidarFecha(self.VarFecha.get())
        if not OkF:
            Errores.append(f"Fecha: {MsgF}")

        if not self.VarTipoSangre.get():
            Errores.append("Tipo de sangre: debe seleccionar uno.")

        OkP, MsgP, ValorPeso = Val.ValidarPeso(self.VarPeso.get())
        if not OkP:
            Errores.append(f"Peso: {MsgP}")

        OkT, MsgT = Val.ValidarTelefono(self.VarTelefono.get())
        if not OkT:
            Errores.append(f"Telefono: {MsgT}")

        OkC, MsgC = Val.ValidarCorreo(self.VarCorreo.get())
        if not OkC:
            Errores.append(f"Correo: {MsgC}")

        if Errores:
            messagebox.showerror("Errores en el formulario",
                                 "\n\n".join(Errores), parent=self)
            return

        FilaActual = modelo_datos.Donadores[self.IndiceDonadorActual]
        D, M, A = (int(P) for P in self.VarFecha.get().strip().split("/"))
        NuevaFila = [
            Partes,
            FilaActual[IdxCedula],
            TipoSangreAIndice(self.VarTipoSangre.get()),
            self.VarSexo.get(),
            (D, M, A),
            ValorPeso,
            self.VarCorreo.get().strip(),
            self.VarTelefono.get().strip(),
            FilaActual[modelo_datos.IdxEstado],
            FilaActual[modelo_datos.IdxJustificacion],
        ]
        modelo_datos.Donadores[self.IndiceDonadorActual] = NuevaFila
        GuardarBaseDeDatos()

        messagebox.showinfo("Exito",
                            "Datos actualizados correctamente.",
                            parent=self)
        self.destroy()

    def _RechazarActualizacion(self):
        """Muestra 'Datos No actualizados.' y se mantiene en la ventana."""
        messagebox.showinfo("Sin cambios",
                            "Datos No actualizados.", parent=self)
