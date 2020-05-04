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

# Create a global variable of presence at home
inhouse = True

# Create 2 global variables with a location of user
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


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='{}'.format(query.data))


# Answer to random messages
def talk_to_me(update, context):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_text = "Hi {} {}, you just caught some germs and said {}".format(update.message.chat.first_name, emo,
                                                                          update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=user_text, reply_markup=get_keyboard(update))


# API yandex
def get_yandex():
    API_URL = 'https://search-maps.yandex.ru/v1/'
    # SPN provides the span of the search
    PARAMS = dict(text='аптеки', ll=f'{longitude}, {latitude}', spn="0.01000,0.01000", lang='ru_RU',
                  apikey=settings.API_KEY_YNDX)

    response = requests.get(API_URL, params=PARAMS)

    results = response.json()
    places = results['features']
    lst_of_places = list()
    lst_of_names = list()
    lst_of_links = list()
    index_number = 0
    while index_number <= 2:
        lst_of_places.append(places[index_number]['geometry']['coordinates'])
        lst_of_names.append(places[index_number]['properties']['name'])
        lst_of_links.append(
            f'https://yandex.ru/maps/?text={lst_of_places[index_number][1]}%2C{lst_of_places[index_number][0]}')
        index_number += 1
    return lst_of_names, lst_of_links


# Get user's location to send the list of the nearest pharmacies
def get_location(update, context):
    location = update.message.location
    global latitude
    latitude = location['latitude']
    global longitude
    longitude = location['longitude']
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    location_text = f'Big brother is watching you (for your own safety) {emo}'
    pharmacies_text = 'Here are the pharmacies nearest to you:'
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


# Sending voice message
def brodsky(update, context):
    context.bot.send_voice(chat_id=update.message.chat.id,
                           voice=open(choice(glob('root/fuck_coronavirus/media/brodsky.mp3')), 'rb'))


# Sending with regular messages with random choice
def regular_messages(context):
    action_set = [
        ["Don't touch your face!", "Well I don't touch it!", 'media/face.tgs', "But it's okay to touch yourself:)"],
        ["Wash your hands!", 'Alright, alright. I have washed my hands!', 'media/hands.tgs',
         'Enjoy your sparkling fingers then'],
        ["Open your windows and go out of your room for 10-15 minutes", 'Well ok, I will do that.', 'media/fine.tgs',
         'Now breathe in deeply through the nose'],
        ["Fuck coronavirus!", 'Hell yeah! Fuck it!!!', 'media/fuck.tgs',
         "There should be a picture of exploded covid but I don't have it sadly"]]
    action = choice(action_set)
    keyboard = [[InlineKeyboardButton(action[1], callback_data=action[3])]]
    reply_button = InlineKeyboardMarkup(keyboard)
    if inhouse:
        for user in get_subscribers(db):
            context.bot.send_message(chat_id=user['chat_id'], text=action[0], reply_markup=reply_button)
    else:
        pass


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
    unsubscribe_text = "Well, you're gonna die anyway. See you, little pussy..."
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
    back_home_text = 'Thanks God, you are still alive. But probably it will not last longer.'
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
    updater.job_queue.run_repeating(regular_messages, interval=1080, first=5)
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('location', get_location))

    updater.start_polling()
    updater.idle()


main()
