import logging
import random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to track user card checks
user_checks = {}

# Function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    welcome_message = f"Welcome, {user_first_name}! 🎉\n\n"
    welcome_message += "Check out our channel: [Your Channel Name](https://t.me/darkdorking)"  # Replace with your channel link
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

# Function to generate random expiry date
def generate_expiry():
    return f"{random.randint(1, 12):02d}/{random.randint(25, 30)}"

# Function to generate random CVV
def generate_cvv():
    return f"{random.randint(100, 999)}"

# Function to handle the .gen command
async def generate_card(update: Update, context: CallbackContext) -> None:
    args = context.args

    # Check if user provided a BIN
    if len(args) > 0:
        bin_number = args[0]
    else:
        await update.message.reply_text("Usage: .gen <bin> (optional: expiry CVV)")
        return

    # Detect expiry date
    expire_date = generate_expiry()
    if len(args) > 1:
        expire_date = args[1]

    # Detect CVV
    cvv = generate_cvv()
    if len(args) > 2:
        cvv = args[2]

    # Generate 10 cards
    cards = []
    for _ in range(10):
        card_number = f"{bin_number}{random.randint(100000000, 999999999)}"
        cards.append(f"💳 **{card_number} | {expire_date} | {cvv}**")

    card_message = "**Generated Cards** 🎴\n\n" + "\n".join(cards)
    
    await update.message.reply_text(card_message, parse_mode="Markdown")

# Function to check card status with limits
async def check_card_with_limit(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    card_number = context.args[0] if len(context.args) > 0 else None

    # Initialize user checks if not present
    if user_id not in user_checks:
        user_checks[user_id] = {"count": 0, "last_checked": datetime.now()}

    # Reset count if a new day
    if (datetime.now() - user_checks[user_id]["last_checked"]).days > 0:
        user_checks[user_id]["count"] = 0
        user_checks[user_id]["last_checked"] = datetime.now()

    # Check if user has reached the limit
    if user_checks[user_id]["count"] < 20:
        if card_number:
            # Simulate checking the card status
            is_live = random.choice([True, False])
            user_checks[user_id]["count"] += 1
            
            status_message = (
                f"Card Status Check! 🔍\n"
                f"**Card Number:** {card_number}\n"
                f"**Status:** {'Live ✅' if is_live else 'Dead ❌'}\n"
            )
            await update.message.reply_text(status_message, parse_mode="Markdown")
        else:
            await update.message.reply_text("Usage: .chk <card_number>")
    else:
        await update.message.reply_text("Daily limit reached! Upgrade to premium membership for more checks.")

# Main function to set up the bot
async def main():
    # Directly set your bot token here
    TOKEN = "8011551620:AAFvDlRL7brL1JF9kEpQJXIVzZf01og4Lc0"  # Replace with your actual bot token
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", generate_card))
    app.add_handler(CommandHandler("chk", check_card_with_limit))

    # Start polling for updates
    await app.run_polling()

# Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
