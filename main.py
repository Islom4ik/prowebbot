from telebot import TeleBot
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import time
import os
load_dotenv()



bot = TeleBot(os.getenv("BOT_TOKEN"), parse_mode='HTML')

data = {

}


@bot.message_handler(commands=['start', 'help'])
def first(ctx: Message):
    if ctx.text == '/start':
        try:
            if data[f"{ctx.from_user.id}"]:
                if data[f"{ctx.from_user.id}"]["started"] == True:
                    bot.delete_message(ctx.chat.id, ctx.message_id)
                    return
        except Exception as KeyError:
            data[f"{ctx.from_user.id}"] = {"started": False, "dstep": 0}
        kbstart = InlineKeyboardMarkup()
        kbstart.add(InlineKeyboardButton('Начать диалог 🪧', callback_data='startdialogue'))
        bot.send_message(ctx.chat.id, f'Добрый день, {ctx.from_user.first_name}!\n\nДля того чтобы начать диалог нажмите на кнопку ниже ⬇', reply_markup=kbstart)

@bot.callback_query_handler(func=lambda call: True)
def cbhadler(ctx: Message):
    if ctx.data == 'startdialogue':
        bot.send_message(ctx.from_user.id, 'Диалог начат 🟢')
        bot.answer_callback_query(callback_query_id=ctx.id, show_alert=False, text='Запускаю...')
        bot.delete_message(ctx.from_user.id, ctx.message.id)
        data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
        bot.send_message(ctx.from_user.id, 'Привет! Меня зовут Ban, а как тебя?')
        data[f"{ctx.from_user.id}"]['started'] = True

@bot.message_handler(content_types=['text'])
def text_handling(ctx: Message):
    try:
        if data[f'{ctx.from_user.id}']['started'] == True:
            if data[f"{ctx.from_user.id}"]['dstep'] == 1:
                bot.send_message(ctx.chat.id,
                                 f'{ctx.text.title()}, рад знакомству! Какая у вас сейчас погода? У нас вот ясная 🤩.')
                data[f"{ctx.from_user.id}"]['name'] = ctx.text.title()
                data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
            elif data[f"{ctx.from_user.id}"]['dstep'] == 2:
                bot.send_message(ctx.chat.id,
                                 f'Ого. Давай я попробую отгадать что ты загадал из сделующих 3-х фрукт:\n1 - Арбуз\n2 - Дыня\n3 - Персик\n\nЕсли уже загадал, напиши слово "Загадал"')
                data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
            elif data[f"{ctx.from_user.id}"]['dstep'] == 3:
                if ctx.text.lower() == 'загадал':
                    bot.send_message(ctx.chat.id, f'Хммм...', reply_to_message_id=ctx.message_id)
                    time.sleep(1)
                    bot.send_message(ctx.chat.id, f'Ты загадал... <tg-spoiler>Арбуз!? (Да / Нет)</tg-spoiler>')
                    data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
                else:
                    bot.send_message(ctx.chat.id, f'Если ты уже загадал, напиши слово "Загадал"',
                                     reply_to_message_id=ctx.message_id)
            elif data[f"{ctx.from_user.id}"]['dstep'] == 4:
                if ctx.text.lower() == 'да':
                    bot.send_message(ctx.chat.id, f'Ну я же экстрасенс 😎', reply_to_message_id=ctx.message_id)
                    time.sleep(1)
                    bot.send_message(ctx.chat.id,
                                     f'Попробуй теперь ты угадай. Я загадал, действуй! (Просто назовите фрукт)')
                    data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
                elif ctx.text.lower() == 'нет':
                    bot.send_message(ctx.chat.id, f'Эхх жаль 😔', reply_to_message_id=ctx.message_id)
                    time.sleep(1)
                    bot.send_message(ctx.chat.id,
                                     f'Попробуй теперь ты угадай. Уверен ты тоже не сможешь угадать! Я загадал, действуй! (Просто назовите фрукт)')
                    data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
                else:
                    bot.send_message(ctx.chat.id, f'Да / Нет', reply_to_message_id=ctx.message_id)
            elif data[f"{ctx.from_user.id}"]['dstep'] == 5:
                if ctx.text.lower() == 'персик':
                    bot.send_message(ctx.chat.id, f'Кааак? Как ты это сделал? Ты угадал!',
                                     reply_to_message_id=ctx.message_id)
                    time.sleep(1)
                    bot.send_message(ctx.chat.id, f'Слов нет! Ты занимаешься каким либо спортом?')
                    data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
                else:
                    bot.send_message(ctx.chat.id, f'Хехехехехе, неа! Не угадал)', reply_to_message_id=ctx.message_id)
                    time.sleep(1)
                    bot.send_message(ctx.chat.id, f'Ладно! Ты занимаешься каким либо спортом?')
                    data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
            elif data[f"{ctx.from_user.id}"]['dstep'] == 6:
                bot.send_message(ctx.chat.id,
                                 f'Я вот занимаюсь спячкой) Это наш национальный вид спорта) А кем ты хочешь стать в будушем(Или уже стал)?',
                                 reply_to_message_id=ctx.message_id)
                data[f"{ctx.from_user.id}"]['dstep'] = data[f"{ctx.from_user.id}"]['dstep'] + 1
            elif data[f"{ctx.from_user.id}"]['dstep'] == 7:
                bot.send_message(ctx.chat.id,
                                 f'Ну молодец молодец... ладно мне пора идти на занятия) Удачи тебе... чемпион!')
                time.sleep(2)
                bot.send_message(ctx.chat.id, f'Диалог окончен 🔴')
                data[f"{ctx.from_user.id}"]['dstep'] = 0
                data[f"{ctx.from_user.id}"]['started'] = False
    except Exception as e:
        return



bot.infinity_polling(skip_pending=True)