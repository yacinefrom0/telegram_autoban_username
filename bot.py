import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# To understand : https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
#TODO : telegram.ChatMemberUpdated only represents changes in the status of a user.
#What you can do is checking every time from which user the update came in the chat and store
#its current Name/username whatever and compare it

TOKEN = 'BOT_TELEGRAM_TOKEN_HERE'
whitelisted_user_ids = [
    970285864343175258,  # your_moderator_user_id_here
    123456789123456789,  # your_moderator_user_id_here
]
target_strings = [
    'massa',
    'massa support',
    'massa official',
]
def start(update, context):
    update.message.reply_text("""
Bienvenue sur le bot officiel de Yacine.

Les commandes disponibles sont :
- /info pour comprendre qui je suis.
    """)


def info(update, context):
    update.message.reply_text('Bonjour :) Je suis MassaVeilleur, ici pour vous protéger du mieux que je peux!')

def new_user(update, context):
    bot = telegram.Bot(TOKEN)
    user = update.message.from_user
    chat_id = update.message.chat_id
    member_banned = False
    member_names = [user['username'], user['last_name'], user['first_name']]

    #print('L\'utilisateur est {} et son user ID est : {} et  son last_name est {} et son firstname est {} '.format(user['username'], user['id'], user['last_name'], user['first_name']))
    if user['id'] not in whitelisted_user_ids:
        for target_string in target_strings:
            if member_banned is False:
                for member_name in member_names:
                    if (member_name is not None) and (target_string in member_name.lower()):
                        print('L\'utilisateur {} matche avec un nom interdit!'.format(user['username']))
                        try:
                            print('Je bannis {}!'.format(user['username']))
                            bot.ban_chat_member(chat_id, user['id'])
                            member_banned = True
                            break
                        except:
                            print('J\'arrive pas à bannir {}... :c'.format(user['username']))
    else:
        print('Le membre {} est dans la whitelist, j\'ignore...'.format(user['username']))
    if member_banned is False:
        print('No need to ban {}, does not match the target strings!'.format(user['username']))


def main():
    # La classe Updater permet de lire en continu ce qu'il se passe sur le channel
    updater = Updater(TOKEN, use_context=True)

    # Pour avoir accès au dispatcher plus facilement
    dp = updater.dispatcher

    # On ajoute des gestionnaires de commandes
    # On donne a CommandHandler la commande textuelle et une fonction associée
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user))

    # Pour gérer les autres messages qui ne sont pas des commandes
    #dp.add_handler(MessageHandler(Filters.text, pas_compris))

    # Sert à lancer le bot
    updater.start_polling()

    # Pour arrêter le bot proprement avec CTRL+C
    updater.idle()


if __name__ == '__main__':
    main()
