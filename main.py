import telebot
from telebot import types
import logging
import time
from urllib.error import HTTPError
from task_view import tasks
from task_description import task_dscr
from task_comment import task_comm

bot = telebot.TeleBot(### Place token here ###)

logging.basicConfig(filename='bot.log', level=logging.INFO, encoding='utf-8',
                    format='%(levelname)s %(asctime)s: %(message)s (Line: %(lineno)s - %(filename)s)', filemode='w')

logger = logging.getLogger(__name__)
handler = logging.FileHandler('bot.log', encoding='utf-8')
formatter = logging.Formatter('%(levelname)s %(asctime)s: %(message)s (Line: %(lineno)s - %(filename)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Запуск бота')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/mytasks")
    item2 = types.KeyboardButton("/description")
    item3 = types.KeyboardButton("/sendcomment")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Выберите действие:\n'
                                      '/mytasks - список открытых задач\n'
                                      '/description - открыть описание задачи по ID\n'
                                      '/sendcomment - оставить комментарий к задаче', reply_markup=markup)


@bot.message_handler(commands=['mytasks'])
def my_tasks(message):
    msg = bot.send_message(message.chat.id, 'Введите логин и пароль через пробел\nпример: login password')
    bot.register_next_step_handler(msg, task_list)


def task_list(message):
    logger.info(f'Запрос списка задач пользователем id: {message.from_user.id}')
    msg1 = bot.send_message(message.chat.id, 'Ожидайте 20 сек')
    value = message.text
    lst_tasks = tasks(value)
    time.sleep(1)
    if lst_tasks is None:
        msg2 = bot.send_message(message.chat.id, 'Открытых задач нет')
    elif lst_tasks == ValueError:
        msg2 = bot.send_message(message.chat.id, 'Пара логин/пароль имеет некорректный формат')
    elif lst_tasks == KeyError:
        msg2 = bot.send_message(message.chat.id, 'Неверный логин или пароль')
    elif lst_tasks == HTTPError:
        msg2 = bot.send_message(message.chat.id, 'Сервер недоступен')
    else:
        msg2 = bot.send_message(message.chat.id, 'Актуальные задачи:')
        for d in lst_tasks:
            msg3 = bot.send_message(message.chat.id, d)
        logger.info(f'Данные успешно переданы пользователю id: {message.from_user.id}')


@bot.message_handler(commands=['description'])
def description(message):
    msg = bot.send_message(message.chat.id, 'Введите логин, пароль и номер задачи через пробел\n'
                                            'пример: login password id')
    bot.register_next_step_handler(msg, task_description)


def task_description(message):
    logger.info(f'Запрос страницы задачи пользователем id:{message.from_user.id}')
    msg1 = bot.send_message(message.chat.id, 'Ожидайте 20 сек')
    value = message.text
    dscr_txt = task_dscr(value)
    time.sleep(1)
    if dscr_txt == ValueError:
        msg2 = bot.send_message(message.chat.id, 'Введённые данные имеют некорректный формат')
    elif dscr_txt == KeyError:
        msg2 = bot.send_message(message.chat.id, 'Неверный логин или пароль')
    elif dscr_txt == KeyboardInterrupt:
        msg2 = bot.send_message(message.chat.id, 'Задача с данным ID не существует')
    elif dscr_txt == HTTPError:
        msg2 = bot.send_message(message.chat.id, 'Сервер недоступен')
    else:
        msg2 = bot.send_message(message.chat.id, 'Описание задачи:')
        msg3 = bot.send_message(message.chat.id, *dscr_txt)
        logger.info(f'Данные успешно переданы пользователю id: {message.from_user.id}')


@bot.message_handler(commands=['sendcomment'])
def comment(message):
    msg = bot.send_message(message.chat.id, 'Введите логин, пароль, номер задачи и комментарий через пробел\n'
                                            'пример: login password id comment')
    bot.register_next_step_handler(msg, task_comment)


def task_comment(message):
    logger.info(f'Запрос страницы задачи пользователем id:{message.from_user.id}')
    msg1 = bot.send_message(message.chat.id, 'Ожидайте 20 сек')
    value = message.text
    task_comment_returned = task_comm(value)
    time.sleep(1)
    if task_comment_returned == ValueError:
        msg2 = bot.send_message(message.chat.id, 'Введённые данные имеют некорректный формат')
    elif task_comment_returned == KeyError:
        msg2 = bot.send_message(message.chat.id, 'Неверный логин или пароль')
    elif task_comment_returned == KeyboardInterrupt:
        msg2 = bot.send_message(message.chat.id, 'Задача с данным ID не существует')
    elif task_comment_returned == HTTPError:
        msg2 = bot.send_message(message.chat.id, 'Сервер недоступен')
    else:
        msg2 = bot.send_message(message.chat.id, f'Комментарий добавлен\n'
                                                 f'ID задачи: {task_comment_returned[0]}\n'
                                                 f'Текст комментария: {task_comment_returned[1]}')
        logger.info(f'Пользователь id:{message.from_user.id} оставил комментарий к задаче {task_comment_returned[0]}')




bot.polling(non_stop=True)
