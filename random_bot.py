import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "8011551620:AAFvDlRL7brL1JF9kEpQJXIVzZf01og4Lc0"  # Yaha apna Telegram Bot Token daalo

# Luhn Algorithm for Valid CC
def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    checksum = 0
    even = False

    for d in reversed(digits):
        if even:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
        even = not even

    return checksum % 10

# CC Generator Function
def generate_credit_card(bin_number, quantity=5):
    generated_cards = []
    
    for _ in range(quantity):
        card_number = str(bin_number) + ''.join(str(random.randint(0, 9)) for _ in range(15 - len(str(bin_number))))
        check_digit = (10 - luhn_checksum(card_number + "0")) % 10
        final_card_number = card_number + str(check_digit)

        expiry_month = str(random.randint(1, 12)).zfill(2)
        expiry_year = str(random.randint(25, 30))  # Expiry between 2025-2030
        cvv = str(random.randint(100, 999))

        generated_cards.append(f"{final_card_number} | {expiry_month}/{expiry_year} | {cvv}")
    
    return "\n".join(generated_cards)

# Telegram Command Handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send /ccgen <BIN> to generate credit cards.")

def ccgen(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 1 and context.args[0].isdigit() and len(context.args[0]) == 6:
        bin_input = context.args[0]
        cc_list = generate_credit_card(bin_input)
        update.message.reply_text(f"Generated Credit Cards:\n{cc_list}")
    else:
        update.message.reply_text("Invalid command! Use: /ccgen <6-digit BIN>")

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ccgen", ccgen))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
