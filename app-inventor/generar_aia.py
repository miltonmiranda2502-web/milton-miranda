#!/usr/bin/env python3
"""Genera TimbreEscolar.aia (proyecto de MIT App Inventor).

Construye el diseño de la pantalla (Screen1.scm), los bloques (Screen1.bky)
y empaqueta los íconos y fuentes de assets/ en un .aia listo para importar en
https://ai2.appinventor.mit.edu  (Proyectos > Importar proyecto .aia).

Uso:  python3 generar_aia.py
"""
import itertools
import json
import os
import zipfile
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
PROYECTO = "TimbreEscolar"
USUARIO = "ai_timbre"
SALIDA = os.path.join(AQUI, PROYECTO + ".aia")

# Fuentes Poppins (Google Fonts, licencia OFL)
F_REG = "Poppins-Regular.ttf"
F_MED = "Poppins-Medium.ttf"
F_SEMI = "Poppins-SemiBold.ttf"
F_BOLD = "Poppins-Bold.ttf"
ASSETS = ["ic_timbre.png", "ic_alarma.png", "bt_on.png", "bt_off.png",
          F_REG, F_MED, F_SEMI, F_BOLD]

# Versiones de App Inventor (nb199+). Son iguales o menores a las del
# servidor actual; si el servidor es más nuevo, actualiza el proyecto solo.
YA_VERSION = "232"
BLOCKS_VERSION = "37"
VERSIONES = {
    "Form": "31", "Button": "7", "Label": "5", "Image": "6",
    "HorizontalArrangement": "4", "VerticalArrangement": "4",
    "ListView": "10", "ListPicker": "9", "TimePicker": "4",
    "BluetoothClient": "8", "Clock": "4", "TinyDB": "3", "Notifier": "6",
}

# ---------------------------------------------------------------- colores
AZUL = "&HFF0033A0"
AZUL_TINTE = "&HFFE6EBF5"
AMARILLO = "&HFFFFD100"
BLANCO = "&HFFFFFFFF"
GRIS_FONDO = "&HFFF4F6F9"
TEXTO = "&HFF1E293B"
TEXTO_SEC = "&HFF64748B"
DIVISOR = "&HFFE2E8F0"
ROJO_TEXTO = "&HFFC53030"
NINGUNO = "&H00FFFFFF"
BLANCO_80 = "&HCCFFFFFF"
BLANCO_70 = "&HB3FFFFFF"
VIDRIO = "&H24FFFFFF"     # blanco al 14 %: "tarjetas de vidrio" del encabezado

# En App Inventor los porcentajes son del ANCHO DE LA PANTALLA (no del padre).
LLENAR = "-2"
ANCHO_TARJETA = "-1092"   # tarjeta: 92 % -> 4 % de margen a cada lado
ANCHO_INTERNO = "-1084"   # contenido: 84 % -> 4 % de relleno dentro de la tarjeta

# Textos de las opciones de los diálogos (los bloques los comparan)
OPC_EDITAR = "✏️ Editar"
OPC_ELIMINAR = "🗑 Eliminar"
OPC_TOCAR = "🔔 Tocar"

# ================================================================ diseño
_uuid = itertools.count(1000)


def comp(tipo, nombre, hijos=None, **props):
    c = {"$Name": nombre, "$Type": tipo, "$Version": VERSIONES[tipo],
         "Uuid": str(next(_uuid))}
    c.update({k: str(v) for k, v in props.items()})
    if hijos is not None:
        c["$Components"] = hijos
    return c


_esp = itertools.count(1)


def espacio(alto=None, ancho=None, color=None):
    props = {"HasMargins": "False", "Text": ""}
    if alto:
        props["Height"] = alto
    if ancho:
        props["Width"] = ancho
    if color:
        props["BackgroundColor"] = color
    return comp("Label", "Espacio%d" % next(_esp), **props)


def etiqueta(nombre, texto, tam=14, fuente=F_REG, color=TEXTO, **extra):
    props = {"Text": texto, "FontSize": tam, "FontTypeface": fuente, "TextColor": color,
             "HasMargins": "False"}
    props.update(extra)
    return comp("Label", nombre, **props)


def boton(tipo, nombre, texto, tam, fondo, color, **extra):
    props = {"Text": texto, "FontSize": tam, "FontTypeface": F_SEMI, "TextColor": color,
             "BackgroundColor": fondo, "Shape": "1"}
    props.update(extra)
    return comp(tipo, nombre, **props)


def tile(nombre, titulo, valor, detalle, color_valor):
    return comp("VerticalArrangement", nombre, [
        espacio(alto=10),
        comp("HorizontalArrangement", nombre + "Fila", [
            espacio(ancho=12),
            comp("VerticalArrangement", nombre + "Textos", [
                etiqueta("Lbl%sTitulo" % nombre, titulo, 10, F_MED, BLANCO_70),
                etiqueta("Lbl%sValor" % nombre, valor, 24, F_BOLD, color_valor),
                etiqueta("Lbl%sDetalle" % nombre, detalle, 11, F_REG, BLANCO_80),
            ]),
        ]),
        espacio(alto=10),
    ], Width="-1044", BackgroundColor=VIDRIO)


def diseno():
    encabezado = comp("VerticalArrangement", "Encabezado", [
        espacio(alto=16),
        comp("HorizontalArrangement", "FilaTitulo", [
            espacio(ancho=16),
            comp("Image", "ImgLogo", Picture="ic_timbre.png", Width=48, Height=48,
                 ScalePictureToFit="True"),
            espacio(ancho=12),
            comp("VerticalArrangement", "BloqueTitulo", [
                etiqueta("LblTitulo", "Timbre Escolar", 20, F_BOLD, BLANCO),
                etiqueta("LblSubtitulo", "Control de horarios por Bluetooth", 12, F_REG,
                         BLANCO_80),
            ]),
        ], Width=LLENAR, AlignVertical="2"),
        espacio(alto=14),
        comp("HorizontalArrangement", "FilaTiles", [
            tile("Hora", "HORA ACTUAL", "--:--:--", "", BLANCO),
            espacio(ancho=10),
            tile("Proximo", "PRÓXIMO TIMBRE", "--:--", "Sin horarios", AMARILLO),
        ], Width=LLENAR, AlignHorizontal="3"),
        espacio(alto=12),
        comp("HorizontalArrangement", "FilaBadge", [
            espacio(ancho=16),
            comp("HorizontalArrangement", "BadgeBT", [
                espacio(ancho=10),
                comp("Image", "ImgBT", Picture="bt_off.png", Width=18, Height=18,
                     ScalePictureToFit="True"),
                comp("ListPicker", "LP_Conectar", Text="Desconectado · Conectar",
                     FontSize=12, FontTypeface=F_MED, TextColor=ROJO_TEXTO,
                     BackgroundColor=NINGUNO, Title="Elige tu ESP32",
                     ItemBackgroundColor=BLANCO, ItemTextColor=TEXTO),
            ], BackgroundColor=BLANCO, AlignVertical="2"),
            espacio(ancho=LLENAR),
            boton("Button", "BtnTocar", "🔔 Tocar ahora", 13, AMARILLO, TEXTO, Height=40),
            espacio(ancho=16),
        ], Width=LLENAR, AlignVertical="2"),
        espacio(alto=16),
    ], Width=LLENAR, BackgroundColor=AZUL)

    tarjeta_hora = comp("VerticalArrangement", "TarjetaHora", [
        espacio(alto=14),
        etiqueta("LblOverHora", "PROGRAMAR", 11, F_SEMI, AZUL, Width=ANCHO_INTERNO),
        etiqueta("LblTituloHora", "Nueva hora de timbre", 17, F_SEMI, Width=ANCHO_INTERNO),
        espacio(alto=10),
        comp("HorizontalArrangement", "FilaHora", [
            boton("TimePicker", "SelectorHora", "07:30", 32, GRIS_FONDO, AZUL,
                  FontTypeface=F_BOLD, Width="-1046", Height=64),
            espacio(ancho=10),
            boton("Button", "BtnAnadir", "＋ Añadir", 16, AMARILLO, TEXTO,
                  Width="-1035", Height=64),
        ], Width=ANCHO_INTERNO, AlignVertical="2"),
        espacio(alto=6),
        etiqueta("LblAyudaHora", "Toca la hora para cambiarla", 12, F_REG, TEXTO_SEC,
                 Width=ANCHO_INTERNO),
        espacio(alto=14),
    ], Width=ANCHO_TARJETA, BackgroundColor=BLANCO, AlignHorizontal="3")

    tarjeta_lista = comp("VerticalArrangement", "TarjetaLista", [
        espacio(alto=14),
        comp("HorizontalArrangement", "CabeceraLista", [
            comp("VerticalArrangement", "BloqueTituloLista", [
                etiqueta("LblOverLista", "TU JORNADA", 11, F_SEMI, AZUL),
                etiqueta("LblTituloLista", "Horarios programados", 17, F_SEMI),
            ], Width=LLENAR),
            etiqueta("LblContador", "0", 14, F_SEMI, AZUL, BackgroundColor=AZUL_TINTE,
                     Width=40, Height=30, TextAlignment="1"),
        ], Width=ANCHO_INTERNO, AlignVertical="2"),
        espacio(alto=4),
        etiqueta("LblAyudaLista", "Toca un horario para editarlo o eliminarlo", 12, F_REG,
                 TEXTO_SEC, Width=ANCHO_INTERNO),
        espacio(alto=8),
        espacio(alto=1, ancho=ANCHO_INTERNO, color=DIVISOR),
        comp("ListView", "ListaHorarios", Width=ANCHO_INTERNO, Height=LLENAR,
             BackgroundColor=BLANCO, ListViewLayout="4", ImageWidth=40, ImageHeight=40,
             FontSize=20, FontTypeface=F_SEMI, TextColor=TEXTO,
             FontSizeDetail=12, FontTypefaceDetail=F_REG, TextColorDetail=TEXTO_SEC,
             SelectionColor=AZUL_TINTE),
        espacio(alto=20),
        etiqueta("LblVacioIcono", "🔔", 36, Width=ANCHO_INTERNO, TextAlignment="1",
                 Visible="False"),
        etiqueta("LblVacioTitulo", "Aún no hay horarios", 15, F_SEMI, Width=ANCHO_INTERNO,
                 TextAlignment="1", Visible="False"),
        etiqueta("LblVacioAyuda", "Elige una hora y pulsa «＋ Añadir»", 12, F_REG, TEXTO_SEC,
                 Width=ANCHO_INTERNO, TextAlignment="1", Visible="False"),
        espacio(alto=8),
        # Selector oculto: se abre desde los bloques al elegir "Editar"
        comp("TimePicker", "SelectorEditar", Text="Editar", Visible="False"),
    ], Width=ANCHO_TARJETA, Height=LLENAR, BackgroundColor=BLANCO, AlignHorizontal="3")

    barra = comp("VerticalArrangement", "BarraInferior", [
        espacio(alto=10),
        etiqueta("LblEstadoSync", "Conecta el ESP32 para guardar", 12, F_REG, TEXTO_SEC,
                 Width=ANCHO_TARJETA),
        espacio(alto=6),
        boton("Button", "BtnGuardar", "🔄  Guardar Todo en ESP32", 16, AMARILLO, TEXTO,
              Width=ANCHO_TARJETA, Height=56),
        espacio(alto=12),
    ], Width=LLENAR, BackgroundColor=BLANCO, AlignHorizontal="3")

    no_visibles = [
        comp("BluetoothClient", "BluetoothClient1"),
        comp("Clock", "RelojEstado", TimerInterval=1000),
        comp("TinyDB", "BaseDatos", Namespace="TimbreEscolar"),
        comp("Notifier", "Avisos"),
        comp("Notifier", "AvisoTimbre"),
    ]

    return {
        "$Name": "Screen1", "$Type": "Form", "$Version": VERSIONES["Form"],
        "Uuid": "0", "Title": "Timbre Escolar", "AppName": PROYECTO,
        "TitleVisible": "False", "BackgroundColor": GRIS_FONDO,
        "AlignHorizontal": "3", "Scrollable": "False", "Sizing": "Responsive",
        "Theme": "AppTheme.Light", "PrimaryColor": AZUL, "PrimaryColorDark": AZUL,
        "AccentColor": AMARILLO, "Icon": "ic_timbre.png", "ScreenOrientation": "portrait",
        "VersionCode": "2", "VersionName": "2.0", "ShowListsAsJson": "True",
        "$Components": [
            encabezado, espacio(alto=12), tarjeta_hora, espacio(alto=12),
            tarjeta_lista, espacio(alto=12), espacio(alto=1, ancho=LLENAR, color=DIVISOR),
            barra,
        ] + no_visibles,
    }


def recorrer(c):
    yield c
    for h in c.get("$Components", []):
        yield from recorrer(h)


# ================================================================ bloques
_bid = itertools.count(1)


def B(tipo, campos=None, valores=None, sentencias=None, mutacion=None):
    b = ET.Element("block", {"type": tipo, "id": "b%d" % next(_bid)})
    if mutacion is not None:
        b.append(mutacion)
    for k, v in (campos or {}).items():
        ET.SubElement(b, "field", {"name": k}).text = str(v)
    for k, v in (valores or {}).items():
        ET.SubElement(b, "value", {"name": k}).append(v)
    for k, v in (sentencias or {}).items():
        ET.SubElement(b, "statement", {"name": k}).append(cadena(v))
    return b


def M(attrs=None, *hijos):
    m = ET.Element("mutation", {k: str(v) for k, v in (attrs or {}).items()})
    for h in hijos:
        m.append(h)
    return m


def cadena(bloques):
    """Encadena una lista de bloques de sentencia con <next>."""
    bloques = [b for b in bloques if b is not None]
    for a, b in zip(bloques, bloques[1:]):
        ET.SubElement(a, "next").append(b)
    return bloques[0]


# --- valores
def txt(s): return B("text", {"TEXT": s})
def num(n): return B("math_number", {"NUM": n})
def verdadero(): return B("logic_boolean", {"BOOL": "TRUE"})
def falso(): return B("logic_boolean", {"BOOL": "FALSE"})
def lista_vacia(): return B("lists_create_with", mutacion=M({"items": 0}))


def color(*rgba):
    """make color [r g b] o [r g b alfa]."""
    lst = B("lists_create_with", valores={"ADD%d" % i: num(v) for i, v in enumerate(rgba)},
            mutacion=M({"items": len(rgba)}))
    return B("color_make_color", valores={"COLORLIST": lst})


def unir(*partes):
    return B("text_join", valores={"ADD%d" % i: p for i, p in enumerate(partes)},
             mutacion=M({"items": len(partes)}))


def g(nombre): return B("lexical_variable_get", {"VAR": "global " + nombre})
def loc(nombre): return B("lexical_variable_get", {"VAR": nombre})


def param(nombre):
    return B("lexical_variable_get", {"VAR": nombre},
             mutacion=M({}, ET.Element("eventparam", {"name": nombre})))


def no(v): return B("logic_negate", valores={"BOOL": v})
def igual(a, b): return B("logic_compare", {"OP": "EQ"}, {"A": a, "B": b})
def distinto(a, b): return B("logic_compare", {"OP": "NEQ"}, {"A": a, "B": b})
def texto_mayor(a, b): return B("text_compare", {"OP": "GT"}, {"TEXT1": a, "TEXT2": b})
def largo(lst): return B("lists_length", valores={"LIST": lst})
def vacia(lst): return B("lists_is_empty", valores={"LIST": lst})
def esta_en(item, lst): return B("lists_is_in", valores={"ITEM": item, "LIST": lst})
def elemento(lst, i): return B("lists_select_item", valores={"LIST": lst, "NUM": i})
def unir_con(sep, lst): return B("lists_join_with_separator", valores={"SEPARATOR": sep, "LIST": lst})
def dividir(t, sep): return B("text_split", {"OP": "SPLIT"}, {"TEXT": t, "AT": sep})


def y(a, b):
    return B("logic_operation", {"OP": "AND"}, {"A": a, "B": b}, mutacion=M({"items": 2}))


def mas(a, b):
    return B("math_add", valores={"NUM0": a, "NUM1": b}, mutacion=M({"items": 2}))


def agregar(lst, item):
    return B("lists_add_items", valores={"LIST": lst, "ITEM0": item}, mutacion=M({"items": 1}))


# --- componentes
def _mut_comp(tipo, inst, **extra):
    return M(dict(component_type=tipo, is_generic="false", instance_name=inst, **extra))


def leer(tipo, inst, prop):
    return B("component_set_get", {"COMPONENT_SELECTOR": inst, "PROP": prop},
             mutacion=_mut_comp(tipo, inst, set_or_get="get", property_name=prop))


def poner(tipo, inst, prop, valor):
    return B("component_set_get", {"COMPONENT_SELECTOR": inst, "PROP": prop},
             {"VALUE": valor},
             mutacion=_mut_comp(tipo, inst, set_or_get="set", property_name=prop))


def llamar(tipo, inst, metodo, *args):
    return B("component_method", {"COMPONENT_SELECTOR": inst},
             {"ARG%d" % i: a for i, a in enumerate(args)},
             mutacion=_mut_comp(tipo, inst, method_name=metodo))


def evento(tipo, inst, nombre, cuerpo):
    return B("component_event", {"COMPONENT_SELECTOR": inst}, sentencias={"DO": cuerpo},
             mutacion=_mut_comp(tipo, inst, event_name=nombre))


# --- control
def si(cond, entonces, sino=None, sino_si=()):
    """if cond / else if (c, cuerpo)... / else."""
    valores, sent, mut = {"IF0": cond}, {"DO0": entonces}, {}
    for i, (c, cuerpo) in enumerate(sino_si, start=1):
        valores["IF%d" % i] = c
        sent["DO%d" % i] = cuerpo
    if sino_si:
        mut["elseif"] = len(sino_si)
    if sino:
        sent["ELSE"] = sino
        mut["else"] = 1
    return B("controls_if", valores=valores, sentencias=sent, mutacion=M(mut))


def global_(nombre, valor):
    return B("global_declaration", {"NAME": nombre}, {"VALUE": valor})


def asignar(nombre, valor):
    return B("lexical_variable_set", {"VAR": "global " + nombre}, {"VALUE": valor})


def asignar_loc(nombre, valor):
    return B("lexical_variable_set", {"VAR": nombre}, {"VALUE": valor})


def local(nombre, inicial, cuerpo):
    return B("local_declaration_statement", {"VAR0": nombre}, {"DECL0": inicial},
             {"STACK": cuerpo}, mutacion=M({}, ET.Element("localname", {"name": nombre})))


def para_cada(var, lst, cuerpo):
    return B("controls_forEach", {"VAR": var}, {"LIST": lst}, {"DO": cuerpo})


def para_rango(var, ini, fin, paso, cuerpo):
    return B("controls_forRange", {"VAR": var}, {"START": ini, "END": fin, "STEP": paso},
             {"DO": cuerpo})


def proc(nombre, cuerpo, arg=None):
    if arg is None:
        return B("procedures_defnoreturn", {"NAME": nombre}, sentencias={"STACK": cuerpo})
    return B("procedures_defnoreturn", {"NAME": nombre, "VAR0": arg},
             sentencias={"STACK": cuerpo},
             mutacion=M({}, ET.Element("arg", {"name": arg})))


def ejecutar(nombre, arg=None, valor=None):
    if arg is None:
        return B("procedures_callnoreturn", {"PROCNAME": nombre}, mutacion=M({"name": nombre}))
    return B("procedures_callnoreturn", {"PROCNAME": nombre}, {"ARG0": valor},
             mutacion=M({"name": nombre}, ET.Element("arg", {"name": arg})))


def aviso(mensaje):
    return llamar("Notifier", "Avisos", "ShowAlert", mensaje)


def ahora(patron):
    return llamar("Clock", "RelojEstado", "FormatDateTime",
                  llamar("Clock", "RelojEstado", "Now"), txt(patron))


def bloques():
    BT = ("BluetoothClient", "BluetoothClient1")
    conectado = lambda: leer(*BT, "IsConnected")
    C_AZUL, C_AMARILLO, C_BLANCO = (0, 51, 160), (255, 209, 0), (255, 255, 255)
    C_TEXTO, C_SEC, C_ROJO = (30, 41, 59), (100, 116, 139), (197, 48, 48)
    C_DESHAB_FONDO, C_DESHAB_TEXTO = (226, 232, 240), (148, 163, 184)
    C_VIDRIO, C_BLANCO_TENUE = (255, 255, 255, 40), (255, 255, 255, 150)
    hay_vacia = lambda: vacia(g("horarios"))
    vis = lambda nombre, v: poner("Label", nombre, "Visible", v)

    tops = [
        # ---------------------------------------------------- variables
        global_("horarios", lista_vacia()),
        global_("pendientes", falso()),
        global_("indiceSel", num(0)),
        global_("conectadoAntes", falso()),

        # Al abrir la app: carga los horarios guardados en el teléfono
        evento("Form", "Screen1", "Initialize", [
            asignar("horarios", llamar("TinyDB", "BaseDatos", "GetValue",
                                       txt("horarios"), lista_vacia())),
            ejecutar("actualizarLista"),
            ejecutar("actualizarEstado"),
            ejecutar("actualizarReloj"),
        ]),

        # ---------------------------------------------------- procedimientos
        # Lista con ícono de alarma, número de timbre y pista de edición
        proc("actualizarLista", [
            local("vista", lista_vacia(), [
                para_rango("i", num(1), largo(g("horarios")), num(1), [
                    agregar(loc("vista"), llamar(
                        "ListView", "ListaHorarios", "CreateElement",
                        elemento(g("horarios"), loc("i")),
                        unir(txt("Timbre "), loc("i"), txt(" · toca para editar o eliminar")),
                        txt("ic_alarma.png"))),
                ]),
                poner("ListView", "ListaHorarios", "Elements", loc("vista")),
            ]),
            poner("Label", "LblContador", "Text", largo(g("horarios"))),
            poner("ListView", "ListaHorarios", "Visible", no(hay_vacia())),
            vis("LblAyudaLista", no(hay_vacia())),
            vis("LblVacioIcono", hay_vacia()),
            vis("LblVacioTitulo", hay_vacia()),
            vis("LblVacioAyuda", hay_vacia()),
            ejecutar("actualizarProximo"),
        ]),

        # Tarjeta "Próximo timbre" del encabezado
        proc("actualizarProximo", [
            local("ahora", ahora("HH:mm"), [
                local("proximo", txt(""), [
                    para_cada("hora", g("horarios"), [
                        si(y(igual(loc("proximo"), txt("")),
                             texto_mayor(loc("hora"), loc("ahora"))), [
                            asignar_loc("proximo", loc("hora")),
                        ]),
                    ]),
                    si(hay_vacia(), [
                        poner("Label", "LblProximoValor", "Text", txt("--:--")),
                        poner("Label", "LblProximoDetalle", "Text", txt("Sin horarios")),
                    ], sino_si=[(igual(loc("proximo"), txt("")), [
                        poner("Label", "LblProximoValor", "Text", elemento(g("horarios"), num(1))),
                        poner("Label", "LblProximoDetalle", "Text", txt("Mañana")),
                    ])], sino=[
                        poner("Label", "LblProximoValor", "Text", loc("proximo")),
                        poner("Label", "LblProximoDetalle", "Text", txt("Hoy")),
                    ]),
                ]),
            ]),
        ]),

        # Reloj en vivo del encabezado
        proc("actualizarReloj", [
            poner("Label", "LblHoraValor", "Text", ahora("HH:mm:ss")),
            poner("Label", "LblHoraDetalle", "Text", ahora("EEEE d MMM")),
            ejecutar("actualizarProximo"),
        ]),

        # Badge Bluetooth, botón "Tocar ahora" y botón Guardar según la conexión
        proc("actualizarEstado", [
            asignar("conectadoAntes", conectado()),
            si(conectado(), [
                poner("HorizontalArrangement", "BadgeBT", "BackgroundColor", color(*C_AMARILLO)),
                poner("Image", "ImgBT", "Picture", txt("bt_on.png")),
                poner("ListPicker", "LP_Conectar", "Text", txt("Conectado · ESP32")),
                poner("ListPicker", "LP_Conectar", "TextColor", color(*C_AZUL)),
                poner("Button", "BtnTocar", "Enabled", verdadero()),
                poner("Button", "BtnTocar", "BackgroundColor", color(*C_AMARILLO)),
                poner("Button", "BtnTocar", "TextColor", color(*C_TEXTO)),
                poner("Button", "BtnGuardar", "Enabled", verdadero()),
                poner("Button", "BtnGuardar", "BackgroundColor", color(*C_AMARILLO)),
                poner("Button", "BtnGuardar", "TextColor", color(*C_TEXTO)),
                si(g("pendientes"), [
                    poner("Label", "LblEstadoSync", "Text", txt("● Hay cambios sin guardar")),
                    poner("Label", "LblEstadoSync", "TextColor", color(*C_AZUL)),
                ], [
                    poner("Label", "LblEstadoSync", "Text", txt("✓ Todo sincronizado con el ESP32")),
                    poner("Label", "LblEstadoSync", "TextColor", color(*C_SEC)),
                ]),
            ], [
                poner("HorizontalArrangement", "BadgeBT", "BackgroundColor", color(*C_BLANCO)),
                poner("Image", "ImgBT", "Picture", txt("bt_off.png")),
                poner("ListPicker", "LP_Conectar", "Text", txt("Desconectado · Conectar")),
                poner("ListPicker", "LP_Conectar", "TextColor", color(*C_ROJO)),
                poner("Button", "BtnTocar", "Enabled", falso()),
                poner("Button", "BtnTocar", "BackgroundColor", color(*C_VIDRIO)),
                poner("Button", "BtnTocar", "TextColor", color(*C_BLANCO_TENUE)),
                poner("Button", "BtnGuardar", "Enabled", falso()),
                poner("Button", "BtnGuardar", "BackgroundColor", color(*C_DESHAB_FONDO)),
                poner("Button", "BtnGuardar", "TextColor", color(*C_DESHAB_TEXTO)),
                poner("Label", "LblEstadoSync", "Text", txt("Conecta el ESP32 para guardar o tocar el timbre")),
                poner("Label", "LblEstadoSync", "TextColor", color(*C_SEC)),
            ]),
        ]),

        # Inserta una hora en la lista manteniendo el orden cronológico
        proc("insertarOrdenado", [
            local("posicion", mas(largo(g("horarios")), num(1)), [
                para_rango("i", num(1), largo(g("horarios")), num(1), [
                    si(y(texto_mayor(elemento(g("horarios"), loc("i")), loc("hora")),
                         igual(loc("posicion"), mas(largo(g("horarios")), num(1)))), [
                        asignar_loc("posicion", loc("i")),
                    ]),
                ]),
                B("lists_insert_item", valores={"LIST": g("horarios"),
                                                "INDEX": loc("posicion"),
                                                "ITEM": loc("hora")}),
            ]),
        ], arg="hora"),

        # Después de añadir, editar o borrar: guardar y refrescar la pantalla
        proc("trasCambio", [
            asignar("pendientes", verdadero()),
            llamar("TinyDB", "BaseDatos", "StoreValue", txt("horarios"), g("horarios")),
            ejecutar("actualizarLista"),
            ejecutar("actualizarEstado"),
        ]),

        # ---------------------------------------------------- añadir
        evento("TimePicker", "SelectorHora", "AfterTimeSet", [
            poner("TimePicker", "SelectorHora", "Text",
                  llamar("Clock", "RelojEstado", "FormatDateTime",
                         leer("TimePicker", "SelectorHora", "Instant"), txt("HH:mm"))),
        ]),

        evento("Button", "BtnAnadir", "Click", [
            local("hora", leer("TimePicker", "SelectorHora", "Text"), [
                si(esta_en(loc("hora"), g("horarios")), [
                    aviso(txt("Ese horario ya está en la lista")),
                ], [
                    ejecutar("insertarOrdenado", "hora", loc("hora")),
                    ejecutar("trasCambio"),
                    aviso(unir(txt("Horario "), loc("hora"), txt(" añadido"))),
                ]),
            ]),
        ]),

        # ---------------------------------------------------- editar / eliminar
        evento("ListView", "ListaHorarios", "AfterPicking", [
            asignar("indiceSel", leer("ListView", "ListaHorarios", "SelectionIndex")),
            local("hora", elemento(g("horarios"), g("indiceSel")), [
                llamar("Notifier", "Avisos", "ShowChooseDialog",
                       unir(txt("¿Qué quieres hacer con el timbre de las "), loc("hora"), txt("?")),
                       unir(txt("Horario "), loc("hora")),
                       txt(OPC_EDITAR), txt(OPC_ELIMINAR), verdadero()),
            ]),
        ]),

        evento("Notifier", "Avisos", "AfterChoosing", [
            si(igual(param("choice"), txt(OPC_EDITAR)), [
                local("partes", dividir(elemento(g("horarios"), g("indiceSel")), txt(":")), [
                    llamar("TimePicker", "SelectorEditar", "SetTimeToDisplay",
                           elemento(loc("partes"), num(1)), elemento(loc("partes"), num(2))),
                    llamar("TimePicker", "SelectorEditar", "LaunchPicker"),
                ]),
            ], sino_si=[(igual(param("choice"), txt(OPC_ELIMINAR)), [
                B("lists_remove_item", valores={"LIST": g("horarios"),
                                                "INDEX": g("indiceSel")}),
                ejecutar("trasCambio"),
                aviso(txt("Horario eliminado")),
            ])]),
        ]),

        evento("TimePicker", "SelectorEditar", "AfterTimeSet", [
            local("nueva", llamar("Clock", "RelojEstado", "FormatDateTime",
                                  leer("TimePicker", "SelectorEditar", "Instant"), txt("HH:mm")), [
                local("vieja", elemento(g("horarios"), g("indiceSel")), [
                    si(distinto(loc("nueva"), loc("vieja")), [
                        si(esta_en(loc("nueva"), g("horarios")), [
                            aviso(txt("Ese horario ya está en la lista")),
                        ], [
                            B("lists_remove_item", valores={"LIST": g("horarios"),
                                                            "INDEX": g("indiceSel")}),
                            ejecutar("insertarOrdenado", "hora", loc("nueva")),
                            ejecutar("trasCambio"),
                            aviso(unir(txt("Horario cambiado: "), loc("vieja"), txt(" → "),
                                       loc("nueva"))),
                        ]),
                    ]),
                ]),
            ]),
        ]),

        # ---------------------------------------------------- Bluetooth
        evento("ListPicker", "LP_Conectar", "BeforePicking", [
            poner("ListPicker", "LP_Conectar", "Elements", leer(*BT, "AddressesAndNames")),
        ]),

        evento("ListPicker", "LP_Conectar", "AfterPicking", [
            si(conectado(), [llamar(*BT, "Disconnect")]),
            poner("ListPicker", "LP_Conectar", "Text", txt("Conectando…")),
            si(llamar(*BT, "Connect", leer("ListPicker", "LP_Conectar", "Selection")), [
                aviso(txt("Conectado al ESP32")),
            ], [
                aviso(txt("No se pudo conectar. ¿Está encendido y emparejado?")),
            ]),
            ejecutar("actualizarEstado"),
        ]),

        # ---------------------------------------------------- tocar el timbre ahora
        evento("Button", "BtnTocar", "Click", [
            si(no(conectado()), [
                aviso(txt("Primero conecta el ESP32")),
            ], [
                llamar("Notifier", "AvisoTimbre", "ShowChooseDialog",
                       txt("El timbre sonará ahora mismo en toda la institución."),
                       txt("¿Tocar el timbre?"), txt(OPC_TOCAR), txt("Cancelar"), falso()),
            ]),
        ]),

        evento("Notifier", "AvisoTimbre", "AfterChoosing", [
            si(igual(param("choice"), txt(OPC_TOCAR)), [
                llamar(*BT, "SendText", txt("TOCAR\\n")),
                aviso(txt("🔔 Timbre activado")),
            ]),
        ]),

        # ---------------------------------------------------- guardar en el ESP32
        evento("Button", "BtnGuardar", "Click", [
            si(no(conectado()), [
                aviso(txt("Primero conecta el ESP32")),
            ], [
                llamar(*BT, "SendText", unir(txt("HORA="), ahora("yyyy-MM-dd HH:mm:ss"), txt("\\n"))),
                llamar(*BT, "SendText", unir(txt("HORARIOS="), unir_con(txt(","), g("horarios")),
                                             txt("\\n"))),
                asignar("pendientes", falso()),
                ejecutar("actualizarEstado"),
                poner("Label", "LblEstadoSync", "Text",
                      unir(txt("✓ Última sincronización: hoy "), ahora("HH:mm"))),
                aviso(txt("¡Guardado en ESP32!")),
            ]),
        ]),

        # Cada segundo: reloj, próximo timbre y detección de desconexión
        evento("Clock", "RelojEstado", "Timer", [
            ejecutar("actualizarReloj"),
            si(distinto(conectado(), g("conectadoAntes")), [ejecutar("actualizarEstado")]),
        ]),

        # Errores de Bluetooth: avisar sin cerrar la app
        evento("Form", "Screen1", "ErrorOccurred", [
            aviso(unir(txt("Error de Bluetooth: "), param("message"))),
            ejecutar("actualizarEstado"),
        ]),
    ]

    xml = ET.Element("xml", {"xmlns": "http://www.w3.org/1999/xhtml"})
    for i, t in enumerate(tops):
        t.set("x", str(20 + (i % 3) * 560))
        t.set("y", str(20 + (i // 3) * 520))
        xml.append(t)
    ET.SubElement(xml, "yacodeblocks", {"ya-version": YA_VERSION,
                                        "language-version": BLOCKS_VERSION})
    return xml


# ================================================================ empaquetado
def validar(form, xml):
    todos = list(recorrer(form))
    nombres = {c["$Name"]: c["$Type"] for c in todos}
    assert len(nombres) == len(todos), "nombres de componentes repetidos"
    for m in xml.iter("mutation"):
        inst = m.get("instance_name")
        if inst:
            assert inst in nombres, "componente inexistente: " + inst
            assert nombres[inst] == m.get("component_type"), "tipo incorrecto: " + inst
    definidos = {b.find("field").text for b in xml.iter("block")
                 if b.get("type") == "procedures_defnoreturn"}
    for b in xml.iter("block"):
        if b.get("type") == "procedures_callnoreturn":
            assert b.find("field").text in definidos, "procedimiento sin definir"
    globales = {b.find("field").text for b in xml.iter("block")
                if b.get("type") == "global_declaration"}
    for f in xml.iter("field"):
        if f.get("name") == "VAR" and (f.text or "").startswith("global "):
            assert f.text[7:] in globales, "variable global sin definir: " + f.text
    for c in todos:
        for k in ("Picture", "Icon", "FontTypeface", "FontTypefaceDetail"):
            v = c.get(k)
            if v and not v.isdigit():
                assert v in ASSETS, "asset no incluido: " + v
    for a in ASSETS:
        assert os.path.exists(os.path.join(AQUI, "assets", a)), "falta " + a


def main():
    form = diseno()
    xml = bloques()
    validar(form, xml)

    scm = "#|\n$JSON\n" + json.dumps({
        "authURL": ["ai2.appinventor.mit.edu"], "YaVersion": YA_VERSION,
        "Source": "Form", "Properties": form}, ensure_ascii=False) + "\n|#\n"
    ET.indent(xml)
    bky = ET.tostring(xml, encoding="unicode")
    base = "src/appinventor/%s/%s/" % (USUARIO, PROYECTO)
    props = "\n".join([
        "#",
        "#Proyecto generado por generar_aia.py",
        "main=appinventor.%s.%s.Screen1" % (USUARIO, PROYECTO),
        "name=" + PROYECTO,
        "assets=../assets",
        "source=../src",
        "build=../build",
        "versioncode=2",
        "versionname=2.0",
        "useslocation=False",
        "aname=" + PROYECTO,
        "sizing=Responsive",
        "showlistsasjson=True",
        "actionbar=False",
        "theme=AppTheme.Light",
        "color.primary=" + AZUL,
        "color.primary.dark=" + AZUL,
        "color.accent=" + AMARILLO,
        "defaultfilescope=App",
        "",
    ])

    with zipfile.ZipFile(SALIDA, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("youngandroidproject/project.properties", props)
        z.writestr(base + "Screen1.scm", scm)
        z.writestr(base + "Screen1.bky", bky)
        for a in ASSETS:
            z.write(os.path.join(AQUI, "assets", a), "assets/" + a)
    print("Generado:", SALIDA)


if __name__ == "__main__":
    main()
