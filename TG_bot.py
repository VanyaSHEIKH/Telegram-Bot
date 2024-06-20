import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text="Чтобы начать работу введите команду /values для просмотра доступных вылют, /help - помощь в вводе команд."
    bot.reply_to(message,text)

@bot.message_handler(commands=["values"])
def values(message:telebot.types.Message):
    text="Доступные валюты:"
    for key in keys.keys():
        text='\n'.join((text,key))
    bot.reply_to(message,text)

@bot.message_handler(commands=["help"])
def help(message: telebot.types.Message):
    text="Конвертирование валют должно происходить следующим образом:\
\nПервым сообщением необходимо ввести название валюты, которую необходимо конвертировать.\
Далее необходимо ввести название валюты, в которую необходимо конвертировать первую.\
И наконец добавить количество конвертируемой валюты.\
\nНапример: Bitcoin -> Dollar -> 2\
\nРезультат: Стоимость 2 Bitcoin в Dollar составляет - 66950.01 ."
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Указан лишний параметр. Проверьте правильность написания команды.')
        quote, base, amount = values
        total_base = CryptoConverter.converter(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} составляет - {total_base}'
        bot.send_message(message.chat.id, text)

bot.infinity_polling()
