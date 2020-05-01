from emoji import emojize
from glob import glob
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from db import db, get_or_create_user, toggle_subscription, get_subscribers

import settings
import logging
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')

# Создаем переменную, обозначающую, находится ли юзер дома или нет. По-умолчанию - да
inhouse = True

# Создаем переменные с локацией пользователя
longitude = float
latitude = float


def greeting(update, context):
    user = update.effective_user
    first_name = user.first_name
    user_data = get_or_create_user(db, update.effective_user, update.message)
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    greeting_text = f'Hello {first_name}{emo}. Best of luck with the corona crisis. I am going to help you stay alive. \n ' \
                    f'\n' \
                    f'Try to keep your hands off anyway. Now try /subscribe and see what happens! \n' \
                    f'\n' \
                    f'Also we can show you the closest pharmacy if something goes wrong with you. Try Pharmacies button and we will show you where you should go'
    context.bot.send_message(chat_id=update.effective_chat.id, text=greeting_text, reply_markup=get_keyboard(update))
    print(update.effective_chat.id)


def get_keyboard(update):
    location_button = KeyboardButton('Pharmacies', request_location=True)
    user = get_or_create_user(db, update.effective_user, update.message)
    if user.get('subscribed'):
        sub_button = 'Unsubscribe'
    else:
        sub_button = 'Subscribe'
    if inhouse:
        leave_button = 'I am leaving my place'
    else:
        leave_button = 'I am back'
    buttons = ReplyKeyboardMarkup([['I want to go out', leave_button], [sub_button], [location_button]],
                                  resize_keyboard=True)
    return buttons


def talk_to_me(update, context):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_text = "Hi {} {}, you just caught some germs and said {}".format(update.message.chat.first_name, emo,
                                                                          update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=user_text, reply_markup=get_keyboard(update))


def get_yandex():
    # todo названия аптек
    API_URL = 'https://search-maps.yandex.ru/v1/'
    # в spn задается амплитуда поиска
    PARAMS = dict(text='аптеки', ll=f'{longitude}, {latitude}', spn="0.01000,0.01000", lang='ru_RU',
                  apikey=settings.API_KEY_YNDX)

    response = requests.get(API_URL, params=PARAMS)

    results = response.json()
    places = results['features']
    lst_of_places = list()
    lst_of_names = list()
    lst_of_links = list()
    index_number = 0
    # создаем одним действием через while списки всего, что нужно забрать, при этом легко менять количество нужных элементов:
    while index_number <= 2:
        lst_of_places.append(places[index_number]['geometry']['coordinates'])
        lst_of_names.append(places[index_number]['properties']['name'])
        lst_of_links.append(
            f'https://yandex.ru/maps/?text={lst_of_places[index_number][1]}%2C{lst_of_places[index_number][0]}')
        index_number += 1
    print(lst_of_places)
    print(lst_of_names)
    print(lst_of_links)
    return (lst_of_names, lst_of_links)


def get_location(update, context):
    location = update.message.location
    global latitude
    latitude = location['latitude']
    global longitude
    longitude = location['longitude']
    print(location)
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    location_text = f'Big brother is watching you (for your own safety) {emo}'
    pharmacies_text = 'Here are the pharmacies nearest to you:'
    # stores_text = 'In case you are intolerant to home delivery, here’s a list of the nearest stores. Don’t forget to have your QR-code with you in case you meet the polite people.'
    yandex_data = get_yandex()
    place_names = yandex_data[0]
    links = yandex_data[1]
    index_number = 0
    context.bot.send_message(chat_id=update.effective_chat.id, text=location_text, reply_markup=get_keyboard(update))
    context.bot.send_message(chat_id=update.effective_chat.id, text=pharmacies_text, reply_markup=get_keyboard(update))
    while index_number <= 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=place_names[index_number],
                                 reply_markyp=get_keyboard(update))
        context.bot.send_message(chat_id=update.effective_chat.id, text=links[index_number],
                                 reply_markyp=get_keyboard(update))
        index_number += 1


def send_covid(update, context):
    covid_stickers = glob('media/*.tgs')
    sticker = choice(covid_stickers)
    context.bot.send_sticker(chat_id=update.message.chat.id, sticker=open(sticker, 'rb'))


def bust_covid(update, context):
    covid_gifs = glob('media/*.mp4')
    busted_covid = choice(covid_gifs)
    context.bot.send_video(chat_id=update.message.chat.id, video=open(busted_covid, 'rb'))


def brodsky(update, context):
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open(choice(glob('root/fuck_coronavirus/media/brodskyi.mp3')), 'rb'))


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
    if inhouse:
        for user in get_subscribers(db):
            context.bot.send_message(chat_id=user['chat_id'], text=action[0], reply_markup=reply_button)
    else:
        pass


#         # if action[0] == 'Fuck coronavirus!':
#         #     busted_covid = choice(glob('media/*.mp4'))
#         #     context.bot.send_video(chat_id=chat_id, video=open(busted_covid, 'rb'))
#         # else:
#         #     sticker = choice(glob(str(action[2])))
#         #     context.bot.send_sticker(chat_id=chat_id, sticker=open(sticker, 'rb'))


def button(update, context):
    query = update.callback_query
    query.answer()
    # todo нужно еще удалять стикеры.
    query.edit_message_text(text='{}'.format(query.data))


def subscribe(update, context):
    subscribe_text = "Thanks for subscribing! If you are not good enough for us you can always use /unsubscribe. " \
                     "But you'd rather not. Please"
    already_subscribe_text = "Oh please stop it! You are already such a good boy/girl."
    user_data = get_or_create_user(db, update.effective_user, update.message)
    if not user_data.get('subscribed'):
        toggle_subscription(db, user_data)
        context.bot.send_message(chat_id=update.message.chat_id, text=subscribe_text, reply_markup=get_keyboard(update))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=already_subscribe_text,
                                 reply_markup=get_keyboard(update))


def unsubscribe(update, context):
    unsubscribe_text = "Well, you gonna die anyway. See you, little pussy..."
    nonsubscribe_text = "How can you unsubscribe if you haven't subscribed yet? Use your brain and press /subscribe"
    user_data = get_or_create_user(db, update.effective_user, update.message)
    if user_data.get('subscribed'):
        toggle_subscription(db, user_data)
        context.bot.send_message(chat_id=update.message.chat_id, text=unsubscribe_text,
                                 reply_markup=get_keyboard(update))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=nonsubscribe_text,
                                 reply_markup=get_keyboard(update))


def leave_home(update, context):
    leave_home_text = "Welcome to take your own risks. Do not whine afterwards. However dead people can't whine..."
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
    updater.job_queue.run_repeating(regular_messages, interval=5, first=5)
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('location', get_location))

    updater.start_polling()
    updater.idle()


main()
