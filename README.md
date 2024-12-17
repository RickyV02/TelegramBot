
# Arduino + HC-05 Bluetooth + Bot Telegram

Questo progetto permette di controllare un dispositivo Arduino tramite un bot Telegram usando una connessione Bluetooth (HC-05). Il bot Telegram riceve i comandi inviati dall'utente e li inoltra ad Arduino via Bluetooth. Arduino esegue i comandi e risponde, inviando i risultati al bot.

---

## Funzionamento

1. **Bot Telegram**: L'utente invia comandi al bot Telegram.
2. **Python**: Il bot Python riceve i comandi e li inoltra ad Arduino tramite Bluetooth o una simulazione della connessione.
3. **Arduino**: Esegue i comandi ricevuti e risponde tramite il modulo HC-05.

---

## Componenti Necessari

- Arduino (UNO, Mega, ecc.)
- Modulo Bluetooth HC-05
- Computer con Python installato
- Librerie Python:
  ```bash
  pip install pyserial pyTelegramBotAPI python-dotenv
  ```
- Account Telegram per creare il bot.

---

## Schema dei Collegamenti

| HC-05 Pin | Arduino Pin |
|-----------|-------------|
| VCC       | 5V          |
| GND       | GND         |
| TX        | RX (pin 10, con SoftwareSerial) |
| RX        | TX (pin 11, con SoftwareSerial) |

---

## Codice Arduino

Ecco il codice per Arduino da caricare sull' Arduino:

```cpp
#include <SoftwareSerial.h>

SoftwareSerial BTSerial(10, 11); // RX, TX

void setup() {
    Serial.begin(9600);         // Comunicazione con il computer
    BTSerial.begin(9600);       // Comunicazione con HC-05
    pinMode(13, OUTPUT);        // LED su pin 13
}

void loop() {
    // Legge comandi dal modulo HC-05
    if (BTSerial.available()) {
        String command = BTSerial.readStringUntil('
');
        Serial.println("Comando ricevuto: " + command);

        // Esegue azioni in base al comando
        if (command == "ACCENDI LED") {
            digitalWrite(13, HIGH);
            BTSerial.println("LED acceso!");
        } else if (command == "SPEGNI LED") {
            digitalWrite(13, LOW);
            BTSerial.println("LED spento!");
        } else {
            BTSerial.println("Comando non riconosciuto.");
        }
    }
}
```

---

## Configurazione del Bot Telegram

1. Crea un nuovo bot su Telegram usando `@BotFather`.
2. Copia il token del bot e inseriscilo nel file Python.

---

## Configurazione dell'Ambiente

1. Crea un file `.env` nella stessa cartella del progetto.
2. Aggiungi le seguenti variabili nel file `.env`:

   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   CHAT_ID=your_chat_id_here
   ```

   - Sostituisci `your_bot_token_here` con il token del bot Telegram che hai ricevuto da BotFather.
   - Sostituisci `your_chat_id_here` con il tuo **chat ID** che puoi ottenere usando un bot come `userinfobot`.

---

## Codice Python

Ecco il codice Python aggiornato che gestisce la comunicazione tra il bot Telegram e Arduino (via Bluetooth o simulato):

```python
import io
import telebot
import threading
import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN:
    raise ValueError("Token non trovato nel file .env!")
if not CHAT_ID:
    raise ValueError("Chat ID non trovato nel file .env!")

bot = telebot.TeleBot(TOKEN)

# Simula la connessione seriale utilizzando un buffer in memoria
# Questo consente di emulare il comportamento di una connessione seriale con Arduino.
arduino = io.StringIO()

# Funzione per gestire i messaggi ricevuti dal bot Telegram
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id  # Identifica la chat da cui proviene il messaggio
    text = message.text  # Contenuto del messaggio ricevuto

    # Scrive il messaggio ricevuto nel buffer simulato che rappresenta Arduino
    try:
        arduino.write((text + "
"))  # Aggiunge una nuova riga per simulare la fine del messaggio
        print(f"Messaggio simulato ad Arduino: {text}")  # Stampa per scopi di debug
        bot.send_message(chat_id, f"Messaggio inviato ad Arduino: {text}")  # Conferma l'invio al mittente
    except Exception as e:
        # Gestisce eventuali errori durante l'invio del messaggio al buffer simulato
        bot.send_message(chat_id, f"Errore nell'invio: {str(e)}")

# Funzione per simulare la lettura di risposte da Arduino
def read_from_arduino():
    while True:
        try:
            # Simula una risposta predefinita generata da Arduino
            simulated_response = "Risposta simulata da Arduino
"
            arduino.write(simulated_response)  # Scrive la risposta simulata nel buffer

            # Legge i dati dal buffer simulato
            if isinstance(arduino, io.StringIO):  # Controlla se si sta utilizzando un buffer StringIO
                arduino.seek(0)  # Riposiziona il cursore all'inizio del buffer
                data = arduino.read()  # Legge tutto il contenuto del buffer
                arduino.truncate(0)  # Svuota il buffer per prepararlo a nuovi dati

            # Se vengono trovati dati validi, invia la risposta tramite Telegram
            if data:
                print(f"Dati simulati da Arduino: {data}")  # Stampa per scopi di debug
                bot.send_message(CHAT_ID, f"Risposta da Arduino: {data}")
        except Exception as e:
            # Gestisce eventuali errori durante la lettura dei dati dal buffer o dalla seriale
            print(f"Errore nella lettura da Arduino: {e}")

# Avvia un thread separato per leggere dati da Arduino simulato
thread = threading.Thread(target=read_from_arduino, daemon=True)
thread.start()

# Avvia il bot Telegram per ricevere e gestire messaggi
print("Bot Telegram in esecuzione (simulazione seriale)...")
bot.polling()
```

---

## Esecuzione

1. Carica il codice **Arduino** sull'Arduino.
2. Configura il file Python (`app.py`) per gestire la comunicazione tra il bot Telegram e Arduino.
3. Esegui il programma Python con il comando:

   ```bash
   python app.py
   ```

4. Interagisci con il bot Telegram inviando comandi come `ACCENDI LED` e `SPEGNI LED`.

---

## Note

- Testa il modulo **HC-05** con un'app terminale Bluetooth prima di connetterlo al programma Python.
- Assicurati che il **baud rate** sia corretto per la comunicazione seriale.
- In caso di errore, verifica la configurazione del file `.env` e assicurati che il **chat ID** sia correttamente configurato.

---
