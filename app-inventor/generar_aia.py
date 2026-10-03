#!/usr/bin/env python3
"""Genera TimbreEscolar.aia (proyecto de MIT App Inventor).

Construye el diseño de la pantalla (Screen1.scm), los bloques (Screen1.bky)
y empaqueta los íconos de assets/ en un .aia listo para importar en
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
ASSETS = ["ic_timbre.png", "bt_on.png", "bt_off.png"]

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
AZUL_OSCURO = "&HFF002270"
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

LLENAR = "-2"        # Fill parent
AUTO = "-1"          # Automatic
ANCHO_TARJETA = "-1092"   # 92 % del ancho de la pantalla
ANCHO_INTERNO = "-1090"   # 90 % del ancho de la tarjeta

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


def etiqueta(nombre, texto, tam=14, negrita=False, color=TEXTO, **extra):
    props = {"Text": texto, "FontSize": tam, "TextColor": color}
    if negrita:
        props["FontBold"] = "True"
    props.update(extra)
    return comp("Label", nombre, **props)


def diseno():
    encabezado = comp("VerticalArrangement", "Encabezado", [
        espacio(alto=18),
        comp("HorizontalArrangement", "FilaTitulo", [
            espacio(ancho=20),
            comp("Image", "ImgLogo", Picture="ic_timbre.png", Width=64, Height=64,
                 ScalePictureToFit="True"),
            espacio(ancho=14),
            comp("VerticalArrangement", "BloqueTitulo", [
                etiqueta("LblTitulo", "Timbre Escolar", 22, True, BLANCO, HasMargins="False"),
                espacio(alto=2),
                etiqueta("LblSubtitulo", "Control de horarios por Bluetooth", 14,
                         color=BLANCO_80, HasMargins="False"),
            ]),
        ], Width=LLENAR, AlignVertical="2"),
        espacio(alto=14),
        comp("HorizontalArrangement", "FilaBadge", [
            espacio(ancho=20),
            comp("HorizontalArrangement", "BadgeBT", [
                espacio(ancho=10),
                comp("Image", "ImgBT", Picture="bt_off.png", Width=20, Height=20,
                     ScalePictureToFit="True"),
                comp("ListPicker", "LP_Conectar", Text="Desconectado · Toca para conectar",
                     FontSize=13, FontBold="True", TextColor=ROJO_TEXTO,
                     BackgroundColor=NINGUNO, Title="Elige tu ESP32",
                     ItemBackgroundColor=BLANCO, ItemTextColor=TEXTO),
                espacio(ancho=6),
            ], BackgroundColor=BLANCO, AlignVertical="2"),
        ], Width=LLENAR),
        espacio(alto=20),
    ], Width=LLENAR, BackgroundColor=AZUL)

    tarjeta_hora = comp("VerticalArrangement", "TarjetaHora", [
        espacio(alto=16),
        etiqueta("LblTituloHora", "🕒  Ajustar hora", 18, True, Width=ANCHO_INTERNO),
        espacio(alto=10),
        comp("TimePicker", "SelectorHora", Text="07:30", FontSize=40, FontBold="True",
             TextColor=AZUL, BackgroundColor=GRIS_FONDO, Shape="1",
             Width=ANCHO_INTERNO, Height=90),
        etiqueta("LblAyudaHora", "Toca la hora para cambiarla", 13, color=TEXTO_SEC,
                 Width=ANCHO_INTERNO, TextAlignment="1"),
        espacio(alto=10),
        comp("Button", "BtnAnadir", Text="⏰  Añadir a la lista", FontSize=16,
             FontBold="True", TextColor=TEXTO, BackgroundColor=AMARILLO, Shape="1",
             Width=ANCHO_INTERNO, Height=52),
        espacio(alto=16),
    ], Width=ANCHO_TARJETA, BackgroundColor=BLANCO, AlignHorizontal="3")

    tarjeta_lista = comp("VerticalArrangement", "TarjetaLista", [
        espacio(alto=16),
        comp("HorizontalArrangement", "CabeceraLista", [
            etiqueta("LblTituloLista", "Horarios programados", 18, True, Width=LLENAR),
            etiqueta("LblContador", "0", 13, True, AZUL, BackgroundColor=AZUL_TINTE,
                     Width=40, TextAlignment="1"),
        ], Width=ANCHO_INTERNO, AlignVertical="2"),
        etiqueta("LblAyudaLista", "Toca un horario para eliminarlo 🗑", 13,
                 color=TEXTO_SEC, Width=ANCHO_INTERNO),
        espacio(alto=6),
        espacio(alto=1, ancho=ANCHO_INTERNO, color=DIVISOR),
        comp("ListView", "ListaHorarios", Width=ANCHO_INTERNO, Height=LLENAR,
             BackgroundColor=BLANCO, TextColor=TEXTO, FontSize=22,
             SelectionColor=AZUL_TINTE),
        etiqueta("LblVacioIcono", "🔔", 40, Width=ANCHO_INTERNO, TextAlignment="1",
                 Visible="False"),
        etiqueta("LblVacioTitulo", "Aún no hay horarios", 16, True, Width=ANCHO_INTERNO,
                 TextAlignment="1", Visible="False"),
        etiqueta("LblVacioAyuda", "Elige una hora y pulsa «Añadir a la lista»", 13,
                 color=TEXTO_SEC, Width=ANCHO_INTERNO, TextAlignment="1",
                 Visible="False"),
        espacio(alto=10),
    ], Width=ANCHO_TARJETA, Height=LLENAR, BackgroundColor=BLANCO, AlignHorizontal="3")

    barra = comp("VerticalArrangement", "BarraInferior", [
        espacio(alto=10),
        etiqueta("LblEstadoSync", "Conecta el ESP32 para guardar", 13, color=TEXTO_SEC,
                 Width=ANCHO_TARJETA),
        espacio(alto=8),
        comp("Button", "BtnGuardar", Text="🔄  Guardar Todo en ESP32", FontSize=17,
             FontBold="True", TextColor=TEXTO, BackgroundColor=AMARILLO, Shape="1",
             Width=ANCHO_TARJETA, Height=56),
        espacio(alto=14),
    ], Width=LLENAR, BackgroundColor=BLANCO, AlignHorizontal="3")

    no_visibles = [
        comp("BluetoothClient", "BluetoothClient1"),
        comp("Clock", "RelojEstado", TimerInterval=3000),
        comp("TinyDB", "BaseDatos", Namespace="TimbreEscolar"),
        comp("Notifier", "Avisos"),
    ]

    form = {
        "$Name": "Screen1", "$Type": "Form", "$Version": VERSIONES["Form"],
        "Uuid": "0", "Title": "Timbre Escolar", "AppName": PROYECTO,
        "TitleVisible": "False", "BackgroundColor": GRIS_FONDO,
        "AlignHorizontal": "3", "Scrollable": "False", "Sizing": "Responsive",
        "Theme": "AppTheme.Light", "PrimaryColor": AZUL, "PrimaryColorDark": AZUL,
        "AccentColor": AMARILLO, "Icon": "ic_timbre.png", "ScreenOrientation": "portrait",
        "VersionCode": "1", "VersionName": "1.0", "ShowListsAsJson": "True",
        "$Components": [
            encabezado, espacio(alto=14), tarjeta_hora, espacio(alto=12),
            tarjeta_lista, espacio(alto=12), espacio(alto=1, ancho=LLENAR, color=DIVISOR),
            barra,
        ] + no_visibles,
    }
    return form


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


def color(r, g, b):
    rgb = B("lists_create_with", valores={"ADD0": num(r), "ADD1": num(g), "ADD2": num(b)},
            mutacion=M({"items": 3}))
    return B("color_make_color", valores={"COLORLIST": rgb})


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
def texto_mayor(a, b): return B("text_compare", {"OP": "GT"}, {"TEXT1": a, "TEXT2": b})
def largo(lst): return B("lists_length", valores={"LIST": lst})
def vacia(lst): return B("lists_is_empty", valores={"LIST": lst})
def esta_en(item, lst): return B("lists_is_in", valores={"ITEM": item, "LIST": lst})
def elemento(lst, i): return B("lists_select_item", valores={"LIST": lst, "NUM": i})
def unir_con(sep, lst): return B("lists_join_with_separator", valores={"SEPARATOR": sep, "LIST": lst})


def mas(a, b):
    return B("math_add", valores={"NUM0": a, "NUM1": b}, mutacion=M({"items": 2}))


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
def si(cond, entonces, sino=None):
    sent = {"DO0": entonces}
    mut = {}
    if sino:
        sent["ELSE"] = sino
        mut["else"] = 1
    return B("controls_if", valores={"IF0": cond}, sentencias=sent, mutacion=M(mut))


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


def proc(nombre, cuerpo):
    return B("procedures_defnoreturn", {"NAME": nombre}, sentencias={"STACK": cuerpo})


def ejecutar(nombre):
    return B("procedures_callnoreturn", {"PROCNAME": nombre}, mutacion=M({"name": nombre}))


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
    vis = lambda nombre, v: poner("Label", nombre, "Visible", v() if callable(v) else v)

    tops = [
        # Variables globales
        global_("horarios", lista_vacia()),
        global_("pendientes", falso()),
        global_("indiceBorrar", num(0)),

        # Al abrir la app: carga los horarios guardados en el teléfono
        evento("Form", "Screen1", "Initialize", [
            asignar("horarios", llamar("TinyDB", "BaseDatos", "GetValue",
                                       txt("horarios"), lista_vacia())),
            ejecutar("actualizarLista"),
            ejecutar("actualizarEstado"),
        ]),

        # Muestra la lista con su ícono, el contador y el estado vacío
        proc("actualizarLista", [
            local("vista", lista_vacia(), [
                para_cada("hora", g("horarios"), [
                    B("lists_add_items", valores={"LIST": loc("vista"),
                                                  "ITEM0": unir(txt("⏰   "), loc("hora"))},
                      mutacion=M({"items": 1})),
                ]),
                poner("ListView", "ListaHorarios", "Elements", loc("vista")),
            ]),
            poner("Label", "LblContador", "Text", largo(g("horarios"))),
            poner("ListView", "ListaHorarios", "Visible", no(vacia(g("horarios")))),
            vis("LblVacioIcono", lambda: vacia(g("horarios"))),
            vis("LblVacioTitulo", lambda: vacia(g("horarios"))),
            vis("LblVacioAyuda", lambda: vacia(g("horarios"))),
            poner("Label", "LblAyudaLista", "Visible", no(vacia(g("horarios")))),
        ]),

        # Pinta el badge Bluetooth y el botón Guardar según la conexión
        proc("actualizarEstado", [
            si(conectado(), [
                poner("HorizontalArrangement", "BadgeBT", "BackgroundColor", color(*C_AMARILLO)),
                poner("Image", "ImgBT", "Picture", txt("bt_on.png")),
                poner("ListPicker", "LP_Conectar", "Text", txt("Conectado · ESP32")),
                poner("ListPicker", "LP_Conectar", "TextColor", color(*C_AZUL)),
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
                poner("ListPicker", "LP_Conectar", "Text", txt("Desconectado · Toca para conectar")),
                poner("ListPicker", "LP_Conectar", "TextColor", color(*C_ROJO)),
                poner("Button", "BtnGuardar", "Enabled", falso()),
                poner("Button", "BtnGuardar", "BackgroundColor", color(*C_DESHAB_FONDO)),
                poner("Button", "BtnGuardar", "TextColor", color(*C_DESHAB_TEXTO)),
                poner("Label", "LblEstadoSync", "Text", txt("Conecta el ESP32 para guardar")),
                poner("Label", "LblEstadoSync", "TextColor", color(*C_SEC)),
            ]),
        ]),

        # Guarda la lista en la memoria del teléfono
        proc("guardarEnTelefono", [
            llamar("TinyDB", "BaseDatos", "StoreValue", txt("horarios"), g("horarios")),
        ]),

        # Selector de hora: muestra siempre HH:mm (24 h)
        evento("TimePicker", "SelectorHora", "AfterTimeSet", [
            poner("TimePicker", "SelectorHora", "Text",
                  llamar("Clock", "RelojEstado", "FormatDateTime",
                         leer("TimePicker", "SelectorHora", "Instant"), txt("HH:mm"))),
        ]),

        # Añadir a la lista (sin duplicados y en orden cronológico)
        evento("Button", "BtnAnadir", "Click", [
            local("hora", leer("TimePicker", "SelectorHora", "Text"), [
                si(esta_en(loc("hora"), g("horarios")), [
                    aviso(txt("Ese horario ya está en la lista")),
                ], [
                    local("posicion", mas(largo(g("horarios")), num(1)), [
                        para_rango("i", num(1), largo(g("horarios")), num(1), [
                            si(B("logic_operation", {"OP": "AND"}, {
                                "A": texto_mayor(elemento(g("horarios"), loc("i")), loc("hora")),
                                "B": igual(loc("posicion"), mas(largo(g("horarios")), num(1))),
                            }, mutacion=M({"items": 2})), [
                                asignar_loc("posicion", loc("i")),
                            ]),
                        ]),
                        B("lists_insert_item", valores={"LIST": g("horarios"),
                                                        "INDEX": loc("posicion"),
                                                        "ITEM": loc("hora")}),
                    ]),
                    asignar("pendientes", verdadero()),
                    ejecutar("guardarEnTelefono"),
                    ejecutar("actualizarLista"),
                    ejecutar("actualizarEstado"),
                    aviso(unir(txt("Horario "), loc("hora"), txt(" añadido"))),
                ]),
            ]),
        ]),

        # Tocar un horario de la lista: pedir confirmación para borrarlo
        evento("ListView", "ListaHorarios", "AfterPicking", [
            asignar("indiceBorrar", leer("ListView", "ListaHorarios", "SelectionIndex")),
            llamar("Notifier", "Avisos", "ShowChooseDialog",
                   unir(txt("¿Eliminar el horario de las "),
                        elemento(g("horarios"), g("indiceBorrar")), txt("?")),
                   txt("Eliminar horario"), txt("Eliminar"), txt("Cancelar"), falso()),
        ]),

        evento("Notifier", "Avisos", "AfterChoosing", [
            si(igual(param("choice"), txt("Eliminar")), [
                B("lists_remove_item", valores={"LIST": g("horarios"),
                                                "INDEX": g("indiceBorrar")}),
                asignar("pendientes", verdadero()),
                ejecutar("guardarEnTelefono"),
                ejecutar("actualizarLista"),
                ejecutar("actualizarEstado"),
                aviso(txt("Horario eliminado")),
            ]),
        ]),

        # Badge Bluetooth: lista los dispositivos emparejados
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

        # Guardar Todo en ESP32: envía la hora actual y la lista
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

        # Revisa la conexión cada 3 s para detectar desconexiones
        evento("Clock", "RelojEstado", "Timer", [
            si(no(conectado()), [ejecutar("actualizarEstado")]),
        ]),

        # Errores de Bluetooth: avisar sin cerrar la app
        evento("Form", "Screen1", "ErrorOccurred", [
            aviso(unir(txt("Error de Bluetooth: "), param("message"))),
            ejecutar("actualizarEstado"),
        ]),
    ]

    xml = ET.Element("xml", {"xmlns": "http://www.w3.org/1999/xhtml"})
    for i, t in enumerate(tops):
        t.set("x", str(20 + (i % 3) * 520))
        t.set("y", str(20 + (i // 3) * 420))
        xml.append(t)
    ET.SubElement(xml, "yacodeblocks", {"ya-version": YA_VERSION,
                                        "language-version": BLOCKS_VERSION})
    return xml


# ================================================================ empaquetado
def validar(form, xml):
    nombres = {c["$Name"]: c["$Type"] for c in recorrer(form)}
    assert len(nombres) == sum(1 for _ in recorrer(form)), "nombres de componentes repetidos"
    for m in xml.iter("mutation"):
        inst = m.get("instance_name")
        if inst:
            assert inst in nombres, "componente inexistente: " + inst
            assert nombres[inst] == m.get("component_type"), "tipo incorrecto: " + inst
    definidos = {f.text for b in xml.iter("block") if b.get("type") == "procedures_defnoreturn"
                 for f in b.findall("field")}
    for b in xml.iter("block"):
        if b.get("type") == "procedures_callnoreturn":
            assert b.find("field").text in definidos, "procedimiento sin definir"
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
        "versioncode=1",
        "versionname=1.0",
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
