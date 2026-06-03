"""
Tarea Programada #2 - Donemos Sangre, demos vida...
Taller de Programacion - I Semestre 2026
Integrantes:
    - Cristhoper Jara Salazar
    - Diego Kim
Archivo: principal.py
Proposito:
    Punto de entrada de la aplicacion + TODA la interfaz grafica.
    Es uno de los 3 archivos del proyecto (junto con funciones.py
    y archivos.py).
    Contiene:
        - Constantes de estilos visuales (paleta + tipografias).
        - Helpers para construir banner, botones con hover, footer,
          tarjetas, splash y centrado.
        - Una clase por ventana Tkinter:
              VentanaPrincipal, VentanaInsertar, VentanaGenerar,
              VentanaActualizar, VentanaEliminar, VentanaLugarDonacion,
              VentanaReportes.
        - Funcion Main() que arranca la aplicacion.
    Cada menu tiene SU BOTON REGRESAR (incluida la ventana resumen
    tras insertar). El boton Salir de la ventana principal cierra la
    aplicacion guardando la base de datos.
    Convencion de codigo:
        - Variables, funciones y parametros en NombreCamello.
        - Sin uso de la palabra clave 'global'.

"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import funciones as F
import archivos as A
# SECCION 1: PALETA DE COLORES Y TIPOGRAFIAS

RojoPrincipal = "#B91C1C"
RojoHover = "#991B1B"
RojoOscuro = "#7F1D1D"
RojoSuave = "#FEE2E2"
Blanco = "#FFFFFF"
GrisFondo = "#F9FAFB"
GrisClaro = "#E5E7EB"
GrisMedio = "#9CA3AF"
GrisOscuro = "#374151"
GrisHover = "#6B7280"
GrisDeshabilitado = "#D1D5DB"
VerdeExito = "#15803D"
VerdeHover = "#166534"
AzulInfo = "#1E40AF"

TamTitulo = ("Segoe UI", 18, "bold")
TamSubtitulo = ("Segoe UI", 11, "italic")
TamSeccion = ("Segoe UI", 14, "bold")
TamBoton = ("Segoe UI", 11, "bold")
TamCampo = ("Segoe UI", 11)
TamEtiqueta = ("Segoe UI", 11)
TamFooter = ("Segoe UI", 9)
TamStatus = ("Segoe UI", 9)

# SECCION 2: HELPERS VISUALES

def AplicarTema(Raiz):
    """Tema ttk 'clam' con personalizacion de Combobox."""
    Estilo = ttk.Style(Raiz)
    Estilo.theme_use("clam")
    Estilo.configure("TCombobox",
                     fieldbackground=Blanco, background=Blanco,
                     foreground=GrisOscuro, bordercolor=GrisClaro,
                     lightcolor=GrisClaro, darkcolor=GrisClaro,
                     arrowcolor=RojoPrincipal, padding=6)
    Estilo.map("TCombobox",
               fieldbackground=[("readonly", Blanco)],
               foreground=[("readonly", GrisOscuro)])


def _AplicarHover(Boton, ColorNormal, ColorHover):
    """Vincula <Enter>/<Leave> para alternar color."""
    Boton.bind("<Enter>", lambda _E: Boton.config(bg=ColorHover))
    Boton.bind("<Leave>", lambda _E: Boton.config(bg=ColorNormal))

def CrearHeader(Padre, Titulo, Subtitulo=None):
    """Banner rojo con franja decorativa inferior."""
    Contenedor = tk.Frame(Padre, bg=RojoPrincipal)
    Contenedor.pack(fill="x")
    Banda = tk.Frame(Contenedor, bg=RojoPrincipal, pady=14)
    Banda.pack(fill="x")
    tk.Label(Banda, text=Titulo, font=TamTitulo,
             bg=RojoPrincipal, fg=Blanco).pack()
    if Subtitulo:
        tk.Label(Banda, text=Subtitulo, font=TamSubtitulo,
                 bg=RojoPrincipal, fg=Blanco).pack()
    tk.Frame(Contenedor, bg=RojoOscuro, height=3).pack(fill="x")
    tk.Frame(Contenedor, bg=Blanco, height=2).pack(fill="x")
    return Contenedor

def CrearBotonPrimario(Padre, Texto, Comando, Icono="", Ancho=32):
    """Boton rojo con texto blanco."""
    TextoCompleto = f"{Icono}  {Texto}" if Icono else Texto
    Btn = tk.Button(Padre, text=TextoCompleto, command=Comando,
                    font=TamBoton, bg=RojoPrincipal, fg=Blanco,
                    activebackground=RojoHover, activeforeground=Blanco,
                    relief="flat", bd=0, pady=8, width=Ancho,
                    cursor="hand2", highlightthickness=0)
    _AplicarHover(Btn, RojoPrincipal, RojoHover)
    return Btn

def CrearBotonSecundario(Padre, Texto, Comando, Icono="", Ancho=32):
    """Boton gris para acciones secundarias (Regresar, Cancelar)."""
    TextoCompleto = f"{Icono}  {Texto}" if Icono else Texto
    Btn = tk.Button(Padre, text=TextoCompleto, command=Comando,
                    font=TamBoton, bg=GrisMedio, fg=Blanco,
                    activebackground=GrisHover, activeforeground=Blanco,
                    relief="flat", bd=0, pady=8, width=Ancho,
                    cursor="hand2", highlightthickness=0)
    _AplicarHover(Btn, GrisMedio, GrisHover)
    return Btn

def CrearBotonExito(Padre, Texto, Comando, Icono="", Ancho=32):
    """Boton verde para confirmaciones positivas."""
    TextoCompleto = f"{Icono}  {Texto}" if Icono else Texto
    Btn = tk.Button(Padre, text=TextoCompleto, command=Comando,
                    font=TamBoton, bg=VerdeExito, fg=Blanco,
                    activebackground=VerdeHover, activeforeground=Blanco,
                    relief="flat", bd=0, pady=8, width=Ancho,
                    cursor="hand2", highlightthickness=0)
    _AplicarHover(Btn, VerdeExito, VerdeHover)
    return Btn

def CrearBotonMenu(Padre, Numero, Texto, Comando, Icono):
    """Boton de menu con icono, plano, ancho."""
    TextoCompleto = f"  {Icono}     {Numero}. {Texto}"
    Btn = tk.Button(Padre, text=TextoCompleto, command=Comando,
                    font=("Segoe UI", 12), bg=Blanco, fg=GrisOscuro,
                    activebackground=RojoSuave,
                    activeforeground=GrisOscuro, relief="flat", bd=0,
                    pady=12, padx=10, anchor="w", cursor="hand2",
                    highlightthickness=1,
                    highlightbackground=GrisClaro,
                    highlightcolor=RojoPrincipal)
    _AplicarHover(Btn, Blanco, RojoSuave)
    return Btn

def CrearSeparador(Padre):
    """Linea horizontal fina."""
    return tk.Frame(Padre, bg=GrisClaro, height=1)

def CrearStatusBar(Padre):
    """Barra de estado inferior con label dinamico."""
    Barra = tk.Frame(Padre, bg=GrisClaro, height=24)
    Barra.pack(side="bottom", fill="x")
    tk.Frame(Barra, bg=RojoPrincipal, height=2).pack(fill="x")
    Lbl = tk.Label(Barra, text="", bg=GrisClaro, fg=GrisOscuro,
                   font=TamStatus, anchor="w", padx=12, pady=4)
    Lbl.pack(fill="x")
    return Barra, Lbl

def CrearFooter(Padre, Texto=None):
    """Pie de pagina institucional."""
    Footer = tk.Frame(Padre, bg=GrisFondo, pady=8)
    Footer.pack(side="bottom", fill="x")
    TextoBase = "Banco Nacional de Sangre - Donar sangre, es donar vida"
    if Texto:
        TextoBase += f" - {Texto}"
    tk.Label(Footer, text=TextoBase, font=TamFooter,
             bg=GrisFondo, fg=GrisMedio).pack()
    return Footer


def EnvolverEnTarjeta(Padre, Padx=20, Pady=16):
    """Tarjeta blanca con borde gris claro."""
    Borde = tk.Frame(Padre, bg=GrisClaro)
    Tarjeta = tk.Frame(Borde, bg=Blanco, padx=Padx, pady=Pady)
    Tarjeta.pack(padx=1, pady=1, fill="both", expand=True)
    return Borde, Tarjeta


def MostrarSplash(Raiz, Duracion=1500):
    """Pantalla de bienvenida sin bordes."""
    Raiz.withdraw()
    Splash = tk.Toplevel(Raiz)
    Splash.overrideredirect(True)
    Splash.configure(bg=RojoPrincipal)
    Ancho, Alto = 460, 220
    Pantalla = Raiz.winfo_screenwidth()
    PantallaAlto = Raiz.winfo_screenheight()
    X = (Pantalla - Ancho) // 2
    Y = (PantallaAlto - Alto) // 2
    Splash.geometry(f"{Ancho}x{Alto}+{X}+{Y}")
    tk.Frame(Splash, bg=RojoPrincipal, height=20).pack(fill="x")
    tk.Label(Splash, text="♥",
             font=("Segoe UI", 48, "bold"),
             bg=RojoPrincipal, fg=Blanco).pack(pady=4)
    tk.Label(Splash, text="Banco Nacional de Sangre",
             font=("Segoe UI", 16, "bold"),
             bg=RojoPrincipal, fg=Blanco).pack()
    tk.Label(Splash, text="Sistema de gestion de donadores",
             font=("Segoe UI", 10),
             bg=RojoPrincipal, fg=Blanco).pack(pady=2)
    tk.Frame(Splash, bg=Blanco, height=2).pack(fill="x", pady=12)
    tk.Label(Splash, text="Cargando...",
             font=("Segoe UI", 9, "italic"),
             bg=RojoPrincipal, fg=Blanco).pack()

    def CerrarSplash():
        Splash.destroy()
        Raiz.deiconify()
    Raiz.after(Duracion, CerrarSplash)


def CentrarVentana(Ventana, Ancho, Alto):
    """Centra una ventana en pantalla."""
    Pantalla = Ventana.winfo_screenwidth()
    PantallaAlto = Ventana.winfo_screenheight()
    X = (Pantalla - Ancho) // 2
    Y = (PantallaAlto - Alto) // 2
    Ventana.geometry(f"{Ancho}x{Alto}+{X}+{Y}")

# SECCION 3: VENTANA PRINCIPA

class VentanaPrincipal:
    """Ventana raiz con los 7 botones del menu principal."""

    BotonesPermitidosSinBd = {1, 2, 5, 7}

    DefinicionesMenu = [
        (1, "Insertar donador",              "+",  "_AbrirInsertar"),
        (2, "Generar donadores",             "~",  "_AbrirGenerar"),
        (3, "Actualizar datos del donador",  ">",  "_AbrirActualizar"),
        (4, "Eliminar donador",              "X",  "_AbrirEliminar"),
        (5, "Insertar lugar de donacion",    "@",  "_AbrirInsertarLugar"),
        (6, "Reportes",                      "=",  "_AbrirReportes"),
        (7, "Salir",                         "<",  "_Salir"),
    ]

    def __init__(self, Raiz, BaseDeDatosCargada):
        self.Raiz = Raiz
        self.BotonesMenu = {}
        self.EtiquetaStatus = None
        self._ConfigurarVentana()
        self._ConstruirEncabezado()
        self._ConstruirArea()
        self._ConstruirPie()
        self._AplicarEstadoBotones()
        self._RefrescarStatus()
        self.Raiz.bind("<FocusIn>", self._AlRecibirFoco)
        if BaseDeDatosCargada:
            messagebox.showinfo(
                "Base de datos",
                "Base de datos cargada correctamente desde memoria "
                "secundaria.")

    def _ConfigurarVentana(self):
        self.Raiz.title(
            "Banco Nacional de Sangre - Sistema de Donadores")
        CentrarVentana(self.Raiz, 600, 680)
        self.Raiz.resizable(False, False)
        self.Raiz.configure(bg=GrisFondo)
        self.Raiz.protocol("WM_DELETE_WINDOW", self._Salir)

    def _ConstruirEncabezado(self):
        CrearHeader(self.Raiz,
                    Titulo="Banco Nacional de Sangre",
                    Subtitulo="Donar sangre es donar vida")

    def _ConstruirArea(self):
        Contenedor = tk.Frame(self.Raiz, bg=GrisFondo)
        Contenedor.pack(fill="both", expand=True, padx=30, pady=20)
        tk.Label(Contenedor, text="Menu principal",
                 font=TamSeccion, bg=GrisFondo,
                 fg=GrisOscuro, anchor="w").pack(fill="x", pady=(0, 8))
        CrearSeparador(Contenedor).pack(fill="x", pady=(0, 12))
        Borde, Tarjeta = EnvolverEnTarjeta(Contenedor,
                                           Padx=18, Pady=14)
        Borde.pack(fill="both", expand=True)
        for Numero, Texto, Icono, NombreCallback in (
                VentanaPrincipal.DefinicionesMenu):
            Comando = getattr(self, NombreCallback)
            Boton = CrearBotonMenu(Tarjeta, Numero, Texto, Comando, Icono)
            Boton.pack(fill="x", pady=4)
            self.BotonesMenu[Numero] = Boton

    def _ConstruirPie(self):
        _Barra, self.EtiquetaStatus = CrearStatusBar(self.Raiz)
        CrearFooter(self.Raiz)

    def _AplicarEstadoBotones(self):
        """Activa/desactiva botones segun haya o no BD."""
        HayDatos = F.HayBaseDeDatos()
        for Numero, Boton in self.BotonesMenu.items():
            if HayDatos or Numero in VentanaPrincipal.BotonesPermitidosSinBd:
                Boton.config(state="normal", fg=GrisOscuro)
            else:
                Boton.config(state="disabled", fg=GrisDeshabilitado)

    def _RefrescarStatus(self):
        """Status bar con cantidad de donadores."""
        if self.EtiquetaStatus is None:
            return
        Hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        Cantidad = len(F.Donadores)
        Activos = sum(1 for Fila in F.Donadores
                      if Fila[F.IdxEstado] == 1)
        if Cantidad == 0:
            Texto = f"  Base de datos vacia    |    {Hora}"
        else:
            Texto = (f"  {Cantidad} donadores registrados "
                     f"({Activos} activos)    |    {Hora}")
        self.EtiquetaStatus.config(text=Texto)

    def _AlRecibirFoco(self, _Evento):
        self._AplicarEstadoBotones()
        self._RefrescarStatus()

    def _AbrirInsertar(self):
        VentanaInsertar(self.Raiz)

    def _AbrirGenerar(self):
        VentanaGenerar(self.Raiz)

    def _AbrirActualizar(self):
        VentanaActualizar(self.Raiz)

    def _AbrirEliminar(self):
        VentanaEliminar(self.Raiz)

    def _AbrirInsertarLugar(self):
        VentanaLugarDonacion(self.Raiz)

    def _AbrirReportes(self):
        VentanaReportes(self.Raiz)

    def _Salir(self):
        """Mensaje 'Donar sangre, es donar vida' y cierre."""
        if F.HayBaseDeDatos():
            A.GuardarBaseDeDatos()
        messagebox.showinfo("Hasta pronto",
                            "Donar sangre, es donar vida")
        self.Raiz.destroy()

# SECCION 4: VENTANA INSERTAR DONADOR

class VentanaInsertar(tk.Toplevel):
    """Formulario de insercion con 5 mensajes de retroalimentacion."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Insertar donador")
        CentrarVentana(self, 620, 660)
        self.resizable(False, False)
        self.configure(bg=GrisFondo)
        self.VarCedula = tk.StringVar()
        self.VarNombre = tk.StringVar()
        self.VarFecha = tk.StringVar()
        self.VarTipoSangre = tk.StringVar()
        self.VarSexo = tk.BooleanVar(value=True)
        self.VarPeso = tk.StringVar()
        self.VarTelefono = tk.StringVar()
        self.VarCorreo = tk.StringVar()
        CrearHeader(self, Titulo="Registrar nuevo donador",
                    Subtitulo="Complete todos los campos")
        self._ConstruirFormulario()
        self._ConstruirBotones()
        CrearFooter(self)
        self.transient(Padre); self.grab_set()

    def _ConstruirFormulario(self):
        Contenedor = tk.Frame(self, bg=GrisFondo, padx=24, pady=14)
        Contenedor.pack(fill="both", expand=True)
        Borde, Tarjeta = EnvolverEnTarjeta(Contenedor)
        Borde.pack(fill="both", expand=True)
        Tarjeta.columnconfigure(1, weight=1)
        FilaActual = 0
        for Etiqueta, Variable in [
            ("Cedula (#-####-####):", self.VarCedula),
            ("Nombre completo:",      self.VarNombre),
            ("Fecha (DD/MM/AAAA):",   self.VarFecha),
        ]:
            self._FilaTexto(Tarjeta, FilaActual, Etiqueta, Variable)
            FilaActual += 1
        tk.Label(Tarjeta, text="Tipo de sangre:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").grid(row=FilaActual, column=0, sticky="w",
                                  pady=6, padx=(0, 12))
        ttk.Combobox(Tarjeta, textvariable=self.VarTipoSangre,
                     values=list(F.TiposDeSangre), state="readonly",
                     font=TamCampo, width=28).grid(
                         row=FilaActual, column=1, sticky="ew", pady=6)
        FilaActual += 1
        tk.Label(Tarjeta, text="Sexo:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").grid(row=FilaActual, column=0, sticky="w",
                                  pady=6)
        MarcoSexo = tk.Frame(Tarjeta, bg=Blanco)
        MarcoSexo.grid(row=FilaActual, column=1, sticky="w", pady=6)
        tk.Radiobutton(MarcoSexo, text="Masculino",
                       variable=self.VarSexo, value=True, bg=Blanco,
                       font=TamCampo, fg=GrisOscuro,
                       activebackground=Blanco,
                       selectcolor=Blanco).pack(side="left", padx=(0, 16))
        tk.Radiobutton(MarcoSexo, text="Femenino",
                       variable=self.VarSexo, value=False, bg=Blanco,
                       font=TamCampo, fg=GrisOscuro,
                       activebackground=Blanco,
                       selectcolor=Blanco).pack(side="left")
        FilaActual += 1
        for Etiqueta, Variable in [
            ("Peso (kg):",            self.VarPeso),
            ("Telefono (####-####):", self.VarTelefono),
            ("Correo:",               self.VarCorreo),
        ]:
            self._FilaTexto(Tarjeta, FilaActual, Etiqueta, Variable)
            FilaActual += 1

    def _FilaTexto(self, Padre, Fila, Etiqueta, Variable):
        tk.Label(Padre, text=Etiqueta, bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").grid(row=Fila, column=0, sticky="w",
                                  pady=6, padx=(0, 12))
        tk.Entry(Padre, textvariable=Variable, font=TamCampo, width=28,
                 fg=GrisOscuro, bg=Blanco, relief="solid", bd=1,
                 highlightthickness=1,
                 highlightbackground=GrisClaro,
                 highlightcolor=RojoPrincipal).grid(
                     row=Fila, column=1, sticky="ew", pady=6, ipady=3)

    def _ConstruirBotones(self):
        Marco = tk.Frame(self, bg=GrisFondo, pady=14)
        Marco.pack(fill="x", padx=24)
        CrearBotonPrimario(Marco, "Registrar", self._Registrar,
                           Icono="OK", Ancho=14).pack(side="left",
                                                      padx=4, expand=True)
        CrearBotonSecundario(Marco, "Limpiar", self._Limpiar,
                             Icono="C", Ancho=14).pack(side="left",
                                                       padx=4, expand=True)
        CrearBotonSecundario(Marco, "Regresar", self.destroy,
                             Icono="<", Ancho=14).pack(side="left",
                                                       padx=4, expand=True)

    def _Registrar(self):
        Errores = []
        OkCedula, MsgCedula = F.ValidarCedula(self.VarCedula.get())
        if not OkCedula:
            Errores.append(f"Cedula: {MsgCedula}")
        TextoNombre = self.VarNombre.get().strip()
        Partes = TextoNombre.split()
        if len(Partes) != 3:
            Errores.append("Nombre completo: debe contener el nombre, "
                           "el primer apellido y el segundo apellido "
                           "(3 palabras separadas por espacio).")
        else:
            for P in Partes:
                OkP, MsgP = F.ValidarNombre(P)
                if not OkP:
                    Errores.append(f"Nombre: {MsgP}"); break
        OkFecha, MsgFecha = F.ValidarFecha(self.VarFecha.get())
        if not OkFecha:
            Errores.append(f"Fecha: {MsgFecha}")
        TipoSangre = self.VarTipoSangre.get()
        if not TipoSangre:
            Errores.append("Tipo de sangre: debe seleccionar uno.")
        OkPeso, MsgPeso, ValorPeso = F.ValidarPeso(self.VarPeso.get())
        if not OkPeso:
            Errores.append(f"Peso: {MsgPeso}")
        OkTel, MsgTel = F.ValidarTelefono(self.VarTelefono.get())
        if not OkTel:
            Errores.append(f"Telefono: {MsgTel}")
        OkCor, MsgCor = F.ValidarCorreo(self.VarCorreo.get())
        if not OkCor:
            Errores.append(f"Correo: {MsgCor}")
        if Errores:
            messagebox.showerror("Errores en el formulario",
                                 "\n\n".join(Errores), parent=self)
            return
        CedulaInt = F.CedulaStrAInt(self.VarCedula.get())
        if F.ExisteCedula(CedulaInt):
            messagebox.showerror(
                "Cedula duplicada",
                f"La cedula {self.VarCedula.get().strip()} ya esta "
                "registrada en la base de datos.", parent=self)
            return
        Dia, Mes, Anio = (int(P) for P in
                          self.VarFecha.get().strip().split("/"))
        F.Donadores.append([
            Partes, CedulaInt, F.TipoSangreAIndice(TipoSangre),
            self.VarSexo.get(), (Dia, Mes, Anio), ValorPeso,
            self.VarCorreo.get().strip(),
            self.VarTelefono.get().strip(),
            1, 0,
        ])
        A.GuardarBaseDeDatos()
        Mensajes = self._ConstruirMensajesRetroalimentacion(
            Dia, Mes, Anio, CedulaInt, ValorPeso, TipoSangre)
        self._MostrarRetroalimentacion(Mensajes)
        self._Limpiar()

    def _Limpiar(self):
        self.VarCedula.set(""); self.VarNombre.set("")
        self.VarFecha.set(""); self.VarTipoSangre.set("")
        self.VarSexo.set(True); self.VarPeso.set("")
        self.VarTelefono.set(""); self.VarCorreo.set("")

    def _ConstruirMensajesRetroalimentacion(self, Dia, Mes, Anio,
                                            CedulaInt, Peso, TipoSangre):
        Mensajes = []
        if F.EsMayorDeEdad(Dia, Mes, Anio):
            Mensajes.append("1. Dado su fecha de nacimiento usted ya "
                            "puede ser donador.")
        else:
            Mensajes.append("1. Dado su fecha de nacimiento usted aun "
                            "no puede ser donador.")
        CedulaStr = F.CedulaIntAStr(CedulaInt)
        Codigo = F.CedulaACodigoProvincia(CedulaStr)
        Provincia = F.NombreProvincia(Codigo)
        Lugares = F.ObtenerLugaresPorCedula(CedulaInt)
        if Lugares:
            Mensajes.append(f"2. Dado que usted nacio en la provincia "
                            f"de: {Provincia}, usted podria donar en: "
                            f"{', '.join(Lugares)}.")
        else:
            Mensajes.append(f"2. Dado que usted nacio en la provincia "
                            f"de: {Provincia}, no hay lugares de "
                            "donacion registrados para esa provincia.")
        Mensajes.append(f"3. {F.ClasificarPeso(Peso)}")
        Mensajes.append(f"4. {F.MensajeCompatibilidad(TipoSangre)}")
        if TipoSangre in ("A+", "A-"):
            Mensajes.append("5. Le recomendamos ver el video: "
                            "'Particularidades de la sangre tipo A: "
                            "Responde diferente al estres segun la "
                            "ciencia'.")
        return Mensajes

    def _MostrarRetroalimentacion(self, Mensajes):
        """Ventana resumen con boton Regresar (fix #4)."""
        Resumen = tk.Toplevel(self)
        Resumen.title("Donador registrado")
        CentrarVentana(Resumen, 680, 460)
        Resumen.configure(bg=GrisFondo)
        Resumen.transient(self)
        CrearHeader(Resumen, Titulo="Donador registrado exitosamente",
                    Subtitulo="Informacion para el donador")
        Cont = tk.Frame(Resumen, bg=GrisFondo, padx=20, pady=14)
        Cont.pack(fill="both", expand=True)
        Borde, Tarjeta = EnvolverEnTarjeta(Cont, Padx=14, Pady=10)
        Borde.pack(fill="both", expand=True)
        Area = tk.Text(Tarjeta, wrap="word", width=70, height=14,
                       font=TamCampo, bg=Blanco, fg=GrisOscuro,
                       relief="flat", bd=0, padx=8, pady=4)
        Area.pack(fill="both", expand=True)
        for M in Mensajes:
            Area.insert("end", M + "\n\n")
        Area.config(state="disabled")
        Marco = tk.Frame(Resumen, bg=GrisFondo, pady=10)
        Marco.pack(fill="x", padx=20)
        # FIX #4: boton "Regresar" (antes era "Cerrar").
        CrearBotonSecundario(Marco, "Regresar", Resumen.destroy,
                             Icono="<", Ancho=14).pack()
        CrearFooter(Resumen)

# SECCION 5: VENTANA GENERAR DONADORES

class VentanaGenerar(tk.Toplevel):
    """Genera donadores aleatorios respetando todas las restricciones."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Generar donadores")
        CentrarVentana(self, 540, 380)
        self.resizable(False, False)
        self.configure(bg=GrisFondo)
        self.VarCantidad = tk.StringVar()
        CrearHeader(self, Titulo="Generar donadores aleatorios",
                    Subtitulo="Poblar la BD rapidamente")
        self._ConstruirFormulario()
        CrearFooter(self)
        self.transient(Padre); self.grab_set()

    def _ConstruirFormulario(self):
        Cont = tk.Frame(self, bg=GrisFondo, padx=24, pady=18)
        Cont.pack(fill="both", expand=True)
        Borde, Tarjeta = EnvolverEnTarjeta(Cont)
        Borde.pack(fill="both", expand=True)
        tk.Label(Tarjeta, text="Indique cuantos donadores desea crear.",
                 bg=Blanco, font=TamCampo,
                 fg=GrisOscuro).pack(pady=(4, 4))
        tk.Label(Tarjeta,
                 text="Cada donador tendra datos aleatorios validos.\n"
                      "Exactamente el 20% quedaran inactivos con\n"
                      "una justificacion aleatoria del 1 al 7.",
                 bg=Blanco, font=("Segoe UI", 9),
                 fg=GrisMedio, justify="center").pack(pady=(0, 14))
        MarcoInput = tk.Frame(Tarjeta, bg=Blanco)
        MarcoInput.pack(pady=4)
        tk.Label(MarcoInput, text="Cantidad:",
                 bg=Blanco, font=TamEtiqueta,
                 fg=GrisOscuro).pack(side="left", padx=(0, 8))
        tk.Entry(MarcoInput, textvariable=self.VarCantidad, width=10,
                 font=TamCampo, fg=GrisOscuro, bg=Blanco,
                 relief="solid", bd=1, justify="center",
                 highlightthickness=1,
                 highlightbackground=GrisClaro,
                 highlightcolor=RojoPrincipal).pack(side="left", ipady=3)
        MarcoBtn = tk.Frame(Tarjeta, bg=Blanco, pady=18)
        MarcoBtn.pack()
        CrearBotonPrimario(MarcoBtn, "Generar", self._Generar,
                           Icono="~", Ancho=14).pack(side="left", padx=6)
        CrearBotonSecundario(MarcoBtn, "Regresar", self.destroy,
                             Icono="<", Ancho=14).pack(side="left",
                                                       padx=6)

    def _Generar(self):
        Texto = self.VarCantidad.get().strip()
        if not Texto:
            messagebox.showerror("Error",
                                 "Debe indicar una cantidad.",
                                 parent=self)
            return
        try:
            Cantidad = int(Texto)
        except ValueError:
            messagebox.showerror("Error",
                                 "La cantidad debe ser un entero.",
                                 parent=self)
            return
        if Cantidad <= 0:
            messagebox.showerror("Error",
                                 "La cantidad debe ser mayor a 0.",
                                 parent=self)
            return
        Agregados = F.GenerarDonadoresAleatorios(Cantidad)
        Inactivos = int(Cantidad * 0.20)
        A.GuardarBaseDeDatos()
        messagebox.showinfo(
            "Generacion completada",
            f"Se generaron {Agregados} donadores.\n"
            f"Activos: {Agregados - Inactivos}\n"
            f"Inactivos: {Inactivos} (20% exacto, justificacion 1-7).",
            parent=self)
        self.VarCantidad.set("")

# SECCION 6: VENTANA INSERTAR LUGAR DE DONACION

class VentanaLugarDonacion(tk.Toplevel):
    """Combobox provincia + Text + verificacion de duplicado."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Insertar lugar de donacion")
        CentrarVentana(self, 580, 460)
        self.resizable(False, False)
        self.configure(bg=GrisFondo)
        self.VarProvincia = tk.StringVar()
        CrearHeader(self, Titulo="Insertar lugar de donacion",
                    Subtitulo="Agrega un nuevo recinto de recoleccion")
        self._ConstruirFormulario()
        CrearFooter(self)
        self.transient(Padre); self.grab_set()

    def _ConstruirFormulario(self):
        Cont = tk.Frame(self, bg=GrisFondo, padx=24, pady=18)
        Cont.pack(fill="both", expand=True)
        Borde, Tarjeta = EnvolverEnTarjeta(Cont)
        Borde.pack(fill="both", expand=True)
        Opciones = [f"{C} - {N}" for C, N in sorted(F.Provincias.items())]
        tk.Label(Tarjeta, text="Provincia:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").pack(fill="x", pady=(0, 4))
        ttk.Combobox(Tarjeta, textvariable=self.VarProvincia,
                     values=Opciones, state="readonly",
                     font=TamCampo).pack(fill="x", pady=(0, 12))
        tk.Label(Tarjeta, text="Nuevo lugar de donacion:",
                 bg=Blanco, font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").pack(fill="x", pady=(0, 4))
        self.AreaTexto = tk.Text(Tarjeta, height=5, font=TamCampo,
                                 wrap="word", bg=Blanco, fg=GrisOscuro,
                                 relief="solid", bd=1,
                                 highlightthickness=1,
                                 highlightbackground=GrisClaro,
                                 highlightcolor=RojoPrincipal)
        self.AreaTexto.pack(fill="x")
        MarcoBtn = tk.Frame(Tarjeta, bg=Blanco, pady=14)
        MarcoBtn.pack()
        CrearBotonPrimario(MarcoBtn, "Insertar", self._Insertar,
                           Icono="+", Ancho=14).pack(side="left", padx=6)
        # FIX #4: boton "Regresar" (antes era "Salir").
        CrearBotonSecundario(MarcoBtn, "Regresar", self.destroy,
                             Icono="<", Ancho=14).pack(side="left",
                                                       padx=6)

    def _Insertar(self):
        Seleccion = self.VarProvincia.get().strip()
        NuevoLugar = self.AreaTexto.get("1.0", "end").strip()
        if not Seleccion:
            messagebox.showerror("Error",
                                 "Debe seleccionar una provincia.",
                                 parent=self)
            return
        if not NuevoLugar:
            messagebox.showerror("Error",
                                 "Debe indicar el nombre del lugar.",
                                 parent=self)
            return
        CodigoProvincia = int(Seleccion.split(" - ")[0])
        Lista = F.LugaresDonacion.setdefault(CodigoProvincia, [])
        if NuevoLugar.lower() in [L.lower() for L in Lista]:
            messagebox.showwarning(
                "Lugar duplicado",
                f"'{NuevoLugar}' ya esta registrado en "
                f"{F.Provincias[CodigoProvincia]}.", parent=self)
            return
        Lista.append(NuevoLugar)
        A.GuardarBaseDeDatos()
        messagebox.showinfo(
            "Lugar agregado",
            f"'{NuevoLugar}' agregado a "
            f"{F.Provincias[CodigoProvincia]}.", parent=self)
        self.AreaTexto.delete("1.0", "end")

# SECCION 7: VENTANA ACTUALIZAR DONADOR

class VentanaActualizar(tk.Toplevel):
    """Busca por cedula y permite modificar (cedula readonly)."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Actualizar donador")
        CentrarVentana(self, 620, 720)
        self.resizable(False, False)
        self.configure(bg=GrisFondo)
        self.IndiceDonadorActual = -1
        self.VarCedulaBusqueda = tk.StringVar()
        self.MarcoFormulario = None
        CrearHeader(self, Titulo="Actualizar donador",
                    Subtitulo="Modifique los datos del registro existente")
        self._ConstruirBuscador()
        CrearFooter(self)
        self.transient(Padre); self.grab_set()

    def _ConstruirBuscador(self):
        Cont = tk.Frame(self, bg=GrisFondo, padx=24, pady=14)
        Cont.pack(fill="x")
        Borde, Tarjeta = EnvolverEnTarjeta(Cont)
        Borde.pack(fill="x")
        Sub = tk.Frame(Tarjeta, bg=Blanco)
        Sub.pack(pady=4)
        tk.Label(Sub, text="Cedula:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro).pack(side="left",
                                                       padx=(0, 8))
        tk.Entry(Sub, textvariable=self.VarCedulaBusqueda,
                 width=16, font=TamCampo, fg=GrisOscuro, bg=Blanco,
                 relief="solid", bd=1, highlightthickness=1,
                 highlightbackground=GrisClaro,
                 highlightcolor=RojoPrincipal).pack(side="left",
                                                    ipady=3, padx=(0, 8))
        CrearBotonPrimario(Sub, "Buscar", self._Buscar,
                           Icono="?", Ancho=10).pack(side="left", padx=4)
        CrearBotonSecundario(Sub, "Regresar", self.destroy,
                             Icono="<", Ancho=10).pack(side="left",
                                                       padx=4)

    def _Buscar(self):
        Texto = self.VarCedulaBusqueda.get().strip()
        Ok, Msg = F.ValidarCedula(Texto)
        if not Ok:
            messagebox.showerror("Cedula invalida", Msg, parent=self)
            return
        CedulaInt = F.CedulaStrAInt(Texto)
        Indice = F.BuscarDonadorPorCedula(CedulaInt)
        if Indice == -1:
            messagebox.showinfo(
                "Cedula no registrada",
                f"La persona con el numero de cedula: {Texto} no "
                "esta registrado en la base de datos del Banco de "
                "Sangre aun.", parent=self)
            return
        self.IndiceDonadorActual = Indice
        self._ConstruirFormularioEdicion(Indice)

    def _ConstruirFormularioEdicion(self, IndiceDonador):
        if self.MarcoFormulario is not None:
            self.MarcoFormulario.destroy()
        Fila = F.Donadores[IndiceDonador]
        Cont = tk.Frame(self, bg=GrisFondo, padx=24, pady=8)
        Cont.pack(fill="both", expand=True)
        self.MarcoFormulario = Cont
        Borde, Tarjeta = EnvolverEnTarjeta(Cont)
        Borde.pack(fill="both", expand=True)
        Tarjeta.columnconfigure(1, weight=1)
        self.VarNombre = tk.StringVar(value=" ".join(Fila[F.IdxNombre]))
        D, M, Aa = Fila[F.IdxFechaNac]
        self.VarFecha = tk.StringVar(value=f"{D:02d}/{M:02d}/{Aa:04d}")
        self.VarTipoSangre = tk.StringVar(
            value=F.IndiceATipoSangre(Fila[F.IdxTipoSangre]))
        self.VarSexo = tk.BooleanVar(value=Fila[F.IdxSexo])
        self.VarPeso = tk.StringVar(value=str(Fila[F.IdxPeso]))
        self.VarTelefono = tk.StringVar(value=Fila[F.IdxTelefono])
        self.VarCorreo = tk.StringVar(value=Fila[F.IdxCorreo])
        FilaIdx = 0
        tk.Label(Tarjeta, text="Cedula:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").grid(row=FilaIdx, column=0, sticky="w",
                                  pady=6, padx=(0, 12))
        tk.Entry(Tarjeta,
                 textvariable=tk.StringVar(
                     value=F.CedulaIntAStr(Fila[F.IdxCedula])),
                 width=28, font=TamCampo, state="readonly",
                 bd=1, relief="solid",
                 readonlybackground=GrisClaro).grid(
                     row=FilaIdx, column=1, sticky="ew",
                     pady=6, ipady=3)
        FilaIdx += 1
        for Etiqueta, Variable in [
            ("Nombre completo:", self.VarNombre),
            ("Fecha (DD/MM/AAAA):", self.VarFecha),
        ]:
            self._FilaTexto(Tarjeta, FilaIdx, Etiqueta, Variable)
            FilaIdx += 1
        tk.Label(Tarjeta, text="Tipo de sangre:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").grid(row=FilaIdx, column=0, sticky="w",
                                  pady=6)
        ttk.Combobox(Tarjeta, textvariable=self.VarTipoSangre,
                     values=list(F.TiposDeSangre), state="readonly",
                     font=TamCampo, width=28).grid(
                         row=FilaIdx, column=1, sticky="ew", pady=6)
        FilaIdx += 1
        tk.Label(Tarjeta, text="Sexo:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").grid(row=FilaIdx, column=0, sticky="w",
                                  pady=6)
        MarcoSexo = tk.Frame(Tarjeta, bg=Blanco)
        MarcoSexo.grid(row=FilaIdx, column=1, sticky="w", pady=6)
        tk.Radiobutton(MarcoSexo, text="Masculino",
                       variable=self.VarSexo, value=True, bg=Blanco,
                       font=TamCampo, fg=GrisOscuro,
                       activebackground=Blanco,
                       selectcolor=Blanco).pack(side="left",
                                                padx=(0, 16))
        tk.Radiobutton(MarcoSexo, text="Femenino",
                       variable=self.VarSexo, value=False, bg=Blanco,
                       font=TamCampo, fg=GrisOscuro,
                       activebackground=Blanco,
                       selectcolor=Blanco).pack(side="left")
        FilaIdx += 1
        for Etiqueta, Variable in [
            ("Peso (kg):", self.VarPeso),
            ("Telefono (####-####):", self.VarTelefono),
            ("Correo:", self.VarCorreo),
        ]:
            self._FilaTexto(Tarjeta, FilaIdx, Etiqueta, Variable)
            FilaIdx += 1
        Marco = tk.Frame(Tarjeta, bg=Blanco, pady=14)
        Marco.grid(row=FilaIdx, column=0, columnspan=2)
        CrearBotonExito(Marco, "Confirmar",
                        self._ConfirmarActualizacion, Icono="OK",
                        Ancho=14).pack(side="left", padx=6)
        CrearBotonSecundario(Marco, "Rechazar",
                             self._RechazarActualizacion, Icono="X",
                             Ancho=14).pack(side="left", padx=6)

    def _FilaTexto(self, Padre, Fila, Etiqueta, Variable):
        tk.Label(Padre, text=Etiqueta, bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro,
                 anchor="w").grid(row=Fila, column=0, sticky="w",
                                  pady=6, padx=(0, 12))
        tk.Entry(Padre, textvariable=Variable, width=28,
                 font=TamCampo, fg=GrisOscuro, bg=Blanco,
                 relief="solid", bd=1, highlightthickness=1,
                 highlightbackground=GrisClaro,
                 highlightcolor=RojoPrincipal).grid(
                     row=Fila, column=1, sticky="ew",
                     pady=6, ipady=3)

    def _ConfirmarActualizacion(self):
        Errores = []
        Partes = self.VarNombre.get().strip().split()
        if len(Partes) != 3:
            Errores.append("Nombre: 3 palabras (nombre + 2 apellidos).")
        OkF, MsgF = F.ValidarFecha(self.VarFecha.get())
        if not OkF:
            Errores.append(f"Fecha: {MsgF}")
        if not self.VarTipoSangre.get():
            Errores.append("Tipo de sangre: seleccione uno.")
        OkP, MsgP, ValorPeso = F.ValidarPeso(self.VarPeso.get())
        if not OkP:
            Errores.append(f"Peso: {MsgP}")
        OkT, MsgT = F.ValidarTelefono(self.VarTelefono.get())
        if not OkT:
            Errores.append(f"Telefono: {MsgT}")
        OkC, MsgC = F.ValidarCorreo(self.VarCorreo.get())
        if not OkC:
            Errores.append(f"Correo: {MsgC}")
        if Errores:
            messagebox.showerror("Errores",
                                 "\n\n".join(Errores), parent=self)
            return
        FilaActual = F.Donadores[self.IndiceDonadorActual]
        D, M, Aa = (int(P) for P in
                    self.VarFecha.get().strip().split("/"))
        F.Donadores[self.IndiceDonadorActual] = [
            Partes, FilaActual[F.IdxCedula],
            F.TipoSangreAIndice(self.VarTipoSangre.get()),
            self.VarSexo.get(), (D, M, Aa), ValorPeso,
            self.VarCorreo.get().strip(),
            self.VarTelefono.get().strip(),
            FilaActual[F.IdxEstado],
            FilaActual[F.IdxJustificacion],
        ]
        A.GuardarBaseDeDatos()
        messagebox.showinfo("Exito",
                            "Datos actualizados correctamente.",
                            parent=self)
        self.destroy()

    def _RechazarActualizacion(self):
        messagebox.showinfo("Sin cambios",
                            "Datos No actualizados.", parent=self)

# SECCION 8: VENTANA ELIMINAR DONADOR

class VentanaEliminar(tk.Toplevel):
    """Busca por cedula, Combobox de justificaciones de Gemini."""

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Eliminar donador")
        CentrarVentana(self, 680, 420)
        self.resizable(False, False)
        self.configure(bg=GrisFondo)
        self.IndiceDonadorActual = -1
        self.VarCedulaBusqueda = tk.StringVar()
        self.VarJustificacion = tk.StringVar()
        self.MarcoJustif = None
        CrearHeader(self, Titulo="Eliminar donador",
                    Subtitulo="Desactiva un donador con justificacion")
        self._ConstruirBuscador()
        CrearFooter(self)
        self.transient(Padre); self.grab_set()

    def _ConstruirBuscador(self):
        Cont = tk.Frame(self, bg=GrisFondo, padx=24, pady=14)
        Cont.pack(fill="x")
        Borde, Tarjeta = EnvolverEnTarjeta(Cont)
        Borde.pack(fill="x")
        Sub = tk.Frame(Tarjeta, bg=Blanco)
        Sub.pack(pady=4)
        tk.Label(Sub, text="Cedula:", bg=Blanco,
                 font=TamEtiqueta, fg=GrisOscuro).pack(side="left",
                                                       padx=(0, 8))
        tk.Entry(Sub, textvariable=self.VarCedulaBusqueda, width=16,
                 font=TamCampo, fg=GrisOscuro, bg=Blanco,
                 relief="solid", bd=1, highlightthickness=1,
                 highlightbackground=GrisClaro,
                 highlightcolor=RojoPrincipal).pack(side="left",
                                                    ipady=3, padx=(0, 8))
        CrearBotonPrimario(Sub, "Buscar", self._Buscar,
                           Icono="?", Ancho=10).pack(side="left",
                                                     padx=4)
        CrearBotonSecundario(Sub, "Regresar", self.destroy,
                             Icono="<", Ancho=10).pack(side="left",
                                                       padx=4)

    def _Buscar(self):
        Texto = self.VarCedulaBusqueda.get().strip()
        Ok, Msg = F.ValidarCedula(Texto)
        if not Ok:
            messagebox.showerror("Cedula invalida", Msg, parent=self)
            return
        CedulaInt = F.CedulaStrAInt(Texto)
        Indice = F.BuscarDonadorPorCedula(CedulaInt)
        if Indice == -1:
            messagebox.showinfo(
                "Cedula no registrada",
                f"La persona con el numero de cedula: {Texto} no "
                "esta registrado en la base de datos del Banco de "
                "Sangre aun.", parent=self)
            return
        if F.Donadores[Indice][F.IdxEstado] == 0:
            messagebox.showinfo(
                "Donador inactivo",
                f"La persona con cedula {Texto} ya esta marcada como "
                "NO activa.", parent=self)
            return
        self.IndiceDonadorActual = Indice
        self._ConstruirSeleccionJustificacion(Indice)

    def _ConstruirSeleccionJustificacion(self, IndiceDonador):
        if self.MarcoJustif is not None:
            self.MarcoJustif.destroy()
        Cont = tk.Frame(self, bg=GrisFondo, padx=24, pady=8)
        Cont.pack(fill="both", expand=True)
        self.MarcoJustif = Cont
        Borde, Tarjeta = EnvolverEnTarjeta(Cont)
        Borde.pack(fill="both", expand=True)
        Opciones = [f"{Codigo} - {Texto[:60]}..."
                    for Codigo, Texto in
                    sorted(F.Justificaciones.items())
                    if Codigo > 0]
        tk.Label(Tarjeta,
                 text="Seleccione la justificacion del rechazo:",
                 bg=Blanco, font=TamEtiqueta,
                 fg=GrisOscuro, anchor="w").pack(fill="x", pady=(0, 4))
        ttk.Combobox(Tarjeta, textvariable=self.VarJustificacion,
                     values=Opciones, state="readonly",
                     font=TamCampo).pack(fill="x")
        Marco = tk.Frame(Tarjeta, bg=Blanco, pady=14)
        Marco.pack()
        CrearBotonPrimario(Marco, "Confirmar",
                           self._ConfirmarEliminacion, Icono="OK",
                           Ancho=14).pack(side="left", padx=6)
        CrearBotonSecundario(Marco, "Cancelar",
                             self._RechazarEliminacion, Icono="X",
                             Ancho=14).pack(side="left", padx=6)

    def _ConfirmarEliminacion(self):
        Seleccion = self.VarJustificacion.get().strip()
        if not Seleccion:
            messagebox.showerror("Error",
                                 "Debe seleccionar una justificacion.",
                                 parent=self)
            return
        CodigoJustif = int(Seleccion.split(" - ")[0])
        Fila = F.Donadores[self.IndiceDonadorActual]
        Fila[F.IdxEstado] = 0
        Fila[F.IdxJustificacion] = CodigoJustif
        A.GuardarBaseDeDatos()
        messagebox.showinfo("Donador eliminado",
                            "Donador eliminado satisfactoriamente.",
                            parent=self)
        self.destroy()

    def _RechazarEliminacion(self):
        messagebox.showinfo("Cancelado",
                            "Donador NO eliminado.", parent=self)

# SECCION 9: VENTANA DE REPORTES

class VentanaReportes(tk.Toplevel):
    """9 botones de reporte + boton Regresar."""

    Definiciones = [
        "1. Donantes por provincia",
        "2. Por rango de edad",
        "3. Por tipo de sangre y provincia",
        "4. Lista completa",
        "5. Mujeres O- menores de 45",
        "6. A quien puede donar",
        "7. De quien puede recibir",
        "8. Donantes NO activos",
        "9. Lugares de donacion",
    ]

    def __init__(self, Padre):
        super().__init__(Padre)
        self.title("Reportes")
        CentrarVentana(self, 620, 720)
        self.resizable(False, False)
        self.configure(bg=GrisFondo)
        CrearHeader(self, Titulo="Reportes",
                    Subtitulo="Genere reportes HTML5 con un click")
        self._ConstruirBotones()
        CrearFooter(self)
        self.transient(Padre); self.grab_set()

    def _ConstruirBotones(self):
        Cont = tk.Frame(self, bg=GrisFondo, padx=24, pady=14)
        Cont.pack(fill="both", expand=True)
        Borde, Tarjeta = EnvolverEnTarjeta(Cont)
        Borde.pack(fill="both", expand=True)
        Callbacks = [
            self._ReportePorProvincia, self._ReportePorEdad,
            self._ReportePorTipoYProvincia, self._ReporteCompleto,
            self._ReporteMujeresONegativo, self._ReporteAQuienDona,
            self._ReporteDeQuienRecibe, self._ReporteNoActivos,
            self._ReporteLugares,
        ]
        for Texto, Comando in zip(VentanaReportes.Definiciones,
                                  Callbacks):
            Numero = int(Texto.split(".")[0])
            TextoLimpio = Texto.split(". ", 1)[1]
            CrearBotonMenu(Tarjeta, Numero, TextoLimpio, Comando,
                           "=").pack(fill="x", pady=3)
        Marco = tk.Frame(Tarjeta, bg=Blanco, pady=14)
        Marco.pack()
        CrearBotonSecundario(Marco, "Regresar", self.destroy,
                             Icono="<", Ancho=18).pack()

    def _MostrarResultado(self, Ok, NombreReporte):
        if Ok:
            messagebox.showinfo(NombreReporte,
                                "Reporte creado satisfactoriamente.",
                                parent=self)
        else:
            messagebox.showerror(NombreReporte,
                                 "Reporte no creado.", parent=self)

    def _AbrirSubVentanaProvincia(self, Titulo, GeneradorFn):
        Sub = tk.Toplevel(self)
        Sub.title(Titulo)
        CentrarVentana(Sub, 460, 240)
        Sub.configure(bg=GrisFondo)
        Sub.transient(self); Sub.grab_set()
        CrearHeader(Sub, Titulo=Titulo,
                    Subtitulo="Seleccione la provincia")
        VarProv = tk.StringVar()
        Opciones = [f"{C} - {N}" for C, N in sorted(F.Provincias.items())]
        Cont = tk.Frame(Sub, bg=GrisFondo, padx=24, pady=14)
        Cont.pack(fill="both", expand=True)
        tk.Label(Cont, text="Provincia:", bg=GrisFondo,
                 font=TamEtiqueta, fg=GrisOscuro).pack(pady=4)
        ttk.Combobox(Cont, textvariable=VarProv, values=Opciones,
                     state="readonly", font=TamCampo,
                     width=30).pack()

        def Generar():
            if not VarProv.get():
                messagebox.showerror("Error",
                                     "Seleccione una provincia.",
                                     parent=Sub)
                return
            Cod = int(VarProv.get().split(" - ")[0])
            self._MostrarResultado(GeneradorFn(Cod), Titulo)
            Sub.destroy()

        MarcoBtn = tk.Frame(Cont, bg=GrisFondo, pady=14)
        MarcoBtn.pack()
        CrearBotonPrimario(MarcoBtn, "Generar reporte", Generar,
                           Icono=">", Ancho=16).pack(side="left",
                                                     padx=4)
        CrearBotonSecundario(MarcoBtn, "Regresar", Sub.destroy,
                             Icono="<", Ancho=14).pack(side="left",
                                                       padx=4)

    def _AbrirSubVentanaTipoSangre(self, Titulo, GeneradorFn):
        Sub = tk.Toplevel(self)
        Sub.title(Titulo)
        CentrarVentana(Sub, 460, 240)
        Sub.configure(bg=GrisFondo)
        Sub.transient(self); Sub.grab_set()
        CrearHeader(Sub, Titulo=Titulo,
                    Subtitulo="Seleccione el tipo de sangre")
        VarTipo = tk.StringVar()
        Cont = tk.Frame(Sub, bg=GrisFondo, padx=24, pady=14)
        Cont.pack(fill="both", expand=True)
        tk.Label(Cont, text="Tipo de sangre:", bg=GrisFondo,
                 font=TamEtiqueta, fg=GrisOscuro).pack(pady=4)
        ttk.Combobox(Cont, textvariable=VarTipo,
                     values=list(F.TiposDeSangre), state="readonly",
                     font=TamCampo, width=30).pack()

        def Generar():
            if not VarTipo.get():
                messagebox.showerror("Error",
                                     "Seleccione un tipo de sangre.",
                                     parent=Sub)
                return
            self._MostrarResultado(GeneradorFn(VarTipo.get()), Titulo)
            Sub.destroy()

        MarcoBtn = tk.Frame(Cont, bg=GrisFondo, pady=14)
        MarcoBtn.pack()
        CrearBotonPrimario(MarcoBtn, "Generar reporte", Generar,
                           Icono=">", Ancho=16).pack(side="left", padx=4)
        CrearBotonSecundario(MarcoBtn, "Regresar", Sub.destroy,
                             Icono="<", Ancho=14).pack(side="left",
                                                       padx=4)

    def _ReportePorProvincia(self):
        self._AbrirSubVentanaProvincia(
            "Donantes por provincia", F.ReporteDonantesPorProvincia)

    def _ReportePorEdad(self):
        Sub = tk.Toplevel(self)
        Sub.title("Por rango de edad")
        CentrarVentana(Sub, 460, 300)
        Sub.configure(bg=GrisFondo)
        Sub.transient(self); Sub.grab_set()
        CrearHeader(Sub, Titulo="Por rango de edad",
                    Subtitulo="Entre 18 y 65 anios")
        VarIni = tk.StringVar(); VarFin = tk.StringVar()
        Cont = tk.Frame(Sub, bg=GrisFondo, padx=24, pady=14)
        Cont.pack(fill="both", expand=True)
        F1 = tk.Frame(Cont, bg=GrisFondo); F1.pack(pady=4)
        tk.Label(F1, text="Edad inicial:", bg=GrisFondo,
                 font=TamEtiqueta, fg=GrisOscuro, width=14,
                 anchor="e").pack(side="left")
        EntIni = tk.Entry(F1, textvariable=VarIni, width=8,
                          font=TamCampo, justify="center",
                          fg=GrisOscuro, bg=Blanco, relief="solid",
                          bd=1)
        EntIni.pack(side="left", padx=4, ipady=3)
        F2 = tk.Frame(Cont, bg=GrisFondo); F2.pack(pady=4)
        tk.Label(F2, text="Edad final:", bg=GrisFondo,
                 font=TamEtiqueta, fg=GrisOscuro, width=14,
                 anchor="e").pack(side="left")
        EntFin = tk.Entry(F2, textvariable=VarFin, width=8,
                          font=TamCampo, justify="center",
                          fg=GrisOscuro, bg=Blanco, relief="solid",
                          bd=1, state="disabled")
        EntFin.pack(side="left", padx=4, ipady=3)

        def OnIni(*_A):
            try:
                V = int(VarIni.get().strip())
                if 18 <= V <= 65:
                    EntFin.config(state="normal"); return
            except ValueError:
                pass
            EntFin.config(state="disabled")
        VarIni.trace_add("write", OnIni)

        def Generar():
            try:
                Ini = int(VarIni.get().strip())
            except ValueError:
                messagebox.showerror("Error",
                                     "Edad inicial entero 18-65.",
                                     parent=Sub); return
            if not (18 <= Ini <= 65):
                messagebox.showerror("Error",
                                     "Edad inicial entre 18 y 65.",
                                     parent=Sub); return
            Fin = None
            if VarFin.get().strip():
                try:
                    Fin = int(VarFin.get().strip())
                except ValueError:
                    messagebox.showerror("Error",
                                         "Edad final entero 18-65.",
                                         parent=Sub); return
                if not (18 <= Fin <= 65):
                    messagebox.showerror("Error",
                                         "Edad final entre 18 y 65.",
                                         parent=Sub); return
            self._MostrarResultado(
                F.ReportePorRangoEdad(Ini, Fin), "Por rango de edad")
            Sub.destroy()

        MarcoBtn = tk.Frame(Cont, bg=GrisFondo, pady=14)
        MarcoBtn.pack()
        CrearBotonPrimario(MarcoBtn, "Generar reporte", Generar,
                           Icono=">", Ancho=16).pack(side="left",
                                                     padx=4)
        CrearBotonSecundario(MarcoBtn, "Regresar", Sub.destroy,
                             Icono="<", Ancho=14).pack(side="left",
                                                       padx=4)

    def _ReportePorTipoYProvincia(self):
        Sub = tk.Toplevel(self)
        Sub.title("Por tipo y provincia")
        CentrarVentana(Sub, 460, 300)
        Sub.configure(bg=GrisFondo)
        Sub.transient(self); Sub.grab_set()
        CrearHeader(Sub, Titulo="Por tipo y provincia",
                    Subtitulo="Seleccione ambos criterios")
        VarTipo = tk.StringVar(); VarProv = tk.StringVar()
        Opciones = [f"{C} - {N}" for C, N in sorted(F.Provincias.items())]
        Cont = tk.Frame(Sub, bg=GrisFondo, padx=24, pady=10)
        Cont.pack(fill="both", expand=True)
        tk.Label(Cont, text="Tipo de sangre:", bg=GrisFondo,
                 font=TamEtiqueta, fg=GrisOscuro).pack(pady=2)
        ttk.Combobox(Cont, textvariable=VarTipo,
                     values=list(F.TiposDeSangre), state="readonly",
                     font=TamCampo, width=28).pack()
        tk.Label(Cont, text="Provincia:", bg=GrisFondo,
                 font=TamEtiqueta, fg=GrisOscuro).pack(pady=2)
        ttk.Combobox(Cont, textvariable=VarProv, values=Opciones,
                     state="readonly", font=TamCampo,
                     width=28).pack()

        def Generar():
            if not VarTipo.get() or not VarProv.get():
                messagebox.showerror("Error",
                                     "Seleccione tipo y provincia.",
                                     parent=Sub); return
            Cod = int(VarProv.get().split(" - ")[0])
            self._MostrarResultado(
                F.ReportePorTipoYProvincia(VarTipo.get(), Cod),
                "Por tipo y provincia")
            Sub.destroy()

        MarcoBtn = tk.Frame(Cont, bg=GrisFondo, pady=14)
        MarcoBtn.pack()
        CrearBotonPrimario(MarcoBtn, "Generar reporte", Generar,
                           Icono=">", Ancho=16).pack(side="left",
                                                     padx=4)
        CrearBotonSecundario(MarcoBtn, "Regresar", Sub.destroy,
                             Icono="<", Ancho=14).pack(side="left",
                                                       padx=4)

    def _ReporteCompleto(self):
        self._MostrarResultado(F.ReporteListaCompleta(),
                               "Lista completa")

    def _ReporteMujeresONegativo(self):
        self._MostrarResultado(F.ReporteMujeresONegativo(),
                               "Mujeres O-")

    def _ReporteNoActivos(self):
        self._MostrarResultado(F.ReporteDonantesNoActivos(),
                               "Donantes NO activos")

    def _ReporteLugares(self):
        self._MostrarResultado(F.ReporteLugaresDonacion(),
                               "Lugares de donacion")

    def _ReporteAQuienDona(self):
        self._AbrirSubVentanaTipoSangre(
            "A quien puede donar", F.ReporteAQuienPuedeDonar)

    def _ReporteDeQuienRecibe(self):
        self._AbrirSubVentanaTipoSangre(
            "De quien puede recibir", F.ReporteDeQuienPuedeRecibir)

# SECCION 10: PUNTO DE ENTRADA
def Main():
    """
    Funcion principal. Inicializa el modelo, aplica el tema,
    muestra splash, carga la BD y lanza la ventana principal.
    """
    F.InicializarModelo()
    BaseDeDatosCargada = A.CargarBaseDeDatos()
    Raiz = tk.Tk()
    AplicarTema(Raiz)
    VentanaPrincipal(Raiz, BaseDeDatosCargada=BaseDeDatosCargada)
    MostrarSplash(Raiz, Duracion=1500)
    Raiz.mainloop()

if __name__ == "__main__":
    Main()
