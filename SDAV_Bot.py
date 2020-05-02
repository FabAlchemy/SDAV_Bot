import telegram.bot
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply

from telegram.utils.request import Request
from telegram.ext import messagequeue as mq

from random import choice
from datetime import *

from data import *
from hello import *
from registration import *
from enigms import *
from admin import *
from allo import *
from mysteirb import *

persistence = PicklePersistence(filename='bot_data_pickle')

# Slightly modify the Bot class to use a MessageQueue in order to avoid
# Telegram's flood limits (30 msg/sec)

class MQBot(telegram.bot.Bot):
    """A subclass of Bot which delegates send method handling to MessageQueue"""
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        """Wrapped method would accept new `queued` and `isgroup` OPTIONAL arguments"""
        return super(MQBot, self).send_message(*args, **kwargs)



def button(update, context):
    """Handle user interaction on any button and dispatch accordingly"""

    query = update.callback_query
    payload = query.data
    query.answer() # avoid hogging the client

    if payload == "end":
        query.edit_message_text(validation_subscribe, reply_markup=InlineKeyboardMarkup([]))
    elif payload.startswith("sub_"):
        sub_button(update, context)
    elif payload.startswith("reg_"):
        reg_button(update, context)


def echo(update, context):
    """Handle the /echo command"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=choice(fun_answers))


# Limit global throughput to 25 messages per second
q = mq.MessageQueue(all_burst_limit=25, all_time_limit_ms=1000)
# Set connection pool size for bot
request = Request(con_pool_size=8)

testbot = MQBot(token, request=request, mqueue=q)
updater = telegram.ext.updater.Updater(bot=testbot, persistence=persistence, use_context=True)
dispatcher = updater.dispatcher

cancel_handler = CommandHandler("cancel", cancel)

start_handler = ConversationHandler(
    entry_points = [CommandHandler("start", start),
                    CommandHandler("start_again", update_id)],
    states = {FIRST_NAME: [cancel_handler, MessageHandler(Filters.text, first_name)],
              LAST_NAME:  [cancel_handler, MessageHandler(Filters.text, last_name)],
              MAJOR:      [cancel_handler, MessageHandler(Filters.text, major)],
              PSEUDO:     [cancel_handler, MessageHandler(Filters.text, pseudo)]},
    fallbacks = [cancel_handler],
    name = "start_handler",
    persistent = True)

dispatcher.add_handler(start_handler)


broadcast_handler = ConversationHandler(
    entry_points = [CommandHandler("broadcast", broadcast)],
    states = {CHANNEL:      [cancel_handler, MessageHandler(Filters.text, channel)],
              MESSAGE:      [cancel_handler, MessageHandler(Filters.text, message)],
              CONFIRMATION: [cancel_handler, MessageHandler(Filters.text, confirmation)]},
    fallbacks = [cancel_handler],
    name = "broadcast_handler",
    persistent = True)

dispatcher.add_handler(broadcast_handler)


allo_handler = ConversationHandler(
    entry_points = [CommandHandler("allo", allo)],
    states = {ALLO_TYPE:      [cancel_handler, MessageHandler(Filters.text, allo_type)],
              ALLO_MESSAGE:   [cancel_handler, MessageHandler(Filters.text, allo_message)]},
    fallbacks = [cancel_handler],
    name = "allo_handler",
    persistent = True)

dispatcher.add_handler(allo_handler)


help_handler = ConversationHandler(
    entry_points = [CommandHandler("help", ask_help)],
    states = {HELP_MESSAGE: [cancel_handler, MessageHandler(Filters.text, ask_help_message)]},
    fallbacks = [cancel_handler],
    name = "help_handler",
    persistent = True)

dispatcher.add_handler(help_handler)


mysteirb_handler = ConversationHandler(
    entry_points = [CommandHandler("mysteirb", mysteirb)],
    states = {MYSTEIRB_SUB: [cancel_handler, MessageHandler(Filters.text, mysteirb_sub)]},
    fallbacks = [cancel_handler],
    name = "mysteirb_handler",
    persistent = True)

dispatcher.add_handler(mysteirb_handler)

dispatcher.add_handler(CommandHandler("subscribe", subscribe))
dispatcher.add_handler(CallbackQueryHandler(button))

dispatcher.add_handler(CommandHandler("register", register))
dispatcher.add_handler(CommandHandler("activities", activities_help))

dispatcher.add_handler(CommandHandler("enigms", enigms))
dispatcher.add_handler(CommandHandler("next_enigm", next_enigm))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), answer))
dispatcher.add_handler(CommandHandler("stats", stats))


dispatcher.add_handler(CommandHandler("echo", echo))

# admin
dispatcher.add_handler(CommandHandler("set_day", set_day))
dispatcher.add_handler(CommandHandler("next_day", next_day))
dispatcher.add_handler(CommandHandler("list_users", list_users))
dispatcher.add_handler(CommandHandler("registration_state", registration_state))
dispatcher.add_handler(CommandHandler("set_user_data", set_user_data))

# bd1a
dispatcher.add_handler(CommandHandler("join", join))
dispatcher.add_handler(CommandHandler("list", list))
dispatcher.add_handler(CommandHandler("broadcast", broadcast))
dispatcher.add_handler(CommandHandler("list_mysteirb", list_mysteirb))

updater.start_polling()
updater.idle()
