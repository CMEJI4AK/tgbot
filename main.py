import telebot
from telebot import types
import traceback
import requests
from urllib.request import urlopen
import lxml
from lxml import etree
import csv

def replace_trash(string):
  return(string.replace(' ', '').replace('\n', ''))

bot = telebot.TeleBot("7121373991:AAG_t5_GsD9UAzghR9hQJPv1Elx31jwlC70")
>
last_messages = {}

@bot.message_handler(content_types = ['photo', 'video', 'audio', 'document', 'sticker', 'animation', 'voice', 'video_note', 'story'])
def get_content(message):
    msg = bot.reply_to(message, 'Мне бы очень хотелось узнать, что там, но я не умею распознавать такого рода сообщения😔.')
    last_messages[message.chat.id] = [msg.message_id]

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Меню')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('Перезапустить бота')
    btn4 = types.KeyboardButton('Справка')
    markup.row(btn1, btn4)
    markup.row(btn2, btn3)
    markup2 = types.InlineKeyboardMarkup()
    msg = bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup = markup)
    last_messages[message.chat.id] = [msg.message_id]

@bot.message_handler(commands = ['menu'])
def menu1(message):
    file = open('./mainphoto.jpg', 'rb')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('На сегодня', url='https://www.youtube.com/watch?v=OfBgJQ5kjTA'))
    markup.add(types.InlineKeyboardButton('На неделю', url='https://www.youtube.com/watch?v=OfBgJQ5kjTA'))
    markup.add(types.InlineKeyboardButton('Выбрать категорию', url='https://www.youtube.com/watch?v=OfBgJQ5kjTA'))
    msg = bot.send_photo(message.chat.id, file,
                         caption='Я помогу найти интересные занятия в Перми, следуйте подсказкам ниже:',
                         reply_markup=markup)
    last_messages[message.chat.id] = [msg.message_id]

@bot.message_handler(commands = ['restart'])
def restart1(message):
    if message.chat.id in last_messages:
        for msg_id in last_messages[message.chat.id]:
            try:
                bot.delete_message(message.chat.id, msg_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
                traceback.print_exc()  # Для более подробного логирования ошибок
        last_messages[message.chat.id] = []  # Очищаем список ID сообщений

    msg = bot.send_message(message.chat.id, "Сессия перезапущена. Все предыдущие сообщения игнорируются. Пропишите '/start' для запуска бота")
    last_messages[message.chat.id] = [msg.message_id]
    bot.register_next_step_handler(message, start)

@bot.message_handler(commands = ['support'])
def support(message):
    support_text = """
    Наша поддержка, с помощью которой вы можете связаться с нами напрямую:
    - Telegram: @savasakii или @egorichlyadov
    - E-mail: saveliybk30@gmail.com или lyadovegorka@yandex.ru
    """
    msg = bot.send_message(message.chat.id, support_text)
    last_messages[message.chat.id] = [msg.message_id]


@bot.message_handler(func=lambda message: message.text.lower() == 'меню')
def menu2(message):
    file = open('./mainphoto.jpg', 'rb')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('На сегодня', url='https://www.youtube.com/watch?v=OfBgJQ5kjTA'))
    markup.add(types.InlineKeyboardButton('На неделю', url='https://www.youtube.com/watch?v=OfBgJQ5kjTA'))
    markup.add(types.InlineKeyboardButton('Выбрать категорию', url='https://www.youtube.com/watch?v=OfBgJQ5kjTA'))
    msg = bot.send_photo(message.chat.id, file, caption='Я помогу найти интересные занятия в Перми, следуйте подсказкам ниже:', reply_markup=markup)
    last_messages[message.chat.id] = [msg.message_id]

@bot.message_handler(func=lambda message: message.text.lower() == 'перезапустить бота')
def restart2(message):
    if message.chat.id in last_messages:
        for msg_id in last_messages[message.chat.id]:
            try:
                bot.delete_message(message.chat.id, msg_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
                traceback.print_exc()  # Для более подробного логирования ошибок
        last_messages[message.chat.id] = []  # Очищаем список ID сообщений

    msg = bot.send_message(message.chat.id, "Сессия перезапущена. Все предыдущие сообщения игнорируются. Пропишите '/start' для запуска бота")
    last_messages[message.chat.id] = [msg.message_id]
    bot.register_next_step_handler(message, start)

@bot.message_handler(func=lambda message: message.text.lower() == 'справка')
def help_message(message):
    help_text = """
    Вот справочная информация по боту:
    - Команда '/start' - начать работу с ботом.
    - Команда '/menu' - показать главное меню.
    - Команда '/support' - поддержка, где вы можете связаться с нами насчёт ваших проблем.
    - Команда '/restart' - перезапустить сессию с ботом.
    - пропишите 'Меню' - показать главное меню.
    - пропишите 'Справка' - показать справочную информацию.
    - пропишите 'Помощь' - получить руководство пользователя.
    - пропишите 'Перезапустить бота' - перезапустить сессию, чтобы предыдущие сообщения игнорировались. После этого пропишите '/start' чтобы запустить бота.
    """
    msg = bot.reply_to(message, help_text)
    last_messages[message.chat.id] = [msg.message_id]

@bot.message_handler(func=lambda message: message.text.lower() == 'помощь')
def help_document(message):
    with open('Руководство пользователя.pdf', 'rb') as help_file:
        msg = bot.send_message(message.chat.id, 'В этом файле находится руководство пользователя, с помощью него вы сможете решите свою проблему')
        bot.send_document(message.chat.id, help_file)
        last_messages[message.chat.id] = [msg.message_id]


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    msg = bot.reply_to(message, "Что то вы не то нажали, пропишите '/start'")


    if message.chat.id not in last_messages:
        last_messages[message.chat.id] = []
    last_messages[message.chat.id].extend([message.message_id, msg.message_id])

# bot.polling(none_stop=True)

url = 'https://aviabilety-loukoster.ru/raspisanie-rejsov'
response = urlopen(url)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)
# Открываем страницу и записываем в файл
# Для сайтов с защитой от программного обращения, можно просто сохранить страницу на диск
url = 'https://aviabilety-loukoster.ru/raspisanie-rejsov'
headers = {'Content-Type': 'text/html',}
response = requests.get(url, headers=headers)
html = response.text
with open ('Yandex2.html', 'w') as f:
    f.write(html)

local = 'file:///content/pobeda2.html'
response = urlopen(local)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)
# При помощи Xpath путей достаем необходимую информацию, записываем в list(list())
result = list()

for root_element in (tree.xpath('/html/body/div/div/div[1]/article/div[2]/div[2]/ul/li')):
  #print(replace_trash(root_element.xpath('h2/text()')[0]))
  source = replace_trash(root_element.xpath('h2/text()')[0]).split('—')[0]
  # div/table/tbody/tr[2]/td[1]
  for row in root_element.xpath('div/table/tbody/tr'):
    flight = row.xpath('td[1]/text()')
    # source = flight.split('-')[0]
    if len(flight) > 0:
      flight = replace_trash(flight[0])
      dest = replace_trash(row.xpath('td[2]/text()')[0])
      start_date = replace_trash(row.xpath('td[3]/text()')[0])
      days = row.xpath('td[4]/text()')[0].replace('\n', '')
      depart = replace_trash(row.xpath('td[5]/text()')[0])
      arrival = replace_trash(row.xpath('td[6]/text()')[0])
      # print(f'{flight} - {source} - {dest} - {start_date} - {days} - {depart} - {arrival}')
      result.append([flight, source, dest, start_date, days, depart, arrival])


# Записываем в результат в таблицу в формате CSV
with open('Yandex.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['flight', 'source', 'dest', 'start_date', 'days', 'depart', 'arrival'])
    for row in result:
        writer.writerow(row)