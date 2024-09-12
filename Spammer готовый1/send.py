from pyrogram import Client
from pyrogram.errors import FloodWait, BadRequest, Flood, InternalServerError
from time import sleep
from sys import stderr, exit
from loguru import logger
from msvcrt import getch
from os import system
import time
import random
import re

def clear(): return system('cls')

api = open('apis.txt').read().split(' ') # api telegram

SESSION_NAME = input('Введите номер телефона: ')
logger.remove()
logger.add(stderr,
           format='<white>{time:HH:mm:ss}</white> | '
                  '<level>{level: <8}</level> | '
                  '<cyan>{line}</cyan> - '
                  '<white>{message}</white>')

app = Client(SESSION_NAME, int(api[0]), api[1])

with open('Чаты.txt', 'r', encoding='utf-8') as file:
    chat_list = [row.strip() for row in file]

def https_delete(listname):
    for https in range(len(listname)):
        listname[https] = re.sub('https://t.me/', '', listname[https])

def send_message(current_chat):
    for _ in range(3):
        try:
            with app:
                # Читаем все строки из файла сообщений
                with open('Сообщение.txt', 'r', encoding='utf-8') as message_file:
                    all_lines = message_file.readlines()

                # Случайно выбираем одну строку из списка
                selected_line = random.choice(all_lines)

                # Отправляем выбранную строку как сообщение
                app.send_message(current_chat, selected_line.strip())

        except FloodWait as error:
            logger.info(f'{current_chat} | FloodWait: {error.x}')
            sleep(error.x)

        except Flood:
            pass

        except BadRequest as error:
            logger.error(f'{current_chat} | {error}')

        except InternalServerError as error:
            logger.error(f'{current_chat} | {error}')

        except Exception as error:
            logger.error(f'{current_chat} | {error}')

        else:
            logger.success(f'{current_chat} | The message was successfully sent')
            return

    with open('errors_send_message.txt', 'a', encoding='utf-8') as file:
        file.write(f'{current_chat}\n')

def join_chat(current_chat):
    for _ in range(3):
        try:
            with app:
                app.join_chat(current_chat)

        except FloodWait as error:
            logger.info(f'{current_chat} | FloodWait: {error.x}')
            sleep(error.x)

        except Flood:
            pass

        except BadRequest as error:
            logger.error(f'{current_chat} | {error}')

        except InternalServerError as error:
            logger.error(f'{current_chat} | {error}')

        except Exception as error:
            logger.error(f'{current_chat} | {error}')

        else:
            logger.success(f'{current_chat} | Successfully logged into the chat')
            return

    with open('errors_join_chat.txt', 'a', encoding='utf-8') as file:
        file.write(f'{current_chat}\n')

if __name__ == '__main__':
    https_delete(chat_list)
    print('Вступление в чаты...')
    for current_chat in chat_list:
        join_chat(current_chat)

    min_delay = int(input('Введите минимальную задержку (в секундах): '))
    max_delay = int(input('Введите максимальную задержку (в секундах): '))
    number_of_sends = int(input('Сколько раз вы хотите отправить сообщение в чаты?: '))

    for current_chat in chat_list:
        for sending_messages in range(number_of_sends):
            send_message(current_chat)
            # Задержка от min_delay до max_delay секунд
            random_delay = random.randint(min_delay, max_delay)
            time.sleep(random_delay)

    print('Работа успешно завершена!')
    print('\nДля выхода нажмите любую клавишу.')
    getch()
    exit()
