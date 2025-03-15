import telebot
import sqlite3
from config import BOT_TOKEN
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)
#conn = sqlite3.connect('db/database.db', check_same_thread=False)
#cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def handle_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Старшие классы (10-11)")
    btn2 = types.KeyboardButton("Средние классы (5-9)")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 
                     text="Привет, {0.first_name}! Я тестовый бот для вывода расписания.".format(message.from_user), 
                     reply_markup=markup)
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Старшие классы (10-11)":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("10 класс")
        btn2 = types.KeyboardButton("11 класс")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выбери свой класс", reply_markup=markup) 

    elif message.text == "Средние классы (5-9)":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("5 класс")
        btn2 = types.KeyboardButton("6 класс")
        btn3 = types.KeyboardButton("7 класс")
        btn4 = types.KeyboardButton("8 класс")
        btn5 = types.KeyboardButton("9 класс")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, back)
        bot.send_message(message.chat.id, text="Выбери свой класс", reply_markup=markup)  

    elif message.text in ["10 класс", "11 класс", "9 класс", "8 класс", "7 класс", "6 класс", "5 класс"]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        letters = ["А", "Б"]  
        if message.text in ["7 класс", "8 класс"]:  
            letters += ["В", "Г"]
        if message.text == "9 класс":  
            letters.append("В")
        
        for letter in letters:
            markup.add(types.KeyboardButton(letter))
        
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text="Выбери букву класса", reply_markup=markup)

    elif message.text in ["А", "Б", "В", "Г"]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("На сегодня")
        btn2 = types.KeyboardButton("На завтра")
        btn3 = types.KeyboardButton("На неделю")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text=f"Вы выбрали класс с буквой {message.text}. Какое расписание вам нужно?", reply_markup=markup)

    elif message.text in ["На сегодня", "На завтра", "На неделю"]:
       
        bot.send_message(message.chat.id, text=f"Вы выбрали расписание {message.text}. Получение данных...")

    elif message.text == "Вернуться в главное меню":
        handle_message(message)  

if __name__ == "__main__":
    bot.polling(none_stop=True)
