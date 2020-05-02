from data import *
from hello import *
from random import choice
from enigmes_sdav import enigms_data


def hide_answer(str):
    """Returns a hint-string for str"""

    hidden = "("
    count = 0
    for i in str:
        if i in [" ", "-", "'", "’"]:
            hidden += i
        else:
            hidden += '–'
            count += 1
    hidden += " : {} lettres)".format(count)
    return hidden


def enigms(update, context):
    """Explain the enigms game"""

    if is_known_user(update, context):

        user_id = update.effective_user.id
        user_subs = context.bot_data["users"][user_id]["subscriptions"]

        if "enigms" not in user_subs:
            context.bot.send_message(chat_id=user_id, text=not_subscribed)

        else:
            context.bot.send_message(chat_id=user_id, text=explanation_enigms)


def next_enigm(update, context):
    """Give a new enigm, if possible and keep track of the time"""

    chat_id = update.effective_chat.id

    if is_known_user(update, context):
        logger.info("[/next_enigm] {} is asking for another enigm".format(update.effective_user.id))

        user_id = update.effective_user.id
        user_subs = context.bot_data["users"][user_id]["subscriptions"]

        if "enigms" not in user_subs:
            context.bot.send_message(chat_id=user_id, text=not_subscribed)
            return False


        day = context.bot_data["date"]
        adv = context.user_data["enigms"][day]

        if False in adv: # enigms remaining for today
            cur_enigm = context.user_data["enigms"][day].index(False) + 1
            logger.info("[/next_enigm] Giving to {} the {}-th enigm of day {}".format(update.effective_user.id, cur_enigm, day))

            # ensure that multiple /next_enigms don't reset the timer
            if "answer" in context.user_data:
                if context.user_data["answer"]["day"] != day or context.user_data["answer"]["number"] != cur_enigm:
                    context.user_data["answer"] = {"day": day, "number": cur_enigm, "started":update.message.date}
            else:
                    context.user_data["answer"] = {"day": day, "number": cur_enigm, "started":update.message.date}


            cur_enigm_data = enigms_data[day][cur_enigm]
            caption = numerals[cur_enigm] + " énigme :"

            # Send the actual enigm
            context.bot.send_message(chat_id=user_id, text=caption)
            if "photo" in cur_enigm_data:
                # Could be improved: files sent once are accessible through a UUID
                # which can be used to send a file to mulitple conversations
                # without having to upload it every time...
                photo = open("images_enigms/" + cur_enigm_data["photo"], "rb")
                context.bot.send_photo(chat_id=user_id, photo=photo)
            else:
                context.bot.send_message(chat_id=user_id, text=enigms_data[day][cur_enigm]["text"])

            # Send the hint
            context.bot.send_message(chat_id=user_id, text=hide_answer(enigms_data[day][cur_enigm]["answer"]))

        else: # answered every enigm available today
            context.bot.send_message(chat_id=user_id, text=enigms_answered_daily)


from Levenshtein import ratio
from datetime import datetime

THRESHOLD = 0.85

def answer(update, context):
    """Vérifie que la saisie utilisateur est la réponse à la question"""

    chat_id = update.effective_chat.id

    if is_known_user(update, context) and chat_id not in allo_groups.values():
        logger.info("{} sent {}".format(update.effective_user.id, update.message.text))

        user_id = update.effective_user.id
        user_subs = context.bot_data["users"][user_id]["subscriptions"]

        if "enigms" not in user_subs or "answer" not in context.user_data:
            # Unexpected interaction with the user
            update.message.reply_text(choice(fun_answers))

        else:
            day = context.bot_data["date"]
            usr_day = context.user_data["answer"]["day"]

            if usr_day != day:
                update.message.reply_text(too_late)

            else:
                cur_enigm = context.user_data["answer"]["number"]

                usr_ans = update.message.text.lower()
                eng_ans = enigms_data[day][cur_enigm]["answer"].lower()

                if ratio(usr_ans, eng_ans) >= THRESHOLD: # the answers seems to be correct

                    delay = update.message.date - context.user_data["answer"]["started"]

                    logger.info("{} solved enigm n° {} of the {}-th day in {}".format(update.effective_user.id, cur_enigm, day, delay))

                    context.user_data["enigms"][day][cur_enigm-1] = delay
                    context.bot_data["users"][user_id]["enigm_data"]["time"] += delay
                    context.bot_data["users"][user_id]["enigm_data"]["answers"] += 1
                    context.user_data.pop("answer", None)

                    update.message.reply_text(choice(well_dones))
                    if False in context.user_data["enigms"][day]:
                        update.message.reply_text(move_on)

                else: # wrong answer
                    update.message.reply_text(choice(try_agains))


def stats(update, context):
    """Send the leaderboard"""
    # Could be improved by only sending the rank of the first 10 players
    # and the rank around the actual person asking
    # instead of sending ALL the leaderboard

    if is_known_user(update, context):
        chat_id = update.effective_chat.id
        logger.info("Giving the leaderboard to {}".format(update.effective_user.id))

        users = context.bot_data["users"]
        leaderboard_ids = []

        for user_id in users:
            if users[user_id]["enigm_data"]["answers"] > 0:
                leaderboard_ids.append(user_id)

        leaderboard_ids.sort(key=lambda id: users[id]["enigm_data"]["time"])
        leaderboard_ids.sort(key=lambda id: users[id]["enigm_data"]["answers"], reverse=True)

        context.bot.send_message(chat_id=chat_id, text="Classement : jeu des énigmes")

        msg = ""
        rank = 1

        for id in leaderboard_ids:
            msg += "{}. {} ({} rép en {})\n".format(rank, users[id]["pseudo"],
                                                    users[id]["enigm_data"]["answers"],
                                                    users[id]["enigm_data"]["time"] - time_origin)
            rank += 1

            if rank % 10 == 0:
                context.bot.send_message(chat_id=chat_id, text=msg)
                msg = ""

        if rank % 10 != 0:
            context.bot.send_message(chat_id=chat_id, text=msg)
