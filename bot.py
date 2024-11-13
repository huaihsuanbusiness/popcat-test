import logging
from telegram.ext import Updater, CommandHandler
from django.core.wsgi import get_wsgi_application

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamebot.settings')
application = get_wsgi_application()

from game.views import tap_handler
from game.models import Player

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the tap function for Telegram bot
def tap(update, context):
    user = update.message.from_user
    user_id = str(user.id)
    username = user.username

    # Process the tap
    score = tap_handler(user_id, username)

    # Send a message with the updated score
    update.message.reply_text(f"{user.username} tapped! Current score: {score}")

# Error handler for the bot
def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    token = os.getenv('7543064890:AAFYkYx0JHrVwdB_afFR6cjScC1DMLboFhY')  # Use environment variable to store token
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    # Handle the '/tap' command
    dp.add_handler(CommandHandler('tap', tap))

    # Log errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
