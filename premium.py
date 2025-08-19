# main.py
import telebot
from telebot import types

# === CONFIG ===
BOT_TOKEN = "8243495375:AAHvEBd6lhs0AjZyOkniDPrQn60apIfvwu4"
FORWARD_CHAT_ID = -1002538002919  # Guruh/kanal ID

# === INIT ===
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# Premium so'rovi bosilgandan keyin chek kutayotgan foydalanuvchilar
awaiting_receipt = set()

# === MATNLAR ===
WELCOME_TEXT = (
    "𝗔𝘀 𝘀𝗮𝗹𝗼𝗺𝘂 𝗮𝗹𝗲𝘆𝗸𝘂𝗺!\n"
    "𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐞𝐚𝐬𝐲  𝐛𝐨𝐭𝐢𝐦𝐢𝐳𝐠𝐚 𝐱𝐮𝐬𝐡 𝐤𝐞𝐥𝐢𝐛𝐬𝐢𝐳‼️"
)

PRICING_TEXT = (
    "\n"
    "𝗡𝗮𝗿𝘅 (𝗨𝗭𝗦):\n"
    "𝟏 𝐨𝐲𝐥𝐢𝐤   𝟒0.𝟎𝟎𝟎𝐔𝐙𝐒\n"
    "𝟏𝟐 𝐨𝐲𝐥𝐢𝐤   𝟐𝟕𝟓.𝟎𝟎𝟎𝐔𝐙𝐒\n"
    "𝟑 𝐨𝐲𝐥𝐢𝐤   𝟏𝟔𝟏.𝟎𝟎𝟎𝐔𝐙𝐒\n"
    "𝟔 𝐨𝐲𝐥𝐢𝐤   𝟐𝟏𝟓.𝟎𝟎𝟎𝐔𝐙𝐒\n"
    "𝟏𝟐 𝐨𝐲𝐥𝐢𝐤   𝟑𝟖𝟓.𝟎𝟎𝟎𝐔𝐙𝐒\n\n"
    "𝘛𝘰'𝘭𝘰𝘷𝘯𝘪 𝘢𝘮𝘢𝘭𝘨𝘢 𝘰𝘴𝘩𝘪𝘳𝘪𝘯𝘨 𝘷𝘢 𝘴𝘩𝘶 𝘻𝘢𝘹𝘰𝘵𝘪 𝘤𝘩𝘦𝘬𝘯𝘪 𝘴𝘩𝘶 𝘺𝘦𝘳𝘨𝘢 𝘺𝘶𝘣𝘰𝘳𝘪𝘯𝘨‼️ \n"
    "𝘊𝘩𝘦𝘬𝘯𝘪 𝘺𝘶𝘣𝘰𝘳𝘨𝘢𝘯𝘪𝘯𝘨𝘪𝘻𝘥𝘢𝘯 𝘴𝘰'𝘯𝘨\n"
    "𝘖𝘱𝘦𝘳𝘢𝘵𝘰𝘳 𝘴𝘪𝘻 𝘣𝘪𝘭𝘢𝘯 𝘣𝘰𝘨'𝘭𝘢𝘯𝘢𝘥𝘪.\n\n"
    "🄺🄰🅁🅃🄰 🅁🄰🅀🄰🄼\n"
    "💳: 4067 0700 0492 6031  A. X"
)

AFTER_FORWARD_REPLY = "𝐓𝐞𝐳 𝐨𝐫𝐚𝐝𝐚 𝐨𝐩𝐞𝐫𝐚𝐭𝐨𝐫 𝐬𝐢𝐳 𝐛𝐢𝐥𝐚𝐧 𝐛𝐨𝐠'𝐥𝐚𝐧𝐚𝐝𝐢‼️"

# === KLAVIATURA ===
def main_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton(
            text=" 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝘀𝗼𝘁𝗶𝗯 𝗼𝗹𝗶𝘀𝗵🌟",
            callback_data="buy_premium"
        )
    )
    return kb

# === HANDLERLAR ===
@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    awaiting_receipt.discard(message.from_user.id)
    bot.send_message(
        message.chat.id,
        WELCOME_TEXT,
        reply_markup=main_keyboard(),
        disable_web_page_preview=True
    )

@bot.callback_query_handler(func=lambda c: c.data == 'buy_premium')
def handle_buy_premium(callback: types.CallbackQuery):
    uid = callback.from_user.id
    awaiting_receipt.add(uid)
    bot.answer_callback_query(callback.id)
    bot.send_message(
        callback.message.chat.id,
        PRICING_TEXT,
        disable_web_page_preview=True
    )

@bot.message_handler(content_types=['photo'])
def handle_photo(message: types.Message):
    uid = message.from_user.id
    if uid not in awaiting_receipt:
        return  # faqat tugmani bosganlardan qabul qilamiz
    try:
        # Rasmning o'zini forward qilish
        bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        # Foydalanuvchi ID sini alohida yuborish
        bot.send_message(FORWARD_CHAT_ID, f"Chek yuborgan foydalanuvchi ID: {uid}")
    except Exception:
        bot.send_message(message.chat.id, "Xabarni yuborishda xatolik. Qayta urinib ko'ring.")
        return
    finally:
        awaiting_receipt.discard(uid)

    bot.reply_to(message, AFTER_FORWARD_REPLY)

# Ba'zi foydalanuvchilar chekni 'document' qilib yuborishi mumkin (pdf/jpg)
@bot.message_handler(content_types=['document'])
def handle_document(message: types.Message):
    uid = message.from_user.id
    if uid not in awaiting_receipt:
        return
    try:
        bot.forward_message(
            chat_id=FORWARD_CHAT_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        bot.send_message(FORWARD_CHAT_ID, f"Chek yuborgan foydalanuvchi ID: {uid}")
    except Exception:
        bot.send_message(message.chat.id, "Xabarni yuborishda xatolik. Qayta urinib ko'ring.")
        return
    finally:
        awaiting_receipt.discard(uid)

    bot.reply_to(message, AFTER_FORWARD_REPLY)

# === RUN ===
if __name__ == "__main__":
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
