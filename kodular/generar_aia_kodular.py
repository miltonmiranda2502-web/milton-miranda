#!/usr/bin/env python3
"""Genera TimbreEscolar_Kodular.aia para Kodular Creator (https://creator.kodular.io).

Versión del proyecto pensada para Kodular:
  - Tarjetas reales con esquinas redondeadas y sombra (componente Card View).
  - Filas de horario con botones de editar y borrar (íconos Material).
  - Fuente Poppins.

Reutiliza los ayudantes de ../app-inventor/generar_aia.py y los assets de
../app-inventor/assets. Uso:  python3 generar_aia_kodular.py
"""
import json
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "app-inventor"))
import generar_aia as ai  # noqa: E402
from generar_aia import (  # noqa: E402
    B, M, comp, espacio, etiqueta, boton, txt, num, verdadero, falso, lista_vacia, color,
    unir, g, loc, param, no, igual, distinto, texto_mayor, largo, vacia, esta_en, elemento,
    unir_con, dividir, y, mas, leer, poner, llamar, evento, si, global_, asignar,
    asignar_loc, local, para_cada, para_rango, proc, ejecutar, aviso, ahora,
    F_REG, F_MED, F_SEMI, F_BOLD, AZUL, AZUL_TINTE, AMARILLO, BLANCO, GRIS_FONDO, TEXTO,
    TEXTO_SEC, DIVISOR, ROJO_TEXTO, NINGUNO, BLANCO_80, BLANCO_70, VIDRIO, LLENAR,
    ANCHO_TARJETA, ANCHO_INTERNO,
)

PROYECTO = "TimbreEscolar"
USUARIO = "timbre_escolar"
SALIDA = os.path.join(AQUI, "TimbreEscolar_Kodular.aia")
F_ICONOS = "MaterialIcons-Regular.ttf"   # íconos por ligadura: texto "delete" -> papelera
ai.ASSETS = ai.ASSETS + [F_ICONOS]
MAX_FILAS = 20

# Formato de Kodular (tomado de un .aia exportado por Kodular). Las versiones de
# los componentes son iguales o menores a las de Kodular: el servidor las
# actualiza solo al importar.
YA_VERSION = "241"
BLOCKS_VERSION = "34"
ai.VERSIONES.update({
    "Form": "43", "Label": "10", "Notifier": "11", "Clock": "4",
    "Button": "6", "Image": "4", "HorizontalArrangement": "3",
    "VerticalArrangement": "3", "VerticalScrollArrangement": "2",
    "TimePicker": "3", "ListPicker": "9", "BluetoothClient": "5", "TinyDB": "2",
    "MakeroidCardView": "1",
})
ROJO = "&HFFE53E3E"
OPC_ELIMINAR = "🗑 Eliminar"
OPC_TOCAR = "🔔 Tocar"


# ================================================================ diseño
def tarjeta(nombre, hijos, ancho=ANCHO_TARJETA, fondo=BLANCO, radio=18, sombra=2, **extra):
    """Card View de Kodular con un VerticalArrangement centrado dentro."""
    cuerpo = comp("VerticalArrangement", nombre + "Cuerpo", hijos, Width=LLENAR,
                  AlignHorizontal="3", **({"Height": LLENAR} if extra.get("Height") else {}))
    return comp("MakeroidCardView", nombre, [cuerpo], Width=ancho, BackgroundColor=fondo,
                CornerRadius=radio, Elevation=sombra, **extra)


def tile(nombre, titulo, valor, detalle, color_valor):
    return tarjeta(nombre, [
        espacio(alto=10),
        comp("HorizontalArrangement", nombre + "Fila", [
            espacio(ancho=12),
            comp("VerticalArrangement", nombre + "Textos", [
                etiqueta("Lbl%sTitulo" % nombre, titulo, 10, F_MED, BLANCO_70),
                etiqueta("Lbl%sValor" % nombre, valor, 24, F_BOLD, color_valor),
                etiqueta("Lbl%sDetalle" % nombre, detalle, 11, F_REG, BLANCO_80),
            ]),
        ], Width=LLENAR),
        espacio(alto=10),
    ], ancho="-1044", fondo=VIDRIO, radio=16, sombra=0)


def icono(nombre, ligadura, color_icono):
    return comp("Button", nombre, Text=ligadura, FontTypeface=F_ICONOS, FontSize=24,
                TextColor=color_icono, BackgroundColor=NINGUNO, Width=44, Height=44)


def fila(i):
    return [
        comp("HorizontalArrangement", "Fila%d" % i, [
            comp("Image", "ImgAlarma%d" % i, Picture="ic_alarma.png", Width=40, Height=40,
                 ScalePictureToFit="True"),
            espacio(ancho=12),
            comp("VerticalArrangement", "TextosFila%d" % i, [
                etiqueta("LblHora%d" % i, "07:00", 20, F_SEMI),
                etiqueta("LblDetalle%d" % i, "Timbre %d" % i, 12, F_REG, TEXTO_SEC),
            ], Width=LLENAR),
            icono("BtnEditar%d" % i, "edit", AZUL),
            icono("BtnBorrar%d" % i, "delete", ROJO),
        ], Width=ANCHO_INTERNO, AlignVertical="2", Height=64, Visible="False"),
        espacio(alto=1, ancho=ANCHO_INTERNO, color=DIVISOR) | {"$Name": "Divisor%d" % i,
                                                               "Visible": "False"},
    ]


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
            comp("MakeroidCardView", "BadgeBT", [
                comp("HorizontalArrangement", "BadgeFila", [
                    espacio(ancho=12),
                    comp("Image", "ImgBT", Picture="bt_off.png", Width=18, Height=18,
                         ScalePictureToFit="True"),
                    comp("ListPicker", "LP_Conectar", Text="Desconectado · Conectar",
                         FontSize=12, FontTypeface=F_MED, TextColor=ROJO_TEXTO,
                         BackgroundColor=NINGUNO, Title="Elige tu ESP32",
                         ItemBackgroundColor=BLANCO, ItemTextColor=TEXTO),
                    espacio(ancho=4),
                ], AlignVertical="2"),
            ], BackgroundColor=BLANCO, CornerRadius=20, Elevation=0),
            espacio(ancho=LLENAR),
            boton("Button", "BtnTocar", "🔔 Tocar ahora", 13, AMARILLO, TEXTO, Height=40),
            espacio(ancho=16),
        ], Width=LLENAR, AlignVertical="2"),
        espacio(alto=16),
    ], Width=LLENAR, BackgroundColor=AZUL)

    tarjeta_hora = tarjeta("TarjetaHora", [
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
    ])

    filas = [c for i in range(1, MAX_FILAS + 1) for c in fila(i)]
    tarjeta_lista = tarjeta("TarjetaLista", [
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
        etiqueta("LblAyudaLista", "Usa ✏️ para editar y 🗑 para eliminar", 12, F_REG,
                 TEXTO_SEC, Width=ANCHO_INTERNO),
        espacio(alto=8),
        espacio(alto=1, ancho=ANCHO_INTERNO, color=DIVISOR),
    ] + filas + [
        espacio(alto=12),
        etiqueta("LblVacioIcono", "🔔", 36, Width=ANCHO_INTERNO, TextAlignment="1",
                 Visible="False"),
        etiqueta("LblVacioTitulo", "Aún no hay horarios", 15, F_SEMI, Width=ANCHO_INTERNO,
                 TextAlignment="1", Visible="False"),
        etiqueta("LblVacioAyuda", "Elige una hora y pulsa «＋ Añadir»", 12, F_REG, TEXTO_SEC,
                 Width=ANCHO_INTERNO, TextAlignment="1", Visible="False"),
        espacio(alto=12),
    ])

    contenido = comp("VerticalScrollArrangement", "Contenido", [
        espacio(alto=12), tarjeta_hora, espacio(alto=12), tarjeta_lista, espacio(alto=16),
        # Selector oculto: se abre desde los bloques al tocar el lápiz de una fila
        comp("TimePicker", "SelectorEditar", Text="Editar", Visible="False"),
    ], Width=LLENAR, Height=LLENAR, AlignHorizontal="3")

    barra = comp("VerticalArrangement", "BarraInferior", [
        espacio(alto=10),
        etiqueta("LblEstadoSync", "Conecta el ESP32 para guardar", 12, F_REG, TEXTO_SEC,
                 Width=ANCHO_TARJETA),
        espacio(alto=6),
        boton("Button", "BtnGuardar", "🔄  Guardar Todo en ESP32", 16, AMARILLO, TEXTO,
              Width=ANCHO_TARJETA, Height=56),
        espacio(alto=12),
    ], Width=LLENAR, BackgroundColor=BLANCO, AlignHorizontal="3")

    return {
        "$Name": "Screen1", "$Type": "Form", "$Version": ai.VERSIONES["Form"],
        "Uuid": "0", "Title": "Timbre Escolar", "AppName": PROYECTO,
        "TitleVisible": "False", "BackgroundColor": GRIS_FONDO,
        "AlignHorizontal": "3", "Scrollable": "False", "Sizing": "Responsive",
        "PrimaryColor": AZUL, "PrimaryColorDark": AZUL, "AccentColor": AMARILLO,
        "Icon": "ic_timbre.png", "ScreenOrientation": "portrait",
        "VersionCode": "3", "VersionName": "3.0",
        "$Components": [
            encabezado, contenido, espacio(alto=1, ancho=LLENAR, color=DIVISOR), barra,
            comp("BluetoothClient", "BluetoothClient1"),
            comp("Clock", "RelojEstado", TimerInterval=1000),
            comp("TinyDB", "BaseDatos", Namespace="TimbreEscolar"),
            comp("Notifier", "Avisos"),
            comp("Notifier", "AvisoTimbre"),
        ],
    }


# ================================================================ bloques
def componente(tipo, inst):
    return B("component_component_block", {"COMPONENT_SELECTOR": inst},
             mutacion=M({"component_type": tipo, "instance_name": inst}))


def lista_componentes(tipo, prefijo):
    items = {"ADD%d" % (i - 1): componente(tipo, "%s%d" % (prefijo, i))
             for i in range(1, MAX_FILAS + 1)}
    return B("lists_create_with", valores=items, mutacion=M({"items": MAX_FILAS}))


def poner_cualquiera(tipo, prop, componente_, valor):
    """set any <tipo>.<prop> of component."""
    return B("component_set_get", {"PROP": prop}, {"COMPONENT": componente_, "VALUE": valor},
             mutacion=M({"component_type": tipo, "set_or_get": "set", "property_name": prop,
                         "is_generic": "true"}))


def evento_cualquiera(tipo, nombre, cuerpo):
    """when any <tipo>.<nombre> (component, notAlreadyHandled)."""
    return B("component_event", sentencias={"DO": cuerpo},
             mutacion=M({"component_type": tipo, "is_generic": "true", "event_name": nombre}))


def posicion(item, lst): return B("lists_position_in", valores={"ITEM": item, "LIST": lst})
def menor_igual(a, b): return B("math_compare", {"OP": "LTE"}, {"A": a, "B": b})
def menor(a, b): return B("math_compare", {"OP": "LT"}, {"A": a, "B": b})
def mayor(a, b): return B("math_compare", {"OP": "GT"}, {"A": a, "B": b})
def mayor_igual(a, b): return B("math_compare", {"OP": "GTE"}, {"A": a, "B": b})


def bloques():
    BT = ("BluetoothClient", "BluetoothClient1")
    conectado = lambda: leer(*BT, "IsConnected")
    C_AZUL, C_AMARILLO, C_BLANCO = (0, 51, 160), (255, 209, 0), (255, 255, 255)
    C_TEXTO, C_SEC, C_ROJO = (30, 41, 59), (100, 116, 139), (197, 48, 48)
    C_DESHAB_FONDO, C_DESHAB_TEXTO = (226, 232, 240), (148, 163, 184)
    C_VIDRIO, C_BLANCO_TENUE = (255, 255, 255, 40), (255, 255, 255, 150)
    hay_vacia = lambda: vacia(g("horarios"))
    vis = lambda nombre, v: poner("Label", nombre, "Visible", v)
    de = lambda lista: elemento(g(lista), loc("i"))

    tops = [
        global_("horarios", lista_vacia()),
        global_("pendientes", falso()),
        global_("indiceSel", num(0)),
        global_("conectadoAntes", falso()),
        global_("filas", lista_vacia()),
        global_("divisores", lista_vacia()),
        global_("etiquetasHora", lista_vacia()),
        global_("etiquetasDetalle", lista_vacia()),
        global_("botonesEditar", lista_vacia()),
        global_("botonesBorrar", lista_vacia()),

        # Al abrir: arma las listas de filas y carga los horarios guardados
        evento("Form", "Screen1", "Initialize", [
            asignar("filas", lista_componentes("HorizontalArrangement", "Fila")),
            asignar("divisores", lista_componentes("Label", "Divisor")),
            asignar("etiquetasHora", lista_componentes("Label", "LblHora")),
            asignar("etiquetasDetalle", lista_componentes("Label", "LblDetalle")),
            asignar("botonesEditar", lista_componentes("Button", "BtnEditar")),
            asignar("botonesBorrar", lista_componentes("Button", "BtnBorrar")),
            asignar("horarios", llamar("TinyDB", "BaseDatos", "GetValue",
                                       txt("horarios"), lista_vacia())),
            ejecutar("actualizarLista"),
            ejecutar("actualizarEstado"),
            ejecutar("actualizarReloj"),
        ]),

        # Muestra una fila por horario (máximo 20) y oculta el resto
        proc("actualizarLista", [
            para_rango("i", num(1), num(MAX_FILAS), num(1), [
                si(menor_igual(loc("i"), largo(g("horarios"))), [
                    poner_cualquiera("Label", "Text", de("etiquetasHora"),
                                     elemento(g("horarios"), loc("i"))),
                    poner_cualquiera("Label", "Text", de("etiquetasDetalle"),
                                     unir(txt("Timbre "), loc("i"))),
                    poner_cualquiera("HorizontalArrangement", "Visible", de("filas"), verdadero()),
                    poner_cualquiera("Label", "Visible", de("divisores"),
                                     menor(loc("i"), largo(g("horarios")))),
                ], [
                    poner_cualquiera("HorizontalArrangement", "Visible", de("filas"), falso()),
                    poner_cualquiera("Label", "Visible", de("divisores"), falso()),
                ]),
            ]),
            poner("Label", "LblContador", "Text", largo(g("horarios"))),
            vis("LblAyudaLista", no(hay_vacia())),
            vis("LblVacioIcono", hay_vacia()),
            vis("LblVacioTitulo", hay_vacia()),
            vis("LblVacioAyuda", hay_vacia()),
            ejecutar("actualizarProximo"),
        ]),

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

        proc("actualizarReloj", [
            poner("Label", "LblHoraValor", "Text", ahora("HH:mm:ss")),
            poner("Label", "LblHoraDetalle", "Text", ahora("EEEE d MMM")),
            ejecutar("actualizarProximo"),
        ]),

        proc("actualizarEstado", [
            asignar("conectadoAntes", conectado()),
            si(conectado(), [
                poner("MakeroidCardView", "BadgeBT", "BackgroundColor", color(*C_AMARILLO)),
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
                poner("MakeroidCardView", "BadgeBT", "BackgroundColor", color(*C_BLANCO)),
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
                ], sino_si=[(mayor_igual(largo(g("horarios")), num(MAX_FILAS)), [
                    aviso(txt("Máximo %d horarios" % MAX_FILAS)),
                ])], sino=[
                    ejecutar("insertarOrdenado", "hora", loc("hora")),
                    ejecutar("trasCambio"),
                    aviso(unir(txt("Horario "), loc("hora"), txt(" añadido"))),
                ]),
            ]),
        ]),

        # ---------------------------------------------------- lápiz y papelera de cada fila
        evento_cualquiera("Button", "Click", [
            local("fila", posicion(param("component"), g("botonesEditar")), [
                si(mayor(loc("fila"), num(0)), [
                    asignar("indiceSel", loc("fila")),
                    local("partes", dividir(elemento(g("horarios"), loc("fila")), txt(":")), [
                        llamar("TimePicker", "SelectorEditar", "SetTimeToDisplay",
                               elemento(loc("partes"), num(1)), elemento(loc("partes"), num(2))),
                        llamar("TimePicker", "SelectorEditar", "LaunchPicker"),
                    ]),
                ]),
            ]),
            local("fila", posicion(param("component"), g("botonesBorrar")), [
                si(mayor(loc("fila"), num(0)), [
                    asignar("indiceSel", loc("fila")),
                    llamar("Notifier", "Avisos", "ShowChooseDialog",
                           unir(txt("¿Eliminar el timbre de las "),
                                elemento(g("horarios"), loc("fila")), txt("?")),
                           txt("Eliminar horario"), txt(OPC_ELIMINAR), txt("Cancelar"), falso()),
                ]),
            ]),
        ]),

        evento("Notifier", "Avisos", "AfterChoosing", [
            si(igual(param("choice"), txt(OPC_ELIMINAR)), [
                B("lists_remove_item", valores={"LIST": g("horarios"),
                                                "INDEX": g("indiceSel")}),
                ejecutar("trasCambio"),
                aviso(txt("Horario eliminado")),
            ]),
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

        evento("Clock", "RelojEstado", "Timer", [
            ejecutar("actualizarReloj"),
            si(distinto(conectado(), g("conectadoAntes")), [ejecutar("actualizarEstado")]),
        ]),

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
def main():
    form = diseno()
    xml = bloques()
    ai.validar(form, xml)
    tipos = {c["$Type"] for c in ai.recorrer(form)} - {"Form"}
    assert tipos <= set(ai.VERSIONES), "falta versión para: %s" % (tipos - set(ai.VERSIONES))

    scm = "#|\n$JSON\n" + json.dumps({
        "authURL": ["creator.kodular.io"], "YaVersion": YA_VERSION,
        "Source": "Form", "Properties": form}, ensure_ascii=False) + "\n|#\n"
    ET.indent(xml)
    bky = ET.tostring(xml, encoding="unicode")
    base = "src/io/kodular/%s/%s/" % (USUARIO, PROYECTO)
    props = "\n".join([
        "#",
        "#Proyecto generado por generar_aia_kodular.py",
        "showlistsasjson=True",
        "minSdk=21",
        "main=io.kodular.%s.%s.Screen1" % (USUARIO, PROYECTO),
        "color.accent=" + AMARILLO,
        "receiveSharedText=none",
        "sizing=Responsive",
        "screenNames=Screen1",
        "color.primary.dark=" + AZUL,
        "build=../build",
        "source=../src",
        "useslocation=False",
        "splashEnabled=False",
        "color.primary=" + AZUL,
        "assets=../assets",
        "versionname=3.0",
        "aname=" + PROYECTO,
        "versioncode=3",
        "theme=AppTheme.Light",
        "rtlSupport=False",
        "name=" + PROYECTO,
        "",
    ])

    with zipfile.ZipFile(SALIDA, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("youngandroidproject/project.properties", props)
        z.writestr(base + "Screen1.scm", scm)
        z.writestr(base + "Screen1.bky", bky)
        for a in ai.ASSETS:
            z.write(os.path.join(ai.AQUI, "assets", a), "assets/" + a)
    print("Generado:", SALIDA)


if __name__ == "__main__":
    main()
