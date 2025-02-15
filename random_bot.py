import logging
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to track user card checks
user_checks = {}

# Function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    welcome_message = (
        f"Welcome, {user_first_name}! 🎉\n\n"
        "Check out our channel: [Your Channel Name](https://t.me/darkdorking)"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

# Function to handle the .gen command
async def generate_card(update: Update, context: CallbackContext) -> None:
    if context.args and len(context.args) == 2:
        bin_number = context.args[0]  # Get the BIN from the command
        expire_date = context.args[1]  # Get the expiration date from the command
        
        # Generate a random card number (for demonstration purposes)
        card_number = f"{bin_number}{random.randint(100000000, 999999999)}"
        
        card_message = (
            f"Card Generated! 🎴\n"
            f"**Card Number:** {card_number}\n"
            f"**Expiration Date:** {expire_date}\n"
            f"**BIN:** {bin_number}\n"
        )
        await update.message.reply_text(card_message, parse_mode='Markdown')
    else:
        await update.message.reply_text("Usage: /gen <bin> <expire_date>")

# Function to check card status with limits
async def check_card_with_limit(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    card_number = context.args[0] if context.args else None

    if not card_number:
        await update.message.reply_text("Usage: /chk <card_number>")
        return

    if user_id not in user_checks:
        user_checks[user_id] = {'count': 0, 'last_checked': datetime.now()}

    if (datetime.now() - user_checks[user_id]['last_checked']).days > 0:
        user_checks[user_id]['count'] = 0
        user_checks[user_id]['last_checked'] = datetime.now()

    if user_checks[user_id]['count'] < 20:
        is_live = random.choice([True, False])
        user_checks[user_id]['count'] += 1
        
        status_message = (
            f"Card Status Check! 🔍\n"
            f"**Card Number:** {card_number}\n"
            f"**Status:** {'Live' if is_live else 'Dead'}\n"
        )
        await update.message.reply_text(status_message, parse_mode='Markdown')
    else:
        await update.message.reply_text("Daily limit reached! Upgrade to premium membership for more checks.")

# Async main function
async def main():
    TOKEN = "8011551620:AAFvDlRL7brL1JF9kEpQJXIVzZf01og4Lc0"  # Replace with your actual bot token
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", generate_card))
    app.add_handler(CommandHandler("chk", check_card_with_limit))

    print("Bot is running...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
