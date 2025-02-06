import os
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext

# Retrieve API keys securely
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Fetch Telegram Bot Token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Fetch OpenAI API Key

# Check if API keys are missing
if not BOT_TOKEN or not OPENAI_API_KEY:
    print("❌ ERROR: Missing environment variables (BOT_TOKEN or OPENAI_API_KEY)")
    exit(1)  # Stop execution if keys are missing

openai.api_key = OPENAI_API_KEY  # Set OpenAI key

# Function to analyze essay
def analyze_essay(text):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Provide detailed feedback on this essay:\n\n{text}",
        max_tokens=300
    )
    return response["choices"][0]["text"]

# Function to handle Telegram messages
async def handle_message(update: Update, context: CallbackContext):
    essay_text = update.message.text
    feedback = analyze_essay(essay_text)
    await update.message.reply_text(f"📌 Essay Feedback:\n\n{feedback}")

# Set up the bot
app = Application.builder().token(BOT_TOKEN).build()

# Add message handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start the bot
print("✅ Bot is running...")
app.run_polling()
