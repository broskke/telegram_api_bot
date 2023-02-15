import telebot
import json
import requests

from todo_requests import GetAllMixin, CreateMixin, RetrieveMixin, UpdateMixin,DeleteMixin
from telebot import types

class Interface(GetAllMixin,CreateMixin, RetrieveMixin,UpdateMixin,DeleteMixin):
    pass
    
interface = Interface()
HOST = 'http://3.67.196.232/'

token = '6289145154:AAEWcERsCeNZcJktxCrv0_4pyLoWGEhGOvA'

bot = telebot.TeleBot(token)

inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
inline_read = types.InlineKeyboardButton("просмотр", callback_data='read')
inline_create = types.InlineKeyboardButton("создание", callback_data='create')
inline_update = types.InlineKeyboardButton("обновление", callback_data='update')
inline_delete = types.InlineKeyboardButton("удаление", callback_data='delete')
inline_keyboard.add(inline_read,inline_create,inline_update,inline_delete)

inline_keyboard1 = types.InlineKeyboardMarkup(row_width=2)
inline_get_all_todo = types.InlineKeyboardButton("просмотр всех задач", callback_data='all_read')
inline_retrieve_todo = types.InlineKeyboardButton("просмотр выбранной задачи", callback_data='retrive')
inline_keyboard1.add(inline_get_all_todo,inline_retrieve_todo)

inline_keyboard_menu = types.InlineKeyboardMarkup(row_width=1)
inline_menu = types.InlineKeyboardButton('в меню',callback_data='menu')
inline_keyboard_menu.add(inline_menu)


@bot.message_handler(commands=['start','hi'])
def start_message(message: types.Message):
    bot.send_photo(message.chat.id,photo = open('task.png','rb'))
    bot.send_message(message.chat.id, 'Здраствуйте, вы можете выбрать один из вариантов', reply_markup=inline_keyboard)

#read чтение 
@bot.callback_query_handler(func=lambda callback: callback.data == 'read')
def read(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id,'какой вариант вы хотите выбрать?',reply_markup=inline_keyboard1 )

@bot.callback_query_handler(func=lambda callback: callback.data == 'all_read')
def all_read(callback: types.CallbackQuery):
    result = json.dumps(interface.get_all_todos(HOST),indent=4)
    bot.send_message(callback.message.chat.id,f'ваши задачи {result}',reply_markup=inline_keyboard_menu)
    
@bot.callback_query_handler(func=lambda callback: callback.data == 'retrive')
def retrive(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id,f'введите число')
    @bot.message_handler(content_types= ['text'])
    def start(message: int):
        response = message.text
        result = json.dumps(interface.retrieve_todo(HOST,response),indent = 4 )
        bot.send_message(message.chat.id,f'выбранная задача {result}',reply_markup=inline_keyboard_menu)



@bot.callback_query_handler(func=lambda callback: callback.data == 'create')
def create(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id,f'Введите название задачи')
    @bot.message_handler(content_types= ['text'])
    def start(message: str):
        data={'title': message.text}
        interface.creat_todo(HOST, data)
        bot.send_message(message.chat.id,'задача создана',reply_markup=inline_keyboard_menu)



@bot.callback_query_handler(func=lambda callback: callback.data == 'update')
def update(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id,f'Введите число')
    list_=[]
    @bot.message_handler(content_types= ['text'])
    
    def start(message: str):
        response = message.text
        list_.append(response)
        msg = bot.send_message(message.chat.id,'Введите новое название задачи')
        bot.register_next_step_handler(msg, new_name)
    def new_name(message):
        title = message.text
        data = {'title':title}
        interface.update_todo(HOST,list_[0], data)
        bot.send_message(message.chat.id,'задача обнавлена',reply_markup=inline_keyboard_menu)




@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
def delete(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id,f'введите число')
    @bot.message_handler(content_types= ['text'])
    def start(message: int):
        response = message.text
        interface.delete_todo(HOST,response)
        bot.send_message(message.chat.id,'задача удалена',reply_markup=inline_keyboard_menu)


#забрасывает вглавное меню
@bot.callback_query_handler(func=lambda callback: callback.data == 'menu')
def menu(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id,'вы вернулись в меню',reply_markup=inline_keyboard)


bot.polling()


#TODO сделать возврат в меню с помощью кнопок
#TODO решить проблему с апдейтом