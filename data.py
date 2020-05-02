from datetime import datetime, time

token = "BOT_TOKEN"

# Useful identifiers
admins = [123456789, 123456789]
bd1a = [123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789, 123456789]
assist_chat = -430574505

# Time reference for delay calculation
time_origin = datetime(2020, 4, 25, 12, 00, 00)

# User data
empty_user = {"name": "",
              "first_name": "",
              "last_name": "",
              "major": "",
              "pseudo": "",
              "subscriptions": ["enigms", "dailies"],
              "registrations": [],
              "enigm_data": {"time": time_origin,
                             "answers": 0}}


# Hello data
FIRST_NAME, LAST_NAME, MAJOR, PSEUDO, SUBSCRIBE, END = range(6)

ask = ["Quel est ton prénom ?",
       "Okay, maintenant ton nom de famille ?",
       "Super ! Tu étudies dans quelle filière ?",
       "Je le savais, la meilleure !\nSous quel pseudo souhaites-tu participer à la SDAV ?",
       "Quelles notifications souhaites-tu recevoir ? Tu pourras modifier ce paramètre plus tard avec la commande /subscribe",
       "Génial, merci 😊"]

validation_subscribe = "J'ai bien pris en compte tes inscriptions"
invalid_input = "Tu es sûr de toi ?"

intro = "Bonjour, je m'appelle @SDAV_Bot 🤖 et je m'occupe des inscriptions aux différentes activités organisées par Myst'eirb durant la SDAV."
ask_data = "Je vais commencer par te demander quelques informations qui me seront utiles 😉\nAttention, je ne retiens pas plus de 30 caractères !"
recap_data = "Je récapitule :"
incorrect_data = "S'il y a une erreur, tu peux exécuter la commande /start_again"
already_started = "Je crois qu'on se connaît déjà ! 😏"
inform_cancel = "Pour annuler, tu peux envoyer /cancel"
success_cancel = "Ok, on s'arrête là 😅"

finish_start = "Tu peux gérer tes notifications avec la commande /subscribe et t'inscire aux activités du jour avec /register\nPour avoir plus d'informations sur les activités organisées : /activities\nEnfin, tu peux demander un /allo quand tu le souhaites 😊\nEt si jamais tu es bloqué, essaie /help !"

majors = ["INFO 💚",
          "MMK ❤",
          "ELEC 💙",
          "TELE 💛",
          "RSI 💜",
          "SEE 💗"]

subscriptions = ["dailies", "enigms"]
subscriptions_names = {"enigms": "Jeu des énigmes",
                       "dailies": "Planning du jour"}

register_question = "Voici la liste des activités du jour.\nÀ quelle(s) activité(s) veux-tu t'inscrire ?"
subscribe_validation = "J'ai fini ma sélection"
validation_subscribe = "J'ai bien pris en compte tes inscriptions"


# Activities
kahoot_str = "Kahoot"
pictio_str = "Pictionnary"
blind_str = "Blind-test"
master_str = "Master of the Grid"
champion_str = "Question pour un Champion"

# Probably could do better with proper JSON files but I don't have
# the time to mess around with that
activities = {27: [{"id": "kahoot1", "name": kahoot_str, "time": time(14, 00)},
                   {"id": "blind1",  "name": blind_str,  "time": time(18, 00)},
                   {"id": "master1", "name": master_str, "time": time(21, 00)}],

              28: [{"id": "pictio1", "name": pictio_str, "time": time(10, 30)},
                   {"id": "blind2",  "name": blind_str,  "time": time(14, 00)},
                   {"id": "kahoot2", "name": kahoot_str, "time": time(18, 00)},
                   {"id": "blind3",  "name": blind_str,  "time": time(21, 30)}],

              29: [{"id": "kahoot3", "name": kahoot_str, "time": time(11, 00)},
                   {"id": "kahoot4", "name": kahoot_str, "time": time(16, 00)},
                   {"id": "blind4",  "name": blind_str,  "time": time(18, 00)},
                   {"id": "pictio2", "name": pictio_str, "time": time(21, 30)}],

              30: [{"id": "kahoot5", "name": kahoot_str, "time": time(11, 00)},
                   {"id": "master2", "name": master_str, "time": time(14, 00)},
                   {"id": "blind5",  "name": blind_str,  "time": time(18, 00)},
                   {"id": "kahoot6", "name": kahoot_str, "time": time(21, 30)}],

              31: [{"id": "pictio3",  "name": pictio_str,   "time": time(10, 30)},
                   {"id": "champion", "name": champion_str, "time": time(21, 30)},
                   {"id": "blind6",   "name": blind_str,    "time": time(18, 00)}]}


# Broadcast data
CHANNEL, MESSAGE, CONFIRMATION, SENT = range(4)

broadcast_str = ["À quelle activité ton message est-il dédié ?\nVoici des propositions :",
                 "Quel est ton message ?",
                 "Okay ce message est-il correct ? [O/N]\nRelis-toi 😉 cette action n'est pas réversible",
                 "C'est parti !"]

right_channel = "Super, un message pour \"{}\" !"
wrong_channel = "Je ne connais pas cette activité : \"{}\"...\nOn recommence ?"

wrong_message = "Mince, on recommence alors...\nQuel est ton messsage ?"
incorrect_yes_no = "Pas compris... [O/N] ?"

planning_next_day = "Le planning des activités vient d'être mis à jour !\nTu peux t'inscrire en effectuant la commande /register"
update_day_finished = "Nous sommes passés au jour {} avec succès"

next_day_dailies = "Le planning des activités vient d'être mis à jour !\nTu peux t'inscrire en effectuant la commande /register"
next_day_enigms = "De nouvelles énigmes sont disponibles !\nTu peux commencer à les résoudre en lançant /enigms"


# Allos
allo_groups = {"Dessin" : -123456789,
               "Alexandrin" : -123456789,
               "Musique" : -123456789,
               "Culture" : -123456789,
               "Question" : -123456789,
               "Meme" : -123456789}

ALLO_TYPE, ALLO_MESSAGE = range(2)

allo_welcome = "Quel type de allô souhaites-tu ?\nTu peux annuler à tout moment avec /cancel"
allo_valid_type = "Okay, un allô {}. Quelle est ta demande ?"
allo_invalid_type = "Hum, je n'ai pas compris 😅"
new_allo = "Nouvel allô de {}, {} :\n{}"
allo_sent = "J'ai transmis ta demande 😊"


# /help texts and links
# tutos = "Le Myst'eirb reste entier 🕵️\nEncore un peu de patience !"

tutos = "Fonctionnement de @# SDAV_Bot : https://bit.ly/3bEeeA9 \n\n\
> Activités à inscription (/register)\n\
Blind-test : https://bit.ly/2W3jl6o \n\
Finale du Blind-test : https://bit.ly/2xefmM6 \n\
Kahoot : https://bit.ly/356nIln \n\
Questions pour un Enseirbien : https://bit.ly/35767tp \n\
Pictionnary : https://bit.ly/3bAuSkh \n\
Master of the Grid : https://bit.ly/2zoPfTd \n\n\
> Activités sans inscription : \n\
Animal Crossing : https://bit.ly/3eV8rYY \n\
Enigmes (/enigms) : https://bit.ly/358Ol9l \n\
Reproductions d'oeuvres d'art : https://bit.ly/2W0uW6f\n"


# Enigms data
DAILY_NUMBER = 10

empty_enigm_tracker = {27: [False] * DAILY_NUMBER,
                       28: [False] * DAILY_NUMBER,
                       29: [False] * DAILY_NUMBER,
                       30: [False] * DAILY_NUMBER,
                       31: [False] * DAILY_NUMBER}

enigms_answered_daily = "Tu as déjà répondu à toutes les énigmes du jour, bravo ! 👏🏻"

too_late = "Mince, tu es en retard, cette énigme n'est plus disponible... ⌚\nTu peux commencer celles d'aujourd'hui avec /next_enigm"

well_dones = ["Bien joué !",
              "Oui c'est ça, bravo !",
              "Super !",
              "Génial !",
              "T'es trop fort 💪🏻",
              "Comment t'as deviné ?"]

try_agains = ["Essaie encore !",
              "Non, ce n'est pas ça...",
              "C'est facile pourtant 🙂",
              "Non, désolé",
              "Ce n'est pas la bonne réponse",
              "Cherche encore !"]

numerals = ["Zéroième ?!",
            "Première",
            "Deuxième",
            "Troisième",
            "Quatrième",
            "Cinquième",
            "Sixième",
            "Septième",
            "Huitième",
            "Neuvième",
            "Dernière"]

not_subscribed = "Tu n'es pas inscrit à cette activité 😅 Commence par /subscribe 😊"
explanation_enigms = "Chaque jour, je te propose 10 énigmes à résoudre. Il s'agit de reconnaître un monument célèbre à partir d'une photo, d'un poème...\nPour obtenir la prochaine énigme, lance la commande /next_enigm. Tu peux ensuite répondre directement par chat et j'analyse tes réponses."
move_on = "Tu peux passer à l'énigme suivante avec /next_enigm si tu le souhaites !"

# Button prefixes
reg_prefix = "reg_"
sub_prefix = "sub_"

# Unexpected interaction
lost = "Tu t'es perdu ?"

fun_answers = ["Bip boup. Boup bip ? 🤖",
               "Hello, world!",
               "Beep Boop. Boop Beep ?",
               "La SDAV c'est trop cool !",
               "Le Myst'eirb reste entier 🕵️",
               "Oui, je suis connecté 😁",
               "Bop bilibopbop",
               "🕵️",
               "🔍",
               "?",
               "😏",
               "👾"]
