/*
  Timbre Escolar - ESP32 (Bluetooth clásico)
  Recibe los horarios desde la app de MIT App Inventor y activa un relé
  a cada hora programada.

  Mensajes que envía la app (una línea por mensaje, terminada en \n):
    HORA=2026-10-03 07:30:00       -> ajusta el reloj del ESP32
    HORARIOS=07:00,09:15,12:30     -> reemplaza la lista de horarios
    PROBAR                         -> hace sonar el timbre una vez

  Requisitos: un ESP32 "clásico" (ESP32-WROOM / DevKit). Los modelos
  ESP32-S2, S3, C3 y C6 NO tienen Bluetooth clásico.
*/
#include <BluetoothSerial.h>
#include <Preferences.h>
#include <sys/time.h>
#include <time.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error "Este ESP32 no tiene Bluetooth clásico. Usa un ESP32 original (WROOM/DevKit)."
#endif

// ----------------------------------------------------------- configuración
const char *NOMBRE_BT = "ESP32-Timbre";       // nombre que verás en el teléfono
const int PIN_RELE = 26;                      // pin conectado al módulo relé
const bool RELE_ACTIVO_ALTO = true;           // false si tu relé se activa con LOW
const unsigned long DURACION_TIMBRE_MS = 5000; // cuánto suena el timbre
const int PIN_LED = 2;                        // LED integrado: encendido = hora sincronizada
const int MAX_HORARIOS = 40;

// ---------------------------------------------------------------- estado
BluetoothSerial SerialBT;
Preferences prefs;

int horarios[MAX_HORARIOS];  // minutos desde medianoche (07:30 -> 450)
int totalHorarios = 0;
bool horaSincronizada = false;
String linea;
int ultimoMinutoRevisado = -1;
bool sonando = false;
unsigned long inicioTimbre = 0;

void rele(bool encendido) {
  digitalWrite(PIN_RELE, (encendido == RELE_ACTIVO_ALTO) ? HIGH : LOW);
}

void sonarTimbre() {
  rele(true);
  sonando = true;
  inicioTimbre = millis();
  Serial.println("Timbre sonando");
}

void cargarHorarios(const String &lista) {
  totalHorarios = 0;
  int inicio = 0;
  while (inicio < (int)lista.length() && totalHorarios < MAX_HORARIOS) {
    int coma = lista.indexOf(',', inicio);
    if (coma < 0) coma = lista.length();
    String item = lista.substring(inicio, coma);
    item.trim();
    int hh, mm;
    if (sscanf(item.c_str(), "%d:%d", &hh, &mm) == 2 && hh >= 0 && hh < 24 && mm >= 0 && mm < 60) {
      horarios[totalHorarios++] = hh * 60 + mm;
    }
    inicio = coma + 1;
  }
  Serial.printf("Horarios cargados: %d\n", totalHorarios);
}

bool ajustarHora(const String &texto) {
  struct tm t = {};
  if (sscanf(texto.c_str(), "%d-%d-%d %d:%d:%d", &t.tm_year, &t.tm_mon, &t.tm_mday,
             &t.tm_hour, &t.tm_min, &t.tm_sec) != 6) {
    return false;
  }
  t.tm_year -= 1900;
  t.tm_mon -= 1;
  t.tm_isdst = 0;
  struct timeval tv = {mktime(&t), 0};
  settimeofday(&tv, nullptr);
  horaSincronizada = true;
  ultimoMinutoRevisado = t.tm_hour * 60 + t.tm_min;  // no sonar por el minuto en curso
  digitalWrite(PIN_LED, HIGH);
  return true;
}

void procesarLinea(String msg) {
  msg.trim();
  if (msg.startsWith("HORA=")) {
    bool ok = ajustarHora(msg.substring(5));
    SerialBT.println(ok ? "OK HORA" : "ERROR HORA");
  } else if (msg.startsWith("HORARIOS=")) {
    String lista = msg.substring(9);
    prefs.putString("horarios", lista);  // se conserva aunque se apague
    cargarHorarios(lista);
    SerialBT.printf("OK %d HORARIOS\n", totalHorarios);
  } else if (msg == "PROBAR") {
    sonarTimbre();
    SerialBT.println("OK PROBAR");
  }
  Serial.println("Recibido: " + msg);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_RELE, OUTPUT);
  pinMode(PIN_LED, OUTPUT);
  rele(false);
  digitalWrite(PIN_LED, LOW);

  prefs.begin("timbre", false);
  cargarHorarios(prefs.getString("horarios", ""));

  SerialBT.begin(NOMBRE_BT);
  Serial.printf("Bluetooth listo como \"%s\"\n", NOMBRE_BT);
}

void loop() {
  // 1) Leer mensajes de la app
  while (SerialBT.available()) {
    char c = SerialBT.read();
    if (c == '\n') {
      procesarLinea(linea);
      linea = "";
    } else if (c != '\r' && linea.length() < 600) {
      linea += c;
    }
  }

  // 2) Revisar si toca sonar (una vez por minuto)
  if (horaSincronizada) {
    time_t ahora = time(nullptr);
    struct tm t;
    localtime_r(&ahora, &t);
    int minuto = t.tm_hour * 60 + t.tm_min;
    if (minuto != ultimoMinutoRevisado) {
      ultimoMinutoRevisado = minuto;
      for (int i = 0; i < totalHorarios; i++) {
        if (horarios[i] == minuto) {
          sonarTimbre();
          break;
        }
      }
    }
  }

  // 3) Apagar el timbre cuando pase la duración
  if (sonando && millis() - inicioTimbre >= DURACION_TIMBRE_MS) {
    rele(false);
    sonando = false;
  }

  delay(20);
}
