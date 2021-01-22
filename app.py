import logging
import os
import re

import bs4
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from keep_alive import keep_alive

logging.basicConfig(handlers=[logging.FileHandler(encoding='utf-8', filename='bot.log')],
                    level=logging.DEBUG,
                    format=u'%(levelname)s - %(name)s - %(asctime)s: %(message)s')

logger = logging.getLogger(__name__)


def thug_out(update, context):
    params = {"translatetext": ' '.join(context.args)}
    target_url = "http://www.gizoogle.net/textilizer.php"
    resp = requests.post(target_url, data=params)
    soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text)
    try:
        soup = bs4.BeautifulSoup(soup_input, "html")
        giz = soup.find_all(text=True)
        update.message.reply_text(giz[38].strip("\r\n"))
    except:
        soup = bs4.BeautifulSoup(soup_input, "lxml")
        giz = soup.find_all(text=True)
        update.message.reply_text(giz[38].strip("\r\n"))


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Yo! Type anything casual after the command /thugout')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Just type anything normal.')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(os.getenv("telegram_token"), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler(["start", "yo"], start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("thugout", thug_out))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    keep_alive()
    load_dotenv("config.env")
    main()
