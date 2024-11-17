from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import random

# User balances stored in memory (for simplicity)
user_balances = {}

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    if user not in user_balances:
        user_balances[user] = 100  # Start with 100 fake coins
    await update.message.reply_text(f"Welcome, {user}! You have {user_balances[user]} coins.")

async def balance(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    balance = user_balances.get(user, 0)
    await update.message.reply_text(f"Your balance: {balance} coins.")

async def earn(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    coins_earned = random.randint(10, 50)
    user_balances[user] += coins_earned
    await update.message.reply_text(f"You earned {coins_earned} coins! Your new balance is {user_balances[user]}.")

async def send(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user.username
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /send [username] [amount]")
        return
    recipient, amount = context.args
    amount = int(amount)
    if user_balances.get(user, 0) >= amount:
        user_balances[user] -= amount
        user_balances[recipient] = user_balances.get(recipient, 0) + amount
        await update.message.reply_text(f"Sent {amount} coins to {recipient}. Your new balance is {user_balances[user]}.")
    else:
        await update.message.reply_text("Insufficient balance!")

def main():
    # Replace 'YOUR_TELEGRAM_API_TOKEN' with your actual bot token
    application = Application.builder().token("7265456799:AAH7bfyZcBaNGDTPAFYJAonojtYceiXUzH8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("earn", earn))
    application.add_handler(CommandHandler("send", send))

    application.run_polling()

if __name__ == '__main__':
    main()
