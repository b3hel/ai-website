import os
from dotenv import load_dotenv
import ollama

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes


load_dotenv()

TOKEN = os.getenv("TOKEN")


chat_history = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Я AI бот. Напиши щось 😉")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_history[user_id] = []
    await update.message.reply_text("🧹 Пам’ять очищена!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text


    if user_id not in chat_history:
        chat_history[user_id] = []


    chat_history[user_id].append({
        "role": "user",
        "content": user_text
    })

    
    response = ollama.chat(
        model="llama3",
        messages=chat_history[user_id]
    )

    bot_reply = response['message']['content']

    
    chat_history[user_id].append({
        "role": "assistant",
        "content": bot_reply
    })

    await update.message.reply_text(bot_reply)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot is running...")
app.run_polling()