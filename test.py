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
        arduino.write((text + "\n"))  # Aggiunge una nuova riga per simulare la fine del messaggio
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
            simulated_response = "Risposta simulata da Arduino\n"
            arduino.write(simulated_response)  # Scrive la risposta simulata nel buffer

            # Legge i dati dal buffer simulato
            if isinstance(arduino, io.StringIO):  # Controlla se si sta utilizzando un buffer StringIO
                arduino.seek(0)  # Riposiziona il cursore all'inizio del buffer
                data = arduino.read()  # Legge tutto il contenuto del buffer
                arduino.truncate(0)  # Svuota il buffer per prepararlo a nuovi dati
            else:
                # Se non si utilizza un buffer simulato, legge i dati dalla connessione seriale
                if arduino.in_waiting > 0:
                    data = arduino.readline().decode('utf-8').strip()

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
