import telegram.bot
from telegram.ext import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from data import *
from copy import deepcopy
from pprint import pformat

from datetime import date

import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


def user_id_str(user_data):
    """Pretty print a user information"""

    try:
        return "{} {} ({}) {}".format(user_data["first_name"],
                                      user_data["last_name"],
                                      user_data["pseudo"],
                                      user_data["major"][-1])
    except: # the user aborted the /start process and data is missing...
        return user_data["name"]


def start(update, context):
    """Register the user in the database"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Handle mulitple /start and the very first user
    if "users" in context.bot_data:
        if user_id not in context.bot_data["users"]:
            logger.info("[/start] New user registering")
            context.bot_data["users"][user_id] = deepcopy(empty_user)
        else:
            context.bot.send_message(chat_id=chat_id, text=already_started)
            return ConversationHandler.END
    else: # the first user issued /start, we init the server "database"
        logger.info("[/start] First user registered")
        context.bot_data["users"] = {user_id: deepcopy(empty_user)}
        context.bot_data["date"] = date.today().day
        context.bot_data["registrations_open"] = True

    # Send greetings and ask the first name
    context.bot.send_message(chat_id=chat_id, text=intro)
    context.bot_data["users"][user_id]["name"] = update.effective_user.name
    context.user_data["enigms"] = deepcopy(empty_enigm_tracker)
    update_id(update, context, first_time=True)
    return FIRST_NAME


def is_known_user(update, context):

    user_id = update.effective_user.id
    if user_id in context.bot_data["users"]:
        return True
    else:
        context.bot.send_message(chat_id=user_id, text="Tu n'es pas enregistré, commence par /start 😃")
        return False


def update_id(update, context, first_time=False):
    """Handle the /start_again command"""
    update.message.reply_text(ask_data + ("\n"+inform_cancel if not first_time else ""))
    update.message.reply_text(ask[FIRST_NAME])

    return FIRST_NAME


def cancel(update, context):
    """Cancel current Conversation"""

    update.message.reply_text(success_cancel, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def first_name(update, context):
    """Register the first name and ask for the last name"""

    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return FIRST_NAME

    context.bot_data["users"][user_id]["first_name"] = user_input
    update.message.reply_text(ask[LAST_NAME])

    return LAST_NAME


def last_name(update, context):
    """Register the last name and ask for the major with a specific keyboard"""

    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return LAST_NAME


    context.bot_data["users"][user_id]["last_name"] = user_input

    keyboard = [[KeyboardButton(maj)] for maj in majors]
    update.message.reply_text(ask[MAJOR],
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

    return MAJOR


def major(update, context):
    """Receive the major and check correctness, ask for pseudo"""

    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip()

    if user_input not in majors:
        update.message.reply_text(invalid_input)
        return MAJOR

    context.bot_data["users"][user_id]["major"] = user_input
    update.message.reply_text(ask[PSEUDO])

    return PSEUDO


def pseudo(update, context):
    """Receive the pseudo and move on to more interesting things"""

    user_id = update.effective_user.id
    user_input = update.message.text[:30].strip().replace("\n", " ")

    if user_input == "":
        update.message.reply_text(invalid_input)
        return PSEUDO

    context.bot_data["users"][user_id]["pseudo"] = user_input
    update.message.reply_text(ask[END], reply_markup=ReplyKeyboardRemove())

    user_str = user_id_str(context.bot_data["users"][user_id])
    update.message.reply_text(recap_data + " \n" + user_str + "\n" + incorrect_data)

    update.message.reply_text(finish_start)

    logger.info("[/start] User {} updated its data : {}".format(user_id, user_str))
    logger.info("[/start] Current users :\n" + pformat(context.bot_data["users"]))
    return ConversationHandler.END



def subscribe(update, context):
    """Handle the /subscribe command"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_subs = context.bot_data["users"][user_id]["subscriptions"]

    keyboard = []
    for sub in subscriptions:
        suffix = "✅" if (sub in user_subs) else "❌"
        keyboard.append([InlineKeyboardButton(subscriptions_names[sub] + " " + suffix,
                        callback_data=sub_prefix + sub)])

    keyboard.append([InlineKeyboardButton(subscribe_validation, callback_data="end")])

    context.bot.send_message(chat_id=chat_id, text=ask[SUBSCRIBE],
                             reply_markup=InlineKeyboardMarkup(keyboard))


def sub_button(update, context):
    """Handle user interaction on subscription buttons"""

    user_id = update.effective_user.id
    query = update.callback_query
    choice = query.data[4:]

    keyboard = []
    user_subs = context.bot_data["users"][user_id]["subscriptions"]

    if choice in user_subs:
        user_subs.remove(choice)
    else:
        user_subs.append(choice)

    for sub in subscriptions: # WARNING: code duplication
        suffix = "✅" if (sub in user_subs) else "❌"
        keyboard.append([InlineKeyboardButton(subscriptions_names[sub] + " " + suffix,
                                              callback_data=sub_prefix + sub)])
    keyboard.append([InlineKeyboardButton(subscribe_validation, callback_data="end")])

    logger.info("[/subscribe] {} subscriptions updated : {}".format(update.effective_user.id, user_subs))
    query.edit_message_text(ask[SUBSCRIBE], reply_markup=InlineKeyboardMarkup(keyboard))



def activities_help(update, context):
    """Handle /activities and send the links"""

    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=tutos)



HELP_MESSAGE = 42

def ask_help(update, context):
    """Handle the /help command and ask for the problem"""

    user_id = update.effective_user.id
    user_data = context.bot_data["users"][user_id]

    update.message.reply_text("Désolé de te causer des problèmes... 😓\nDis-moi ce qu'il se passe exactement ?")

    return HELP_MESSAGE


def ask_help_message(update, context):
    """Transfer help message to the correct channel"""

    user_id = update.effective_user.id

    if user_id in context.bot_data["users"]:
        user_data = context.bot_data["users"][user_id]
    else:
        user_data = {"name": update.effective_user.name}

    formatted_help_msg = "{}, {} a un problème avec moi 😅\n\n{}".format(update.effective_user.name, user_id_str(user_data), update.message.text[:3800])
    logger.info("[/help] {}".format(formatted_help_msg))
    context.bot.send_message(chat_id=assist_chat, text=formatted_help_msg)
    update.message.reply_text("J'ai transmis tes doléances")

    return ConversationHandler.END
