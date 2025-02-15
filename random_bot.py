import logging
import random
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to track user card checks
user_checks = {}

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    welcome_message = f"Welcome, {user_first_name}! 🎉\n\n"
    welcome_message += "Check out our channel: [Your Channel Name](https://t.me/darkdorking)"  # Replace with your channel link
    update.message.reply_text(welcome_message, parse_mode='Markdown')

# Function to handle the .gen command
def generate_card(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 2:
        bin_number = context.args[0]  # Get the BIN from the command
        expire_date = context.args[1]  # Get the expiration date from the command
        
        # Generate a random card number (for demonstration purposes)
        card_number = f"{bin_number}{random.randint(100000000, 999999999)}"
        
        # Create a card message
        card_message = (
            f"Card Generated! 🎴\n"
            f"**Card Number:** {card_number}\n"
            f"**Expiration Date:** {expire_date}\n"
            f"**BIN:** {bin_number}\n"
        )
        
        update.message.reply_text(card_message, parse_mode='Markdown')
    else:
        update.message.reply_text("Usage: .gen <bin> <expire_date>")

# Function to check card status with limits
def check_card_with_limit(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    card_number = context.args[0] if len(context.args) > 0 else None

    # Initialize user checks if not present
    if user_id not in user_checks:
        user_checks[user_id] = {'count': 0, 'last_checked': datetime.now()}

    # Reset count if a new day
    if (datetime.now() - user_checks[user_id]['last_checked']).days > 0:
        user_checks[user_id]['count'] = 0
        user_checks[user_id]['last_checked'] = datetime.now()

    # Check if user has reached the limit
    if user_checks[user_id]['count'] < 20:
        if card_number:
            # Simulate checking the card status
            is_live = random.choice([True, False])
            user_checks[user_id]['count'] += 1
            
            status_message = (
                f"Card Status Check! 🔍\n"
                f"**Card Number:** {card_number}\n"
                f"**Status:** {'Live' if is_live else 'Dead'}\n"
            )
            update.message.reply_text(status_message, parse_mode='Markdown')
        else:
            update.message.reply_text("Usage: .chk <card_number>")
    else:
        update.message.reply_text("Daily limit reached! Upgrade to premium membership for more checks.")

# Main function to set up the bot
def main():
    # Directly set your bot token here
    token = "7695368751:AAFVrzejlS0BLKZD7Bb1HXXgWl5PGclex_0"  # Replace with your actual bot token
    updater = Updater(token)  # Add your bot token here
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("gen", generate_card))
    dispatcher.add_handler(CommandHandler("chk", check_card_with_limit))  # Updated check command

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
