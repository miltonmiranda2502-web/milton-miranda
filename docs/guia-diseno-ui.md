# Timbre Escolar BT: guía de diseño UI/UX (Android)

Concepto visual y especificaciones para la app móvil que programa los horarios de un timbre automático escolar/institucional controlado por un **ESP32 vía Bluetooth**.

- **Plataforma:** Android, basado en Material Design 3 y adaptado a la identidad institucional.
- **Lienzo de referencia:** 360 × 800 dp (teléfono Android medio). Todas las medidas están en **dp** y los textos en **sp**.
- **Retícula:** múltiplos de 8 dp (4 dp para ajustes finos).
- **Pantalla única:** todo el flujo (conectar, añadir horario, revisar lista, sincronizar) cabe en una sola vista con scroll.

---

## 1. Paleta de colores

### 1.1 Colores institucionales (los del brief)

| Token | Hex | Uso |
|---|---|---|
| `azulRey` | `#0033A0` | Encabezado, íconos activos, botones secundarios, hora destacada |
| `amarilloCalido` | `#FFD100` | Acciones principales (CTA), highlights, badge "Conectado" |
| `blanco` | `#FFFFFF` | Superficie de tarjetas, barra inferior |
| `grisFondo` | `#F4F6F9` | Fondo general, contenedor del selector de hora |
| `textoOscuro` | `#1E293B` | Texto principal, texto sobre amarillo |
| `rojoSuave` | `#E53E3E` | Papelera, alertas, estado "Desconectado" |

### 1.2 Tonos de apoyo derivados

Salen de la misma familia y hacen falta para textos secundarios, divisores y estados.

| Token | Hex | Uso |
|---|---|---|
| `azulTinte` | `#E6EBF5` | Fondo del círculo de los íconos de alarma (azul rey al 10 %) |
| `azulOscuro` | `#002270` | Estado *pressed* de elementos azules y degradado del encabezado |
| `amarilloPressed` | `#E6BC00` | Estado *pressed* del botón amarillo |
| `textoSecundario` | `#64748B` | Subtítulos, etiquetas, texto de ayuda |
| `divisor` | `#E2E8F0` | Separadores de lista y bordes de tarjeta |
| `deshabilitadoFondo` | `#E2E8F0` | Botones deshabilitados |
| `deshabilitadoTexto` | `#94A3B8` | Texto e ícono de botones deshabilitados |
| `rojoTexto` | `#C53030` | Rojo para **texto pequeño** (ver contraste) |
| `rojoTinte` | `#FDECEC` | Fondo del gesto "deslizar para borrar" |

### 1.3 Contraste (WCAG 2.1)

| Combinación | Ratio | Resultado |
|---|---|---|
| Blanco sobre `#0033A0` | ≈ 10.6 : 1 | AAA ✔ |
| `#1E293B` sobre `#FFD100` | ≈ 10.0 : 1 | AAA ✔ (texto de los botones amarillos) |
| `#0033A0` sobre `#FFD100` | ≈ 7.3 : 1 | AAA ✔ |
| `#1E293B` sobre `#FFFFFF` | ≈ 14.6 : 1 | AAA ✔ |
| `#E53E3E` sobre `#FFFFFF` | ≈ 4.1 : 1 | ⚠ Sirve para íconos y texto grande (≥ 18 sp), **no** para texto pequeño. En ese caso usar `#C53030`. |
| `#FFD100` sobre `#FFFFFF` | ≈ 1.4 : 1 | ✘ **Nunca** poner texto o íconos amarillos sobre blanco. El amarillo funciona como relleno, no como tinta. |

> **Regla de oro:** sobre amarillo siempre va texto `#1E293B` (o azul rey); sobre azul siempre va blanco o amarillo.

---

## 2. Tipografía y jerarquía visual

- **Títulos y horas:** **Poppins** (geométrica, amigable e institucional).
- **Textos de interfaz y cuerpo:** **Roboto** (la nativa de Android, muy legible en tamaños pequeños).
- Ambas son gratuitas en Google Fonts (licencia OFL) y se pueden integrar con *Downloadable Fonts* de Android.
- Las horas usan **cifras tabulares** (`fontFeatureSettings = "tnum"`) para que los dígitos queden alineados en columna.

| Estilo | Fuente | Tamaño | Peso | Interlineado | Color | Uso |
|---|---|---|---|---|---|---|
| `display/hora` | Poppins | 48 sp | Bold 700 | 56 sp | `#0033A0` | Hora seleccionada en el selector |
| `titulo/app` | Poppins | 22 sp | Bold 700 | 28 sp | `#FFFFFF` | Nombre de la app en el encabezado |
| `subtitulo/app` | Roboto | 14 sp | Regular 400 | 20 sp | `#FFFFFF` al 80 % | Nombre de la institución |
| `titulo/tarjeta` | Poppins | 18 sp | SemiBold 600 | 24 sp | `#1E293B` | "Ajustar hora", "Horarios programados" |
| `hora/lista` | Poppins | 20 sp | SemiBold 600 | 28 sp | `#1E293B` | Cada horario de la lista |
| `cuerpo` | Roboto | 16 sp | Regular 400 | 24 sp | `#1E293B` | Mensajes y estado vacío |
| `etiqueta/boton` | Roboto | 16 sp | Bold 700 | 20 sp | `#1E293B` | Texto de los CTA (sin MAYÚSCULAS forzadas) |
| `etiqueta/badge` | Roboto | 12 sp | Medium 500 | 16 sp | según estado | "Conectado", "Desconectado" |
| `secundario` | Roboto | 13 sp | Regular 400 | 18 sp | `#64748B` | "Timbre 3 · Lun–Vie", textos de ayuda |
| `caption` | Roboto | 12 sp | Regular 400 | 16 sp | `#64748B` | "Última sincronización: 07:02" |

**Jerarquía en pantalla:** (1) estado Bluetooth y título → (2) hora grande seleccionada → (3) lista de horarios → (4) botón de sincronizar. El amarillo marca solo las **dos** acciones importantes (añadir y guardar) para que el ojo vaya directo a ellas.

---

## 3. Maquetación de la pantalla (mockup en texto)

```
┌──────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓ barra de estado (azul) ▓▓▓▓▓▓▓│  24 dp
│▓                                        ▓│
│▓   ╭────╮                               ▓│
│▓   │ 🔔 │  Timbre Escolar               ▓│  SECCIÓN 1
│▓   ╰────╯  Colegio San José             ▓│  Encabezado azul #0033A0
│▓   (72dp, círculo amarillo)             ▓│  alto 184 dp
│▓                                        ▓│  esquinas inf. 28 dp
│▓   ╭──────────────────────╮             ▓│
│▓   │ ᛒ  Conectado · ESP32-Timbre │      ▓│  ← badge pill amarillo
│▓   ╰──────────────────────╯             ▓│
│▓▓▓▓▓▓╭──────────────────────────────╮▓▓▓▓│  ← la tarjeta se solapa
│      │ 🕒  Ajustar hora             │    │    24 dp sobre el azul
│      │                              │    │
│      │   ╭──────────────────────╮   │    │  SECCIÓN 2
│      │   │       07 : 30        │   │    │  Tarjeta blanca
│      │   │  toca para cambiar   │   │    │  selector gris #F4F6F9
│      │   ╰──────────────────────╯   │    │
│      │ ┌──────────────────────────┐ │    │
│      │ │  ⏰+  Añadir a la lista   │ │    │  ← botón amarillo 52 dp
│      │ └──────────────────────────┘ │    │
│      ╰──────────────────────────────╯    │
│                 16 dp                    │
│      ╭──────────────────────────────╮    │
│      │ Horarios programados    (6)  │    │  SECCIÓN 3
│      │──────────────────────────────│    │  Tarjeta blanca con lista
│      │ (⏰) 07:00  Entrada       🗑  │    │
│      │──────────────────────────────│    │  fila 72 dp
│      │ (⏰) 09:15  Receso        🗑  │    │
│      │──────────────────────────────│    │
│      │ (⏰) 09:45  Fin de receso 🗑  │    │
│      │            …                 │    │
│      ╰──────────────────────────────╯    │
│                                          │  (espacio extra para que
│                                          │   la barra fija no tape)
├──────────────────────────────────────────┤
│  Última sincronización: hoy 07:02        │  SECCIÓN 4
│ ┌──────────────────────────────────────┐ │  Barra inferior fija
│ │  ⟳  Guardar Todo en ESP32         •  │ │  botón amarillo 56 dp
│ └──────────────────────────────────────┘ │  (• = cambios pendientes)
└──────────────────────────────────────────┘
```

### 3.1 Sección 1: encabezado y estado

- **Fondo:** azul rey `#0033A0` con un degradado vertical muy sutil hacia `#002270` en la parte baja. Ocupa todo el ancho, mide 184 dp de alto (sin contar la barra de estado) y tiene esquinas inferiores redondeadas de 28 dp.
- **Barra de estado** del sistema en el mismo azul, con íconos claros (`windowLightStatusBar = false`).
- **Identidad:** a la izquierda, un círculo amarillo de 72 dp con la campana azul rey dentro (ver [`assets/ic_timbre.svg`](assets/ic_timbre.svg)). A su derecha, el título "Timbre Escolar" y debajo el nombre de la institución.
- **Toque decorativo (opcional):** dos o tres arcos concéntricos de "onda sonora" en blanco al 8 % saliendo de la esquina superior derecha. Dan profundidad sin restar legibilidad.
- **Badge Bluetooth:** una píldora debajo del título, alineada a la izquierda con el texto. Al tocarla se abre la hoja de dispositivos emparejados.
- **Botón de ajustes (opcional):** ícono `more_vert` blanco de 24 dp dentro de un área táctil de 48 dp en la esquina superior derecha.

**Estados del badge**

| Estado | Fondo | Ícono (Material Symbols) | Texto | Color de texto e ícono |
|---|---|---|---|---|
| Conectado | `#FFD100` | `bluetooth_connected` | "Conectado · ESP32-Timbre" | `#0033A0` |
| Buscando | `#FFFFFF` al 15 % + borde blanco al 40 % | `bluetooth_searching`, con pulso de opacidad 1 → 0.4 cada 1.2 s | "Conectando…" | `#FFFFFF` |
| Desconectado | `#FFFFFF` | `bluetooth_disabled` | "Desconectado · Toca para conectar" | ícono `#E53E3E`, texto `#C53030` |

> No dependas solo del color: cada estado cambia también el **ícono** y el **texto**, así funciona para personas con daltonismo.

### 3.2 Sección 2: ajuste de hora

- La tarjeta blanca **sube 24 dp sobre el encabezado** (margen superior negativo). Ese solape es lo que hace que la interfaz se vea "de app moderna".
- **Encabezado de la tarjeta:** ícono `schedule` azul rey de 24 dp y el título "Ajustar hora".
- **Selector visual:** un contenedor gris `#F4F6F9` de 112 dp de alto y radio 12 dp, con la hora en grande (`07 : 30`, Poppins 48 sp azul rey) y debajo "Toca para cambiar" en texto secundario.
  - Al tocarlo se abre un `MaterialTimePicker` en **formato 24 h** con el tema de la app: reloj y selección en azul rey, botón "Aceptar" en azul. Un timbre se programa en hora exacta, así que 24 h evita confusiones AM/PM.
  - **Alternativa** si se prefiere todo en línea: dos ruedas (`NumberPicker`) para HH y MM separadas por ":" en azul, con el valor activo en 32 sp Bold y los vecinos en 20 sp al 40 % de opacidad.
- **Botón "Añadir a la lista":** primario amarillo a todo el ancho, 52 dp de alto, radio 12 dp, ícono `alarm_add` y texto `#1E293B`.
- **Validaciones:** si la hora ya existe, se muestra un Snackbar "Ese horario ya está en la lista" y la fila repetida destella en amarillo al 30 % durante 600 ms.

### 3.3 Sección 3: lista de horarios

- **Cabecera:** "Horarios programados" y, a la derecha, un chip contador (fondo `#E6EBF5`, texto azul rey 12 sp Bold) con el total, p. ej. `6`. Si el ESP32 tiene un tope de horarios, conviene mostrarlo así: `6 / 20`.
- **Fila de horario** (72 dp):
  - **Inicio:** círculo de 40 dp en `#E6EBF5` con el ícono `alarm` azul rey de 22 dp.
  - **Centro:** la hora (`07:00`, Poppins 20 sp SemiBold) y debajo una etiqueta opcional ("Entrada", "Timbre 1") en texto secundario.
  - **Final:** botón de ícono `delete` (papelera) de 24 dp en `#E53E3E` dentro de un área táctil de 48 dp. Al presionarlo aparece un *ripple* en `#FDECEC`.
- **Orden** cronológico automático, de la más temprana a la más tardía.
- **Divisores** de 1 dp en `#E2E8F0` con sangría a la izquierda de 72 dp (alineados con el texto, no con el ícono).
- **Borrado seguro:** al tocar la papelera, la fila se va con un *fade* y aparece un Snackbar "Horario eliminado" con la acción **DESHACER** en amarillo. También se puede deslizar la fila a la izquierda: aparece un fondo `#FDECEC` con la papelera roja.
- **Estado vacío:** ilustración de una campana en gris claro (96 dp, `#94A3B8` al 50 %), el texto "Aún no hay horarios" y debajo "Elige una hora y pulsa *Añadir a la lista*".
- **Indicador de no sincronizado:** los horarios añadidos que todavía no están en el ESP32 llevan un punto amarillo de 8 dp junto a la hora.

### 3.4 Sección 4: sincronización global

- **Barra inferior fija** (no se mueve con el scroll), de fondo blanco y con una sombra hacia arriba (`0 -2 12 rgba(15,23,42,0.08)`).
- **Texto de estado** (caption) sobre el botón: "Última sincronización: hoy 07:02" o, si hay cambios, "3 cambios sin guardar" en azul rey.
- **Botón "Guardar Todo en ESP32":** amarillo brillante a todo el ancho, 56 dp de alto (el más alto de la app, porque es la acción final), radio 16 dp e ícono `sync` (o `system_update_alt`).
- **Estados del botón**

| Estado | Apariencia |
|---|---|
| Normal (hay cambios) | Fondo `#FFD100`, texto `#1E293B`, punto azul de 8 dp a la derecha |
| Presionado | Fondo `#E6BC00`, escala 0.98 |
| Enviando | Ícono reemplazado por un `CircularProgressIndicator` de 20 dp en `#1E293B`, texto "Enviando…", botón bloqueado |
| Éxito | Durante 2 s: ícono `check_circle` y texto "¡Guardado en ESP32!". Snackbar de confirmación |
| Error | Snackbar con fondo `#1E293B`, ícono rojo y el texto "No se pudo enviar. Reintentar" (acción en amarillo) |
| Deshabilitado (sin conexión) | Fondo `#E2E8F0`, texto `#94A3B8`, y el caption cambia a "Conecta el ESP32 para guardar" |

---

## 4. Tabla de especificaciones por componente

| Componente | Dimensiones | Márgenes / padding | Forma y sombra | Colores | Tipografía | Alineación |
|---|---|---|---|---|---|---|
| **Pantalla** | 360 × 800 dp | Margen lateral 16 dp | — | Fondo `#F4F6F9` | — | — |
| **Encabezado** | Ancho total × 184 dp (+ barra de estado) | Padding 24 dp lateral, 20 dp superior, 48 dp inferior (por el solape) | Radio inferior 28 dp, sin sombra | `#0033A0` → `#002270` | — | Contenido a la izquierda |
| **Ícono de identidad** | 72 × 72 dp (campana de 40 dp) | Separación con el título: 16 dp | Círculo, sombra `0 4 12 rgba(0,0,0,0.20)` | Círculo `#FFD100`, campana `#0033A0` | — | Centrado vertical con el bloque de título |
| **Título y subtítulo** | Ancho flexible | 4 dp entre título y subtítulo | — | Blanco y blanco al 80 % | `titulo/app` y `subtitulo/app` | Izquierda |
| **Badge Bluetooth** | Alto 32 dp, ancho según contenido | Padding 12 dp lateral; 6 dp entre ícono y texto; 16 dp sobre el badge | Píldora (radio 16 dp) | Según el estado (§3.1) | `etiqueta/badge` | Izquierda, alineado al texto del título |
| **Tarjeta (general)** | Ancho total − 32 dp | Padding interno 20 dp; separación entre tarjetas 16 dp | Radio 16 dp, borde 1 dp `#E2E8F0`, elevación 2 dp (`0 4 12 rgba(15,23,42,0.08)`) | Fondo `#FFFFFF` | — | — |
| **Tarjeta "Ajustar hora"** | Alto ≈ 248 dp | Margen superior −24 dp (solape) | Igual que la tarjeta general | — | `titulo/tarjeta` | — |
| **Encabezado de tarjeta** | Alto 24 dp | 8 dp entre ícono y texto; 16 dp por debajo | — | Ícono `#0033A0`, texto `#1E293B` | `titulo/tarjeta` | Izquierda (el contador va a la derecha) |
| **Selector de hora** | Ancho total × 112 dp | Padding 16 dp; 16 dp por debajo | Radio 12 dp; borde 2 dp `#0033A0` al enfocarse | Fondo `#F4F6F9` | `display/hora` + `secundario` | Centrado |
| **Botón primario "Añadir"** | Ancho total × 52 dp | Padding 24 dp lateral; 8 dp entre ícono y texto | Radio 12 dp, elevación 1 dp | `#FFD100` / pressed `#E6BC00` / texto `#1E293B` | `etiqueta/boton` | Contenido centrado |
| **Chip contador** | Alto 24 dp, ancho mín. 32 dp | Padding 8 dp lateral | Píldora | Fondo `#E6EBF5`, texto `#0033A0` | 12 sp Bold | Derecha de la cabecera |
| **Fila de horario** | Ancho total × 72 dp | Padding 16 dp lateral (dentro de la tarjeta queda a ras: 0 dp + 16 dp) | Sin radio; *ripple* `#0033A0` al 8 % | Fondo blanco | `hora/lista` + `secundario` | Centrado vertical |
| **Círculo de alarma** | 40 × 40 dp (ícono de 22 dp) | 16 dp a la derecha | Círculo | `#E6EBF5` / ícono `#0033A0` | — | Inicio de la fila |
| **Botón papelera** | Ícono de 24 dp, área táctil 48 × 48 dp | — | *Ripple* circular `#FDECEC` | `#E53E3E` | — | Final de la fila |
| **Divisor** | 1 dp de alto | Sangría izquierda de 72 dp | — | `#E2E8F0` | — | — |
| **Estado vacío** | Alto ≈ 200 dp | Padding vertical 32 dp; 12 dp entre elementos | — | Ilustración `#94A3B8` al 50 % | `cuerpo` + `secundario` | Centrado |
| **Barra inferior** | Ancho total × 104 dp (+ inset de navegación) | Padding 16 dp lateral, 12 dp superior, 16 dp inferior; 8 dp entre caption y botón | Sombra superior `0 -2 12 rgba(15,23,42,0.08)` | Fondo `#FFFFFF` | `caption` | Caption a la izquierda, botón a lo ancho |
| **Botón "Guardar Todo en ESP32"** | Ancho total × 56 dp | Padding 24 dp lateral; 10 dp entre ícono y texto | Radio 16 dp, elevación 3 dp | `#FFD100` (estados en §3.4) | `etiqueta/boton` | Contenido centrado |
| **Snackbar** | Ancho total − 32 dp, alto mín. 48 dp | 16 dp sobre la barra inferior | Radio 8 dp | Fondo `#1E293B`, texto blanco, acción `#FFD100` | 14 sp Regular, acción en Bold | — |
| **Contenido con scroll** | — | Padding inferior = alto de la barra + 16 dp | — | — | — | — |

**Accesibilidad mínima:** todas las áreas táctiles miden al menos 48 × 48 dp, cada ícono-botón lleva su `contentDescription` (p. ej. "Eliminar horario 07:00") y el diseño admite escalado de fuente hasta 130 % sin cortar texto. Por eso las alturas de las filas son mínimas, no fijas.

---

## 5. Tema Android (referencia rápida)

Así se trasladan los tokens a un tema Material 3, válido tanto para XML como para Jetpack Compose:

| Rol Material 3 | Valor |
|---|---|
| `primary` / `onPrimary` | `#0033A0` / `#FFFFFF` |
| `secondary` / `onSecondary` | `#FFD100` / `#1E293B` |
| `background` / `onBackground` | `#F4F6F9` / `#1E293B` |
| `surface` / `onSurface` | `#FFFFFF` / `#1E293B` |
| `onSurfaceVariant` | `#64748B` |
| `outlineVariant` | `#E2E8F0` |
| `error` / `onError` | `#E53E3E` / `#FFFFFF` |

```xml
<!-- res/values/colors.xml -->
<resources>
    <color name="azul_rey">#0033A0</color>
    <color name="azul_oscuro">#002270</color>
    <color name="azul_tinte">#E6EBF5</color>
    <color name="amarillo_calido">#FFD100</color>
    <color name="amarillo_pressed">#E6BC00</color>
    <color name="blanco">#FFFFFF</color>
    <color name="gris_fondo">#F4F6F9</color>
    <color name="texto_oscuro">#1E293B</color>
    <color name="texto_secundario">#64748B</color>
    <color name="divisor">#E2E8F0</color>
    <color name="rojo_suave">#E53E3E</color>
    <color name="rojo_texto">#C53030</color>
    <color name="rojo_tinte">#FDECEC</color>
</resources>
```

```kotlin
// Jetpack Compose
val TimbreColors = lightColorScheme(
    primary = Color(0xFF0033A0), onPrimary = Color.White,
    secondary = Color(0xFFFFD100), onSecondary = Color(0xFF1E293B),
    background = Color(0xFFF4F6F9), onBackground = Color(0xFF1E293B),
    surface = Color.White, onSurface = Color(0xFF1E293B),
    onSurfaceVariant = Color(0xFF64748B), outlineVariant = Color(0xFFE2E8F0),
    error = Color(0xFFE53E3E), onError = Color.White,
)
```

> **¿Usas MIT App Inventor?** La guía también sirve ahí. Usa `VerticalArrangement` blancos como tarjetas sobre un `Screen` de fondo `#F4F6F9`, los mismos Hex en `BackgroundColor` y botones con `Shape = rounded`. Las sombras no se pueden hacer de forma nativa; puedes simularlas con un borde de 1 px `#E2E8F0`.

---

## 6. Iconografía

- **Estilo:** Material Symbols **Rounded**, relleno 0 (*outlined*), grosor 400 y tamaño óptico 24. Las terminaciones redondeadas combinan con los radios de las tarjetas y con Poppins.
- **Excepción:** los íconos **activos o de estado** (Bluetooth conectado, alarma de la lista) van con **relleno 1** para que se lean como "encendidos".
- **Ícono de identidad** (campana): [`assets/ic_timbre.svg`](assets/ic_timbre.svg) es un SVG propio con los colores de la paleta, listo para importar como *Vector Asset* en Android Studio y libre de derechos porque es parte de este proyecto.

| Función | Material Symbols | Equivalente en Tabler Icons |
|---|---|---|
| Identidad de la app | `notifications_active` (o el SVG propio) | `bell-ringing` |
| Bluetooth conectado | `bluetooth_connected` | `bluetooth-connected` |
| Bluetooth desconectado | `bluetooth_disabled` | `bluetooth-off` |
| Bluetooth buscando | `bluetooth_searching` | `bluetooth` (con animación) |
| Seleccionar hora | `schedule` | `clock` |
| Añadir a la lista | `alarm_add` | `clock-plus` |
| Horario guardado | `alarm` | `alarm` |
| Eliminar horario | `delete` | `trash` |
| Guardar en ESP32 | `sync` / `system_update_alt` | `device-floppy` / `refresh` |
| Éxito | `check_circle` | `circle-check` |
| Error | `error` | `alert-circle` |

---

## 7. Recursos gráficos recomendados

**Recomendación general:** en Android usa **vectores (SVG → VectorDrawable)** en lugar de PNG. Se ven nítidos en cualquier densidad, pesan menos y se pueden recolorear con los tokens. Usa PNG transparente solo para ilustraciones complejas, exportándolo en `mdpi`, `hdpi`, `xhdpi`, `xxhdpi` y `xxxhdpi` (1×, 1.5×, 2×, 3× y 4×).

### Íconos

| Recurso | Licencia | Por qué usarlo |
|---|---|---|
| [Material Symbols (Google Fonts Icons)](https://fonts.google.com/icons) | Apache 2.0 | Estándar de Android; está integrado en Android Studio (*New → Vector Asset → Clip Art*) |
| [Tabler Icons](https://tabler.io/icons) | MIT | Más de 5 000 íconos de trazo uniforme; exporta SVG y PNG con color y tamaño a medida |
| [Lucide](https://lucide.dev) | ISC | Estilo limpio y consistente, ideal si buscas algo menos "Google" |
| [Phosphor Icons](https://phosphoricons.com) | MIT | Seis pesos (thin a fill) para jugar con estados activos e inactivos |
| [Iconoir](https://iconoir.com) | MIT | Alternativa minimalista con buen set de dispositivos y tiempo |
| [SVG Repo](https://www.svgrepo.com) | Varía por ícono (muchos CC0/MIT) | Buscador enorme; **revisa la licencia de cada archivo** |

### Ilustraciones

| Recurso | Licencia | Por qué usarlo |
|---|---|---|
| [unDraw](https://undraw.co/illustrations) | Gratis, sin atribución | Eliges el color de acento antes de descargar: pon `#0033A0` y queda alineado a la marca. Útil para el estado vacío y la pantalla de bienvenida |
| [Open Doodles](https://www.opendoodles.com) | CC0 (dominio público) | Ilustraciones dibujadas a mano, de tono escolar y amigable |
| [Humaaans](https://www.humaaans.com) | CC0 | Personajes combinables (estudiantes, docentes) para el onboarding |
| [Storyset (Freepik)](https://storyset.com) | Gratis **con atribución** | Escenas educativas personalizables por color y animables |
| [Pixabay – vectores](https://pixabay.com/vectors/) | Licencia Pixabay (uso libre sin atribución) | Vectores y PNG transparentes de campanas escolares |
| [OpenMoji](https://openmoji.org) | CC BY-SA 4.0 | Emojis vectoriales (🔔 ⏰) si quieres un estilo más lúdico |

### Animaciones y fuentes

| Recurso | Licencia | Uso sugerido |
|---|---|---|
| [LottieFiles](https://lottiefiles.com/free-animations/bell) | Lottie Simple License (las gratuitas) | Campana que vibra al sincronizar con éxito; ondas de búsqueda Bluetooth |
| [Google Fonts – Poppins](https://fonts.google.com/specimen/Poppins) | OFL | Títulos y horas |
| [Google Fonts – Roboto](https://fonts.google.com/specimen/Roboto) | OFL | Texto de interfaz |

> Flaticon e Icons8 tienen material abundante, pero en su versión gratuita **exigen atribución visible** dentro de la app. Si los usas, añade una sección "Créditos" en *Ajustes*.

---

## 8. Microinteracciones (toque final)

| Momento | Animación |
|---|---|
| Añadir horario | La nueva fila entra con *fade + slide* desde arriba (200 ms, `FastOutSlowIn`) y queda resaltada en amarillo al 20 % durante 800 ms |
| Eliminar horario | La fila se colapsa en 180 ms y aparece el Snackbar con DESHACER |
| Conexión Bluetooth | El badge cambia de color con un *crossfade* de 250 ms y el ícono de la campana del encabezado se "balancea" una vez (±12°, 400 ms) |
| Sincronización exitosa | Vibración háptica corta (`HapticFeedbackConstants.CONFIRM`) y check animado en el botón |
| Error | Vibración doble y el botón se sacude horizontalmente (±6 dp, 300 ms) |

Todas las animaciones respetan la opción del sistema "Quitar animaciones" (`Settings.Global.ANIMATOR_DURATION_SCALE = 0`).
