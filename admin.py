from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from datetime import time, date

from data import *
from hello import *


def set_day(update, context):
    """Set current day manually"""

    user_id = update.effective_user.id

    if user_id in admins:
        try:
            day = int(context.args[0])
            context.bot_data["date"] = day
            update.message.reply_text(update_day_finished.format(context.bot_data["date"]))

        except:
            update.message.reply_text("Syntaxe : /set_day [day]")

    else:
        update.message.reply_text("Petit curieux 😅")


def next_day(update, context):
    """Move on to the next day and alert users subscribed to `dailies` and `enigms`"""

    user_id = update.effective_user.id
    target = "".join(context.args).lower()

    if user_id in admins:
        context.bot_data["date"] = context.bot_data["date"] + 1

        users = context.bot_data["users"]
        for usr in users:
            if ("dailies" in users[usr]["subscriptions"]):
                context.bot.send_message(chat_id=usr, text=next_day_dailies)
            if ("enigms" in users[usr]["subscriptions"]):
                context.bot.send_message(chat_id=usr, text=next_day_enigms)

        update.message.reply_text(update_day_finished.format(context.bot_data["date"]))

    else:
        update.message.reply_text("Petit curieux 😅")


def list_mysteirb(update, context):
    """List the users with a `mysteirb` data"""

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if user_id in bd1a:
        users = context.bot_data["users"]

        msg = ""
        rank = 1
        for usr in users:
            if "mysteirb" in users[usr]:
                msg += "- " + users[usr]["mysteirb"] + " : " + user_id_str(users[usr]) + "\n"
                rank += 1

            if rank % 10 == 0 and msg != "":
                context.bot.send_message(chat_id=chat_id, text=msg)
                msg = ""

        if rank % 10 != 0 and msg != "":
            context.bot.send_message(chat_id=chat_id, text=msg)

    else:
        update.message.reply_text("Petit curieux 😅")


def set_user_data(update, context):
    """Force user data to a certain value."""

    user_id = update.effective_user.id
    target = "".join(context.args).lower()

    if user_id in admins:
        target_user = int(context.args[0])
        target_key = context.args[1]
        target_value = context.args[2]

        users = context.bot_data["users"]

        if target_user in users:
            if target_key == "time":
                if int(target_value) in users:
                    users[target_user]["enigm_data"]["time"] = users[int(target_value)]["enigm_data"]["time"]
                    update.message.reply_text("Done")

            elif target_key in ['first_name', 'last_name', 'pseudo']:
                users[target_user][target_key] = context.args[2]
                update.message.reply_text("Done")

            else:
                update.message.reply_text("Bad target_key")
    else:
        update.message.reply_text("Petit curieux 😅")


def registration_state(update, context):
    """Switch registration_state for everyone"""

    user_id = update.effective_user.id
    if user_id in admins:
        context.bot_data["registrations_open"] = (not context.bot_data["registrations_open"])

        logger.info("Changed registrations state : {}".format(context.bot_data["registrations_open"]))
        update.message.reply_text("Etat des inscriptions changé : {}".format(context.bot_data["registrations_open"]))

    else:
        update.message.reply_text("Petit curieux 😅")


def join(update, context):
    """Display the user informations in the console"""

    chat_id = update.effective_chat.id
    user = update.effective_user

    logger.info("[/join] user {} ({}) issued a /join command (chat: {})".format(user.name, user.id, chat_id))


def list(update, context):
    """Get the users lists for the current day"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id in bd1a:
        users = context.bot_data["users"]
        day = context.bot_data["date"]
        activities_today = activities[day]

        for act in activities_today:
            msg = "--- " + act["name"] + " " + str(act["time"]) + " ---\n\n"
            i = 1
            for usr in users:
                if (act["id"] in users[usr]["registrations"]):
                    msg += str(i) + ". " + user_id_str(users[usr]) + "\n"
                    i += 1

            context.bot.send_message(chat_id=chat_id, text=msg)

    else:
        update.message.reply_text("Petit curieux 😅")


from pprint import pformat

def list_users(update, context):
    """Get the users lists for the current day"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id in admins:
        users = context.bot_data["users"]
        logger.info("[/list_users] Current users :\n" + pformat(context.bot_data["users"]))

        msg = ""
        rank = 1
        for usr in users:
            msg += str(rank) + ". " + str(usr) + " " + users[usr]["name"] + " : " + user_id_str(users[usr]) + "\n"
            rank += 1

            if rank % 10 == 0:
                context.bot.send_message(chat_id=chat_id, text=msg)
                msg = ""

        if rank % 10 != 0:
            context.bot.send_message(chat_id=chat_id, text=msg)

    else:
        update.message.reply_text("Petit curieux 😅")


def broadcast(update, context):
    """Init a broadcasting operation"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id in bd1a:
        context.bot.send_message(chat_id=chat_id, text=broadcast_str[CHANNEL])

        day = context.bot_data["date"]
        activities_today = activities[day]

        msg = ""
        for act in activities_today:
            msg += act["id"] + "\n"

        context.bot.send_message(chat_id=chat_id, text=msg)
        return CHANNEL

    else:
        context.bot.send_message(chat_id=chat_id, text="Petit curieux 😅")
        return ConversationHandler.END


def channel(update, context):
    """Select the channel while in a broadcasting operation"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    target = update.message.text.strip()

    day = context.bot_data["date"]
    activities_today = activities[day]

    for act in activities_today:
        if target == act["id"] or target == "dailies" or target == "enigms":
            context.user_data["broadcast"] = target
            context.bot.send_message(chat_id=chat_id, text=right_channel.format(target))
            context.bot.send_message(chat_id=chat_id, text=broadcast_str[MESSAGE])
            return MESSAGE

    context.bot.send_message(chat_id=chat_id, text=wrong_channel.format(target))
    return CHANNEL


def message(update, context):
    """Receive the message to broadcast"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    context.user_data["message"] = update.message.text
    context.bot.send_message(chat_id=chat_id, text=broadcast_str[CONFIRMATION], quote=True)

    return CONFIRMATION


def confirmation(update, context):
    """Get the confirmation for the current message being broadcast by `user_id`
       and send it the the users subscribed or registered to `target`"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    answer = update.message.text.strip().lower()

    if answer in ["o", "oui"]:
        context.bot.send_message(chat_id=chat_id, text=broadcast_str[SENT])

        target = context.user_data["broadcast"]
        msg = context.user_data["message"]

        users = context.bot_data["users"]

        for usr in users:
            if (target in users[usr]["registrations"]) or (target in users[usr]["subscriptions"]):
                context.bot.send_message(chat_id=usr, text=msg)

        context.user_data["broadcast"] = ""
        context.user_data["message"] = ""

        return ConversationHandler.END


    elif answer in ["n", "non"]:
        context.bot.send_message(chat_id=chat_id, text=wrong_message)
        return MESSAGE
    else:
        context.bot.send_message(chat_id=chat_id, text=incorrect_yes_no)
