import os
import serial
import telebot
import threading
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

# Configurazione connessione Bluetooth
bluetooth_port = "COM3"
baud_rate = 9600
arduino = serial.Serial(bluetooth_port, baud_rate, timeout=1)

# Funzione per gestire i comandi ricevuti dal bot Telegram
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.lower().strip()  # Converti in minuscolo per evitare problemi con il testo

    if text in ["accendi luce", "spegni luce", "accendi ventola", "spegni ventola"]:
        try:
            # Invia il comando ad Arduino tramite la connessione Bluetooth
            arduino.write((text + "\n").encode('utf-8'))
            bot.send_message(chat_id, f"Comando inviato ad Arduino: {text}")
        except Exception as e:
            bot.send_message(chat_id, f"Errore nell'invio del comando: {str(e)}")
    else:
        bot.send_message(chat_id, "Comando non riconosciuto. Usa:\n- accendi luce\n- spegni luce\n- accendi ventola\n- spegni ventola")

# Funzione per leggere i dati da Arduino e inviarli a Telegram
def read_from_arduino():
    while True:
        try:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode('utf-8').strip()
                print(f"Messaggio da Arduino: {data}")  # Debug in console
                bot.send_message(CHAT_ID, f"Risposta da Arduino: {data}")
        except Exception as e:
            print(f"Errore nella lettura da Arduino: {e}")

# Avvia un thread separato per leggere continuamente i dati da Arduino
thread = threading.Thread(target=read_from_arduino, daemon=True)
thread.start()

# Avvia il bot Telegram
print("Bot Telegram in esecuzione...")
bot.polling()
