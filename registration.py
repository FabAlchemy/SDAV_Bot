from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from datetime import time, date

from data import *
from hello import *


def register(update, context):
    """Handle /register command and display today's activities"""

    if is_known_user(update, context):
        user_id = update.effective_user.id
        user_regs = context.bot_data["users"][user_id]["registrations"]

        if context.bot_data["registrations_open"]:
            day = context.bot_data["date"]
            activities_today = activities[day]

            keyboard = []
            for act in activities_today:
                id = act["id"]
                name = act["name"]
                hour = act["time"].strftime("%Hh%M")
                suffix = "✅" if (id in user_regs) else "❌"
                keyboard.append([InlineKeyboardButton(hour + " : " + name + " " + suffix,
                                                      callback_data=reg_prefix+id)])

            keyboard.append([InlineKeyboardButton(subscribe_validation, callback_data="end")])

            update.message.reply_text(register_question,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            update.message.reply_text("Les inscriptions sont fermées pour aujourd'hui 😥")


def reg_button(update, context):
    """Handle user interaction on registration buttons"""

    user_id = update.effective_user.id
    query = update.callback_query
    choice = query.data[4:]

    keyboard = []
    user_regs = context.bot_data["users"][user_id]["registrations"]

    if choice in user_regs:
        user_regs.remove(choice)
    else:
        user_regs.append(choice)

    day = context.bot_data["date"]
    activities_today = activities[day]
    for act in activities_today:
        id = act["id"]
        name = act["name"]
        hour = act["time"].strftime("%Hh%M")
        suffix = "✅" if (id in user_regs) else "❌"
        keyboard.append([InlineKeyboardButton(hour + " : " + name + " " + suffix,
                                              callback_data=reg_prefix+id)])

    keyboard.append([InlineKeyboardButton(subscribe_validation, callback_data="end")])


    logger.info("[/register] {} registrations updated : {}".format(update.effective_user.id, user_regs))
    query.edit_message_text(register_question, reply_markup=InlineKeyboardMarkup(keyboard))
