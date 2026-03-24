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
    bot.send_message(message.chat.id, "Hello 👋 Support se connect ho gaye ho")

# ===== USER MESSAGE → ADMIN =====
@bot.message_handler(func=lambda m: m.chat.id != ADMIN_ID)
def user_message(message):
    user_id = message.chat.id
    save_user(user_id)

    text = f"USER_ID: {user_id}\n\n{message.text}"
    bot.send_message(ADMIN_ID, text)

# ===== ADMIN REPLY → USER =====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID)
def admin_reply(message):
    try:
        user_id, msg = message.text.split(" ", 1)
        bot.send_message(int(user_id), msg)
    except:
        bot.send_message(ADMIN_ID, "Format sahi likho:\nUSERID message")

print("Bot Running...")
bot.infinity_polling()
