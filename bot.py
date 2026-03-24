import telebot
import sqlite3

TOKEN = "8510315469:AAE_zMEIM_hKH6ARZuOrTJXTaHGFX8fy7RU"
ADMIN_ID = 8456405557   # apni telegram id

bot = telebot.TeleBot(TOKEN)

# ===== DATABASE =====
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)")
conn.commit()

def save_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
    conn.commit()

# ===== START =====
@bot.message_handler(commands=['start'])
def start_msg(message):
    user_id = message.chat.id
    save_user(user_id)
    bot.send_message(message.chat.id, "Hello")

# ===== ADMIN REPLY → USER =====
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID)
def admin_reply(message):
    try:
        user_id, msg = message.text.split(" ", 1)
        bot.send_message(int(user_id), msg)
    except:
        bot.send_message(ADMIN_ID, "Format: USERID message")

# ===== USER MESSAGE → ADMIN =====
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def all_messages(message):
    user_id = message.chat.id
    msg_text = message.text if message.text else "Media message"
    text = f"USER_ID: {user_id}\n\n{msg_text}"
    bot.send_message(ADMIN_ID, text)

print("Bot Running...")
bot.infinity_polling()
