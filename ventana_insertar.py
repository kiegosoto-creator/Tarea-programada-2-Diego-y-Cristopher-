"""
================================================================================
Archivo: gui/ventana_insertar.py
Proposito:
    Ventana del formulario "Insertar donador". Solicita cedula, nombre
    completo, fecha de nacimiento, tipo de sangre, sexo, peso, telefono
    y correo. Aplica todas las validaciones de regex.

    Tras insertar muestra los 5 Mensajes de retroalimentacion:
        1. Mayoria de edad por mes y anio.
        2. Lugar de donacion segun provincia de la cedula.
        3. Validacion del peso (3 casos).
        4. A quien puede donar segun tipo de sangre.
        5. Recomendacion del video si es A+ o A-.

Convencion del proyecto:
    - Variables en NombreCamello.
    - Sin uso de 'global' (la matriz se muta accediendo a modelo_datos.Donadores).
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

import modelo_datos
from modelo_datos import TiposDeSangre
import validaciones as Val
from logica_negocio import (
    TipoSangreAIndice,
    ObtenerLugaresPorCedula,
    NombreProvincia,
    MensajeCompatibilidad,
    ExisteCedula,
)
from persistencia import GuardarBaseDeDatos


class VentanaInsertar(tk.Toplevel):
    """
    Ventana modal de inserción de un nuevo donador.
    Aplica todas las validaciones del enunciado y, tras insertar,
    despliega los 5 mensajes de retroalimentación.
    """

    def __init__(self, Padre):
        """
        Args:
            Padre (tk.Tk o tk.Toplevel): ventana padre.
        """
        super().__init__(Padre)
        self.title("Insertar donador")
        self.geometry("560x540")
        self.resizable(False, False)
        self.configure(bg="#fafafa")

        # Variables de Tk asociadas a cada campo del formulario.
        self.VarCedula = tk.StringVar()
        self.VarNombre = tk.StringVar()
        self.VarFecha = tk.StringVar()
        self.VarTipoSangre = tk.StringVar()
        self.VarSexo = tk.BooleanVar(value=True)   # True = Masculino por defecto
        self.VarPeso = tk.StringVar()
        self.VarTelefono = tk.StringVar()
        self.VarCorreo = tk.StringVar()

        self._ConstruirFormulario()
        self._ConstruirBotones()

        # Ventana modal.
        self.transient(Padre)
        self.grab_set()

    # ------------------------------------------------------------------
    # Construccion de la interfaz
    # ------------------------------------------------------------------

    def _ConstruirFormulario(self):
        """Crea las etiquetas, cajas de texto, combobox y radio buttons."""
        Marco = tk.Frame(self, bg="#fafafa", padx=24, pady=16)
        Marco.pack(fill="both", expand=True)

        # Titulo del formulario.
        tk.Label(Marco, text="Registro de nuevo donador",
                 font=("Arial", 14, "bold"), bg="#fafafa", fg="#b00",
                 pady=8).grid(row=0, column=0, columnspan=2, sticky="ew")

        # Cedula, nombre y fecha (campos de texto simples).
        FilasTexto = [
            ("Cedula (#-####-####):", self.VarCedula),
            ("Nombre completo:",      self.VarNombre),
            ("Fecha (DD/MM/AAAA):",   self.VarFecha),
        ]

        FilaActual = 1
        for Etiqueta, Variable in FilasTexto:
            self._AgregarFilaTexto(Marco, FilaActual, Etiqueta, Variable)
            FilaActual += 1

        # Tipo de sangre - Combobox.
        tk.Label(Marco, text="Tipo de sangre:", bg="#fafafa",
                 font=("Arial", 11), anchor="w").grid(
                     row=FilaActual, column=0, sticky="w", pady=4)
        ttk.Combobox(Marco, textvariable=self.VarTipoSangre,
                     values=list(TiposDeSangre),
                     state="readonly", width=28,
                     font=("Arial", 11)).grid(
                         row=FilaActual, column=1, sticky="ew", pady=4)
        FilaActual += 1

        # Sexo - Radio buttons (Masculino por defecto).
        tk.Label(Marco, text="Sexo:", bg="#fafafa",
                 font=("Arial", 11), anchor="w").grid(
                     row=FilaActual, column=0, sticky="w", pady=4)
        MarcoSexo = tk.Frame(Marco, bg="#fafafa")
        MarcoSexo.grid(row=FilaActual, column=1, sticky="w", pady=4)
        tk.Radiobutton(MarcoSexo, text="Masculino",
                       variable=self.VarSexo, value=True,
                       bg="#fafafa", font=("Arial", 11)).pack(
                           side="left", padx=4)
        tk.Radiobutton(MarcoSexo, text="Femenino",
                       variable=self.VarSexo, value=False,
                       bg="#fafafa", font=("Arial", 11)).pack(
                           side="left", padx=4)
        FilaActual += 1

        # Peso, telefono, correo (texto).
        FilasTexto2 = [
            ("Peso (kg):",                self.VarPeso),
            ("Telefono (####-####):",     self.VarTelefono),
            ("Correo:",                   self.VarCorreo),
        ]
        for Etiqueta, Variable in FilasTexto2:
            self._AgregarFilaTexto(Marco, FilaActual, Etiqueta, Variable)
            FilaActual += 1

    def _AgregarFilaTexto(self, Padre, Fila, Etiqueta, Variable):
        """
        Helper: crea una etiqueta y una caja de texto en una fila del grid.

        Args:
            Padre (tk.Widget): contenedor (el frame del formulario).
            Fila (int): numero de fila en el grid.
            Etiqueta (str): texto visible.
            Variable (tk.StringVar): variable asociada a la caja de texto.
        """
        tk.Label(Padre, text=Etiqueta, bg="#fafafa",
                 font=("Arial", 11), anchor="w").grid(
                     row=Fila, column=0, sticky="w", pady=4)
        tk.Entry(Padre, textvariable=Variable, width=30,
                 font=("Arial", 11)).grid(
                     row=Fila, column=1, sticky="ew", pady=4)

    def _ConstruirBotones(self):
        """Crea los botones Registrar, Limpiar y Regresar."""
        MarcoBotones = tk.Frame(self, bg="#fafafa", pady=12)
        MarcoBotones.pack(fill="x", padx=24)

        Definiciones = [
            ("Registrar", "#b00", self._Registrar),
            ("Limpiar",   "#666", self._Limpiar),
            ("Regresar",  "#888", self.destroy),
        ]
        for Texto, Color, Comando in Definiciones:
            tk.Button(MarcoBotones, text=Texto, command=Comando,
                      bg=Color, fg="white",
                      font=("Arial", 11, "bold"),
                      width=12, pady=4, cursor="hand2",
                      activebackground=Color, bd=2).pack(
                          side="left", padx=8, expand=True)

    # ------------------------------------------------------------------
    # Acciones de los botones
    # ------------------------------------------------------------------

    def _Registrar(self):
        """
        Recolecta los datos, valida cada uno y, si todo es correcto,
        agrega el donador a la matriz, persiste y muestra los 5
        mensajes de retroalimentacion en una ventana resumen.
        """
        # Recolectar y validar cada campo. Acumulamos errores para
        # mostrarlos todos juntos al usuario.
        Errores = []

        # --- Cedula ---
        TextoCedula = self.VarCedula.get()
        OkCedula, MsgCedula = Val.ValidarCedula(TextoCedula)
        if not OkCedula:
            Errores.append(f"Cedula: {MsgCedula}")

        # --- Nombre (esperamos 3 palabras: nombre + 2 apellidos) ---
        TextoNombre = self.VarNombre.get().strip()
        Partes = TextoNombre.split()
        if len(Partes) != 3:
            Errores.append("Nombre completo: debe contener el nombre, "
                           "el primer apellido y el segundo apellido "
                           "(3 palabras separadas por espacio).")
        else:
            for Parte in Partes:
                OkParte, MsgParte = Val.ValidarNombre(Parte)
                if not OkParte:
                    Errores.append(f"Nombre: {MsgParte}")
                    break

        # --- Fecha ---
        TextoFecha = self.VarFecha.get()
        OkFecha, MsgFecha = Val.ValidarFecha(TextoFecha)
        if not OkFecha:
            Errores.append(f"Fecha de nacimiento: {MsgFecha}")

        # --- Tipo de sangre ---
        TipoSangre = self.VarTipoSangre.get()
        if not TipoSangre:
            Errores.append("Tipo de sangre: debe seleccionar uno.")

        # --- Peso ---
        OkPeso, MsgPeso, ValorPeso = Val.ValidarPeso(self.VarPeso.get())
        if not OkPeso:
            Errores.append(f"Peso: {MsgPeso}")

        # --- Telefono ---
        OkTelefono, MsgTelefono = Val.ValidarTelefono(self.VarTelefono.get())
        if not OkTelefono:
            Errores.append(f"Telefono: {MsgTelefono}")

        # --- Correo ---
        OkCorreo, MsgCorreo = Val.ValidarCorreo(self.VarCorreo.get())
        if not OkCorreo:
            Errores.append(f"Correo: {MsgCorreo}")

        if Errores:
            messagebox.showerror("Errores en el formulario",
                                 "\n\n".join(Errores), parent=self)
            return

        # --- Verificar duplicado de cedula ---
        CedulaInt = Val.CedulaStrAInt(TextoCedula)
        if ExisteCedula(CedulaInt):
            messagebox.showerror(
                "Cedula duplicada",
                f"La cedula {TextoCedula.strip()} ya esta registrada "
                "en la base de datos.", parent=self)
            return

        # --- Construir la fila respetando los tipos exigidos ---
        Dia, Mes, Anio = (int(P) for P in TextoFecha.strip().split("/"))

        NuevaFila = [
            Partes,                              # nombre: [nom, ap1, ap2]
            CedulaInt,                           # cedula: int
            TipoSangreAIndice(TipoSangre),    # tipo: int (indice)
            self.VarSexo.get(),                  # sexo: bool
            (Dia, Mes, Anio),                    # fecha: tupla
            ValorPeso,                           # peso: float
            self.VarCorreo.get().strip(),        # correo: str
            self.VarTelefono.get().strip(),      # telefono: str
            1,                                   # estado: activo
            0,                                   # justificacion: ninguna
        ]
        modelo_datos.Donadores.append(NuevaFila)
        GuardarBaseDeDatos()

        # Construir y mostrar los 5 mensajes de retroalimentacion.
        Mensajes = self._ConstruirMensajesRetroalimentacion(
            Dia, Mes, Anio, CedulaInt, ValorPeso, TipoSangre)
        self._MostrarRetroalimentacion(Mensajes)
        self._Limpiar()

    def _Limpiar(self):
        """Borra todos los campos del formulario."""
        self.VarCedula.set("")
        self.VarNombre.set("")
        self.VarFecha.set("")
        self.VarTipoSangre.set("")
        self.VarSexo.set(True)
        self.VarPeso.set("")
        self.VarTelefono.set("")
        self.VarCorreo.set("")

    # ------------------------------------------------------------------
    # Retroalimentacion al usuario
    # ------------------------------------------------------------------

    def _ConstruirMensajesRetroalimentacion(self, Dia, Mes, Anio,
                                              CedulaInt, Peso, TipoSangre):
        """
        Construye los 5 mensajes exigidos por el enunciado tras una
        insercion exitosa.

        Args:
            Dia, Mes, Anio (int): fecha de nacimiento.
            CedulaInt (int): cedula sin guiones.
            Peso (float): peso validado.
            TipoSangre (str): tipo de sangre seleccionado.

        Returns:
            list[str]: lista de mensajes en orden.
        """
        Mensajes = []

        # 1. Mayoria de edad por mes y anio.
        if Val.EsMayorDeEdad(Dia, Mes, Anio):
            Mensajes.append("1. Dado su fecha de nacimiento usted ya "
                            "puede ser donador.")
        else:
            Mensajes.append("1. Dado su fecha de nacimiento usted aun "
                            "no puede ser donador.")

        # 2. Lugar segun provincia de la cedula.
        CedulaStr = Val.CedulaIntAStr(CedulaInt)
        Codigo = Val.CedulaACodigoProvincia(CedulaStr)
        Provincia = NombreProvincia(Codigo)
        Lugares = ObtenerLugaresPorCedula(CedulaInt)
        if Lugares:
            ListaLugares = ", ".join(Lugares)
            Mensajes.append(f"2. Dado que usted nacio en la provincia "
                            f"de: {Provincia}, usted podria donar en: "
                            f"{ListaLugares}.")
        else:
            Mensajes.append(f"2. Dado que usted nacio en la provincia "
                            f"de: {Provincia}, no hay lugares de "
                            "donacion registrados para esa provincia.")

        # 3. Validacion del peso (3 casos).
        Mensajes.append(f"3. {Val.ClasificarPeso(Peso)}")

        # 4. Compatibilidad sanguinea.
        Mensajes.append(f"4. {MensajeCompatibilidad(TipoSangre)}")

        # 5. Recomendacion del video si es A+ o A-.
        if TipoSangre in ("A+", "A-"):
            Mensajes.append(
                "5. Le recomendamos ver el video: "
                "'Particularidades de la sangre tipo A: Responde "
                "diferente al estres segun la ciencia'.")

        return Mensajes

    def _MostrarRetroalimentacion(self, Mensajes):
        """
        Despliega una ventana modal con los 5 mensajes generados tras
        la insercion exitosa.

        Args:
            Mensajes (list[str]): textos a mostrar, uno por bloque.
        """
        VentanaResumen = tk.Toplevel(self)
        VentanaResumen.title("Datos del donador registrado")
        VentanaResumen.geometry("620x400")
        VentanaResumen.configure(bg="#fafafa")
        VentanaResumen.transient(self)

        tk.Label(VentanaResumen,
                 text="Donador registrado exitosamente",
                 font=("Arial", 14, "bold"),
                 bg="#fafafa", fg="#080",
                 pady=8).pack(fill="x")

        AreaTexto = tk.Text(VentanaResumen, wrap="word", width=72,
                            height=16, font=("Arial", 10),
                            padx=12, pady=8)
        AreaTexto.pack(fill="both", expand=True, padx=12, pady=8)

        for Mensaje in Mensajes:
            AreaTexto.insert("end", Mensaje + "\n\n")
        AreaTexto.config(state="disabled")

        tk.Button(VentanaResumen, text="Cerrar",
                  command=VentanaResumen.destroy, width=12, pady=4,
                  cursor="hand2",
                  bg="#b00", fg="white",
                  font=("Arial", 11, "bold")).pack(pady=8)
