from data import *
from hello import *


def allo(update, context):
    """Handle the beginning of a /allo conversation and propose available allos"""

    if is_known_user(update, context):
        user_id = update.effective_user.id
        logger.info("[/allo] User {} asking for a allo".format(user_id))

        keyboard = [[KeyboardButton(t)] for t in allo_groups]

        context.bot.send_message(chat_id=user_id, text=allo_welcome,
                                 reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

        return ALLO_TYPE


def allo_type(update, context):
    """Receive allo type and check correctness"""

    user_id = update.effective_user.id
    allo_type = update.message.text[:30].strip()
    context.user_data["allo_type"] = allo_type

    if allo_type not in allo_groups:
        update.message.reply_text(allo_invalid_type)
        return ALLO_TYPE

    if allo_type == "Culture":
        allo_message(update, context)
        return ConversationHandler.END

    else:
        context.bot.send_message(chat_id=user_id,
                                 text=allo_valid_type.format(allo_type),
                                 reply_markup = ReplyKeyboardRemove())

    return ALLO_MESSAGE


def allo_message(update, context):
    """Receive allo message and dispatch to the associated TG group"""

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    msg_id = update.message.message_id

    user_data = context.bot_data["users"][user_id]
    allo_type = context.user_data["allo_type"]

    allo_formatted = new_allo.format(update.effective_user.name,
                                     user_id_str(user_data),
                                     update.message.text[:3800])

    logger.info("[/allo] {}\n".format(allo_formatted))

    context.bot.send_message(chat_id=allo_groups[allo_type],
                             text=allo_formatted)

    context.bot.send_message(chat_id=user_id, text=allo_sent,
                             reply_markup = ReplyKeyboardRemove())

    context.user_data["allo_type"] = None

    return ConversationHandler.END
