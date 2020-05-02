import telegram.bot
from telegram.ext import *

from data import *
from hello import *

MYSTEIRB_SUB = 81

def mysteirb(update, context):
    """Handle /mysteirb command"""

    if is_known_user(update, context):
        user_id = update.effective_user.id
        logger.info("[/mysteirb] User {} solving the mysteirb".format(user_id))

        context.bot.send_message(chat_id=user_id, text="Alors, quel est le vrai nom du BDA 2020-2021 selon toi ?")

        return MYSTEIRB_SUB


def mysteirb_sub(update, context):
    user_id = update.effective_user.id
    rep = update.message.text[:50].strip().replace("\n", " ")

    user_data = context.bot_data["users"][user_id]
    user_data["mysteirb"] = rep

    update.message.reply_text("Le Myst'eirb sera levé ce soir !")

    return ConversationHandler.END
