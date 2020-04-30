from emoji import emojize
from glob import glob
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import settings
import logging
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')

# Создаем сет с подписчиками. Отсюда будем забирать чат айди
#todo Сделать базу данных для сабов
subscribers = set()

# Создаем переменную, обозначающую, находится ли юзер дома или нет. По-умолчанию - да
inhouse = True

# Создаем перменные с локацией пользователя
longitude = float
latitude = float


def greeting(update, context):
    user = update.effective_user
    first_name = user.first_name
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    greeting_text = f'Hello {first_name}{emo}. Best of luck with the corona crisis. I am going to help you to stay alive. \n ' \
                    f'\n' \
                    f'Try to keep your hands off anyway. Now try /subscribe and see what happens! \n' \
                    f'\n' \
                    f'Also we can show you the closest pharmacy if something goes wrong with you. Try Pharmacies button and we will show you where you should go'
    context.bot.send_message(chat_id=update.effective_chat.id, text=greeting_text, reply_markup=get_keyboard(update))
    print(update.effective_chat.id)


def get_keyboard(update):
    location_button = KeyboardButton('Pharmacies', request_location=True)
    if update.message.chat_id in subscribers:
        sub_button = 'Unsubscribe'
    else:
        sub_button = 'Subscribe'
    if inhouse == True:
        leave_button = 'I am leaving my place'
    else:
        leave_button = 'I am back'
    buttons = ReplyKeyboardMarkup([['I want to go out', leave_button], [sub_button], [location_button]], resize_keyboard=True)
    return buttons


def talk_to_me(update, context):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_text = "Hi {} {}, you just caught some germs and said {}".format(update.message.chat.first_name, emo,
                                                                          update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=user_text, reply_markup=get_keyboard(update))


def get_yandex():
    #todo названия аптек
    API_URL = 'https://search-maps.yandex.ru/v1/'

    PARAMS = dict(text='аптеки', ll=f'{longitude}, {latitude}', lang='ru_RU', apikey=settings.API_KEY_YNDX)

    response = requests.get(API_URL, params=PARAMS)

    results = response.json()
    pharmacies = results['features']
    lst_of_pharmacies = list()
    lst_of_pharmacies.append(pharmacies[0]['geometry']['coordinates'])
    lst_of_pharmacies.append(pharmacies[1]['geometry']['coordinates'])
    lst_of_pharmacies.append(pharmacies[2]['geometry']['coordinates'])

    coordinates_1 = lst_of_pharmacies[0]
    coordinates_2 = lst_of_pharmacies[1]
    coordinates_3 = lst_of_pharmacies[2]
    longitude_1 = coordinates_1[0]
    latitude_1 = coordinates_1[1]
    longitude_2 = coordinates_2[0]
    latitude_2 = coordinates_2[1]
    longitude_3 = coordinates_3[0]
    latitude_3 = coordinates_3[1]

    link_1 = f'https://yandex.ru/maps/?text={latitude_1}%2C{longitude_1}'
    link_2 = f'https://yandex.ru/maps/?text={latitude_2}%2C{longitude_2}'
    link_3 = f'https://yandex.ru/maps/?text={latitude_3}%2C{longitude_3}'

    return link_1, link_2, link_3


def get_location(update, context):
    location = update.message.location
    global latitude
    latitude = location['latitude']
    global longitude
    longitude = location['longitude']
    print(location)
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    location_text = f'Big brother is watching you (for your own safety) {emo}'
    pharmacies_text = 'Here are the nearest pharmacies to you:'
    links = get_yandex()
    print(links)
    link_1 = links[0]
    link_2 = links[1]
    link_3 = links[2]
    context.bot.send_message(chat_id=update.effective_chat.id, text=location_text, reply_markup=get_keyboard(update))
    context.bot.send_message(chat_id=update.effective_chat.id, text=pharmacies_text, reply_markup=get_keyboard(update))
    context.bot.send_message(chat_id=update.effective_chat.id, text=link_1, reply_markyp=get_keyboard(update))
    context.bot.send_message(chat_id=update.effective_chat.id, text=link_2, reply_markyp=get_keyboard(update))
    context.bot.send_message(chat_id=update.effective_chat.id, text=link_3, reply_markyp=get_keyboard(update))


def send_covid(update, context):
    covid_stickers = glob('media/*.tgs')
    sticker = choice(covid_stickers)
    context.bot.send_sticker(chat_id=update.message.chat.id, sticker=open(sticker, 'rb'))


def bust_covid(update, context):
    covid_gifs = glob('media/*.mp4')
    busted_covid = choice(covid_gifs)
    context.bot.send_video(chat_id=update.message.chat.id, video=open(busted_covid, 'rb'))


def brodsky(update, context):
    context.bot.send_voice(chat_id=update.message.chat.id, voice=open(choice(glob('root/fuck_coronavirus/media/brodskyi.mp3')), 'rb'))


def regular_messages(context):
    action_set = [
        ["Do not touch your face!", 'Well I do not touch it!', 'media/face.tgs', "But it's okay to touch yourself:)"],
        ["Wash your hands!", 'Alright, alright. I have washed my hands!', 'media/hands.tgs',
         'Enjoy your sparkling fingers then'],
        ["Open your windows and go out of your room for 10-15 minutes", 'Well ok, I will do that.', 'media/fine.tgs',
         'Now breathe in deeply through the nose'],
        ["Fuck coronavirus!", 'Hell yeah! Fuck it!!!', 'media/fuck.tgs',
         'Busted picture of covid that I do not have so far']]
    action = choice(action_set)
    keyboard = [[InlineKeyboardButton(action[1], callback_data=action[3])]]
    reply_button = InlineKeyboardMarkup(keyboard)
    if inhouse == True:
        for chat_id in subscribers:
            context.bot.send_message(chat_id=chat_id, text=action[0], reply_markup=reply_button)
    else:
        pass
        # if action[0] == 'Fuck coronavirus!':
        #     busted_covid = choice(glob('media/*.mp4'))
        #     context.bot.send_video(chat_id=chat_id, video=open(busted_covid, 'rb'))
        # else:
        #     sticker = choice(glob(str(action[2])))
        #     context.bot.send_sticker(chat_id=chat_id, sticker=open(sticker, 'rb'))


def button(update, context):
    query = update.callback_query
    query.answer()
    # todo нужно еще удалять стикеры.
    query.edit_message_text(text='{}'.format(query.data))


def subscribe(update, context):
    subscribe_text = "Hey thanks for your subscribing! If you are not good enough for us you can always use /unsubscribe. " \
                     "But you'd rather not. Please"
    already_subscribe_text = "Oh please stop it! You are already such a good boy/girl."
    if update.message.chat_id in subscribers:
        context.bot.send_message(chat_id=update.message.chat_id, text=already_subscribe_text,
                                 reply_markup=get_keyboard(update))
    else:
        subscribers.add(update.message.chat_id)
        context.bot.send_message(chat_id=update.message.chat_id, text=subscribe_text, reply_markup=get_keyboard(update))


def unsubscribe(update, context):
    unsubscribe_text = "Well you are gonna die anyway. Little pussy! See you..."
    nonsubscribe_text = "How can you unsubscribe if you haven't subscribed yet? Use your brain and press /subscribe"
    if update.message.chat_id in subscribers:
        subscribers.remove(update.message.chat_id)
        context.bot.send_message(chat_id=update.message.chat_id, text=unsubscribe_text,
                                 reply_markup=get_keyboard(update))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=nonsubscribe_text,
                                 reply_markup=get_keyboard(update))


def leave_home(update, context):
    leave_home_text = "Well it is your own risk. Do not whine afterwards. However dead people can't whine..."
    global inhouse
    inhouse = False
    context.bot.send_message(chat_id=update.message.chat_id, text=leave_home_text, reply_markup=get_keyboard(update))


def back_home(update, context):
    back_home_text = 'Thanks god, you are still alive. But probably it will not last longer.'
    global inhouse
    inhouse = True
    context.bot.send_message(chat_id=update.message.chat_id, text=back_home_text, reply_markup=get_keyboard(update))

def main():
    updater = Updater(settings.API_KEY, request_kwargs=settings.PROXY, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greeting))
    dp.add_handler(MessageHandler(Filters.regex('^(I want to go out)$'), brodsky))
    dp.add_handler(MessageHandler(Filters.regex('^(Subscribe)$'), subscribe))
    dp.add_handler(MessageHandler(Filters.regex('^(Unsubscribe)$'), unsubscribe))
    dp.add_handler(MessageHandler(Filters.regex('^(I am leaving my place)$'), leave_home))
    dp.add_handler(MessageHandler(Filters.regex('^(I am back)$'), back_home))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(MessageHandler(Filters.location, get_location))
    updater.job_queue.run_repeating(regular_messages, interval=10, first=10)
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('location', get_location))

    updater.start_polling()
    updater.idle()


main()
