import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import ChatMember
import logging

# Enable logging to see if there are any issues
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch the bot token from environment variables
TOKEN = os.getenv('BOT_TOKEN')  # This will get the token from Vercel's environment variables

if not TOKEN:
    logger.error("Bot token is missing!")
    exit()

# Function to check if the user is an admin in the group
def is_admin(update: Update) -> bool:
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    chat_member = update.message.bot.get_chat_member(chat_id, user_id)
    
    return chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.CREATOR]

# Command to start the quiz (only accessible to admins)
def start_quiz(update: Update, context: CallbackContext):
    if is_admin(update):
        update.message.reply_text("Starting the quiz!")
        # Add logic to start the quiz here
    else:
        update.message.reply_text("You must be an admin to start the quiz.")

# Command to stop the quiz (only accessible to admins)
def stop_quiz(update: Update, context: CallbackContext):
    if is_admin(update):
        update.message.reply_text("Stopping the quiz!")
        # Add logic to stop the quiz here
    else:
        update.message.reply_text("You must be an admin to stop the quiz.")

# Command to add a question (only accessible to admins)
def add_question(update: Update, context: CallbackContext):
    if is_admin(update):
        question_text = " ".join(context.args)  # Capture the question from the command
        if question_text:
            update.message.reply_text(f"Question added: {question_text}")
            # Add logic to store the question
        else:
            update.message.reply_text("Please provide a question.")
    else:
        update.message.reply_text("You must be an admin to add questions.")

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers for each command
    dispatcher.add_handler(CommandHandler("startquiz", start_quiz))
    dispatcher.add_handler(CommandHandler("stopquiz", stop_quiz))
    dispatcher.add_handler(CommandHandler("addquestion", add_question))

    # Start polling to receive updates
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
