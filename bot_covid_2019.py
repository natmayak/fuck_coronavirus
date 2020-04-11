from emoji import emojize
from glob import glob
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')


def greeting(update, context):
    user = update.effective_user
    first_name = user.first_name
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    # todo Добавить инструкцию и описание бота типа что бот делает, как и что делать пользователю
    greeting_text = f'Hello {first_name}{emo}. Best of luck with the corona crisis. I am going to help you stay alive. Try to keep your hands off anyway'
    context.bot.send_message(chat_id=update.effective_chat.id, text=greeting_text, reply_markup=get_keyboard())


def talk_to_me(update, context):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_text = "Hi {} {}, you just caught some germs and said {}".format(update.message.chat.first_name, emo,
                                                                          update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=user_text, reply_markup=get_keyboard())


def get_location(update, context):
    print(update.message.location)
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    location_text = f'Big brother is watching you (for your own safety) {emo}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=location_text, reply_markup=get_keyboard())


# функция добавляет клавиатуру. вставляем эту функцию везде в reply_markup, чтобы кнопки появлялись не только на старте, а всегда
def get_keyboard():
    location_button = KeyboardButton('location', request_location=True)
    buttons = ReplyKeyboardMarkup([['I want to go out', 'sticker'], [location_button]], resize_keyboard=True)
    # resize позволяет заузить кнопки в моб. версии бота, тк исходно на айфоне кнопки выходят огромными (на десктопе кнопки сразу ок)
    return buttons


# отправку стикера пока вывела через кнопку, чтобы протестить работу.
# Далее кнопку можно убрать, а функцию использовать в составе job_queue
# . tgs - формат telegram sticker. папка с файлами сейчас в корне
def send_covid(update, context):
    covid_stickers = glob('media/*.tgs')  # glob позволяет отбирать путь к файлу по заданному шаблону и создает словарь
    sticker = choice(covid_stickers)  # выбор рандомного стикера
    context.bot.send_sticker(chat_id=update.message.chat.id, sticker=open(sticker,
                                                                          'rb'))  # rb - read binary, этот параметр добавляется для нетекстовых объектов


# под распад ковида. сейчас задано через видео, но если гифка будет не в mp4, вероятно задавать через photo
def bust_covid(update, context):
    covid_gifs = glob('media/*.mp4')
    busted_covid = choice(covid_gifs)  # choice выбирает файл из списка
    context.bot.send_video(chat_id=update.message.chat.id, video=open(busted_covid, 'rb'))


def brodsky(update, context):
    context.bot.send_voice(chat_id=update.message.chat.id, voice=open(choice(glob('media/*.mp3')), 'rb'))
    # на войс не писала отдельную функцию, работает по принципу стикера: в папке ищем файл, отбираем 1


def regular_messages(update, context, sticker, reply_button):
    face = "Don't touch your face!"
    hands = "Wash your hands!"
    windows = "Open your windows and go out of your room for 10-15 minutes"
    fuck = "Fuck coronavirus!"
    messages = [face, hands, windows, fuck]
    revealed_message = choice(messages)
    if revealed_message == face:
        keyboard = InlineKeyboardButton('Well I do not touch it!')
        reply_button = InlineKeyboardMarkup(keyboard)
        sticker = glob('face.tgs')
    elif revealed_message == hands:
        keyboard = InlineKeyboardButton('Alright, alright. I have washed my hands!')
        reply_button = InlineKeyboardMarkup(keyboard)
        sticker = glob('hands.tgs')
    elif revealed_message == windows:
        keyboard = InlineKeyboardButton('Hm ok, I will do that.')
        reply_button = InlineKeyboardMarkup(keyboard)
        sticker = glob('fine.tgs')
    elif revealed_message == fuck:
        keyboard = InlineKeyboardButton('Hell yeah! Fuck it!!!')
        reply_button = InlineKeyboardMarkup(keyboard)
        sticker = glob('fuck.tgs')
    context.bot.send_sticker(chat_id=update.message.chat.id, sticker=open(sticker, 'rb'))
    context.bot.send_message(chat_id=update.message.chat_id, text=revealed_message, reply_markup=reply_button)

#todo для теста, удалить, когда заработает обычная функция
def bla(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='bla')


def main():
    updater = Updater(settings.API_KEY, request_kwargs=settings.PROXY, use_context=True)
    # в новой версии tg api updater задается через use_context

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greeting))
    dp.add_handler(MessageHandler(Filters.regex('^(I want to go out)$'), brodsky))
    # regex фильтр сравнивает текст из кнопки с текстом, на который хендлер реагирует
    dp.add_handler(MessageHandler(Filters.regex('^(sticker)$'), send_covid))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(MessageHandler(Filters.location, get_location))
    dp.job_queue.run_repeating(regular_messages, interval=60, first=0)
    # todo для теста, удалить, когда заработает обычная функция
    dp.job_queue.run_once(bla, 1)
    updater.start_polling()
    updater.idle()


main()
