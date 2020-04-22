from emoji import emojize
from glob import glob
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import settings
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')

# Создаем сет с подписчиками. Отсюда будем забирать чат айди
subscribers = set()


def greeting(update, context):
    user = update.effective_user
    first_name = user.first_name
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    # todo Добавить инструкцию и описание бота типа что бот делает, как и что делать пользователю
    greeting_text = f'Hello {first_name}{emo}. Best of luck with the corona crisis. I am going to help you to stay alive. Try to keep your hands off anyway. Now try /subscribe and see what happens!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=greeting_text, reply_markup=get_keyboard(update))
    print(update.effective_chat.id)


def get_keyboard(update):
    location_button = KeyboardButton('location', request_location=True)
    if update.message.chat_id in subscribers:
        sub_button = 'unsubscribe'
    else:
        sub_button = 'subscribe'
    buttons = ReplyKeyboardMarkup([['I want to go out', sub_button], [location_button]], resize_keyboard=True)
    return buttons


def talk_to_me(update, context):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_text = "Hi {} {}, you just caught some germs and said {}".format(update.message.chat.first_name, emo,
                                                                          update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=user_text, reply_markup=get_keyboard(update))


def get_location(update, context):
    print(update.message.location)
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    location_text = f'Big brother is watching you (for your own safety) {emo}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=location_text, reply_markup=get_keyboard(update))


def send_covid(update, context):
    covid_stickers = glob('media/*.tgs')
    sticker = choice(covid_stickers)
    context.bot.send_sticker(chat_id=update.message.chat.id, sticker=open(sticker, 'rb'))


def bust_covid(update, context):
    covid_gifs = glob('media/*.mp4')
    busted_covid = choice(covid_gifs)
    context.bot.send_video(chat_id=update.message.chat.id, video=open(busted_covid, 'rb'))


def brodsky(update, context):
    context.bot.send_voice(chat_id=update.message.chat.id, voice=open(choice(glob('media/*.mp3')), 'rb'))


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
    for chat_id in subscribers:
        context.bot.send_message(chat_id=chat_id, text=action[0], reply_markup=reply_button)
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
    subscribe_text = "Hey thanks for your subscribing! If you are not good enough for us you can always use /unsubscribe. But you'd rather not. Please"
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


def main():
    updater = Updater(settings.API_KEY, request_kwargs=settings.PROXY, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greeting))
    dp.add_handler(MessageHandler(Filters.regex('^(I want to go out)$'), brodsky))
    dp.add_handler(MessageHandler(Filters.regex('^(subscribe)$'), subscribe))
    dp.add_handler(MessageHandler(Filters.regex('^(unsubscribe)$'), unsubscribe))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(MessageHandler(Filters.location, get_location))
    updater.job_queue.run_repeating(regular_messages, interval=1020, first=10)
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))

    updater.start_polling()
    updater.idle()


main()
