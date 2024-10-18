import telebot
import logging
import time
from urllib.error import HTTPError
from task_view import tasks


logging.basicConfig(filename='bot.log', level=logging.INFO, encoding='utf-8',
                    format='%(levelname)s %(asctime)s: %(message)s (Line: %(lineno)s - %(filename)s', filemode='w')

logger = logging.getLogger(__name__)
handler = logging.FileHandler('bot.log', encoding='utf-8')
formatter = logging.Formatter('%(levelname)s %(asctime)s: %(message)s (Line: %(lineno)s - %(filename)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Запуск')


@bot.message_handler(commands=['mytasks'])
def my_tasks(message):
    msg = bot.send_message(message.chat.id, 'Введите логин и пароль через пробел')
    bot.register_next_step_handler(msg, task_list)


def task_list(message):
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
        logger.info('Данные переданы пользователю')


# @bot.message_handler(commands=['taskinfo'])
# def task_info(message):
#     msg = bot.send_message(message.chat.id, 'Введите логин и пароль через пробел')
#     bot.register_next_step_handler(msg, task_description)
#
# def task_description():
#



bot.polling(non_stop=True)

