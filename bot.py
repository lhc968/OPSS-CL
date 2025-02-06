import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import openai

# Retrieve API keys from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API Key

if not BOT_TOKEN or not OPENAI_API_KEY:
    print("❌ ERROR: Missing environment variables (BOT_TOKEN or OPENAI_API_KEY)")
    exit(1)  # Stop execution if keys are missing

openai.api_key = OPENAI_API_KEY  # Set OpenAI API key

# Function to analyze essay
def analyze_essay(text):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Provide detailed feedback on this essay:\n\n{text}",
        max_tokens=300
    )
    return response["choices"][0]["text"]

# Function to handle Telegram messages
def handle_message(update: Update, context: CallbackContext):
    essay_text = update.message.text
    feedback = analyze_essay(essay_text)
    update.message.reply_text(f"📌 Essay Feedback:\n\n{feedback}")

# Set up and start the bot
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()
