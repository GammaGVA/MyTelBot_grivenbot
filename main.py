from os import remove
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from keyboard import Keyboards, text_hello, text_help, text_description
from config import tokenBot
from weather import get_weather
from handlers import Photo
from recasepuncRUS.recasepunc import WordpieceTokenizer

bot = Bot(tokenBot)
dp = Dispatcher(bot=bot)
kb = Keyboards()


async def on_startup(_) -> None:
    print('Бот запущен!')


@dp.message_handler(commands=['start'])
@dp.message_handler(Text(equals='Рестарт 🌟'))
async def send_welcome(message: types.Message) -> None:
    # Кнопка рестарт/Начало работы
    await message.delete()
    await message.answer(text_hello, protect_content=True)
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAEICX1kBuxgStdLz9-zDJmGlJ12yiX3jAACNQADrWW8FPWlcVzFMOXgLgQ',
                           reply_markup=kb.menu())


@dp.message_handler(commands=['menu'])
async def send_welcome(message: types.Message) -> None:
    # Кнопка возврата в главное меню
    await message.delete()
    await message.answer(text='Главное меню', reply_markup=kb.menu())


@dp.message_handler(commands=['help'])
@dp.message_handler(Text(equals='Команды 🫡'))
async def send_help(message: types.Message) -> None:
    # Кнопка списка команд
    await message.delete()
    await message.answer(text=text_help,
                         parse_mode='HTML')


@dp.message_handler(commands=['description'])
@dp.message_handler(Text(equals='О боте 😜'))
async def send_description(message: types.Message) -> None:
    # Кнопка описания бота
    await message.delete()
    await message.answer(text=text_description)


@dp.message_handler(content_types='sticker')
async def sticker_id(message: types.Message) -> None:
    # Функция получения id стикеров
    await message.answer("Лови ID стикера 😜")
    await message.answer(message.sticker.file_id)


@dp.message_handler(commands=['weather'])
@dp.message_handler(Text(equals='Погода ⛅️'))
async def weather(message: types.Message) -> None:
    # Функция по выбору просмотра погоды
    await message.delete()
    await message.answer(text=' Погода в...',
                         reply_markup=kb.weather())


@dp.callback_query_handler(Text(startswith='weather_'))
async def callback_weather(callback: types.CallbackQuery) -> None:
    # Обработчик callback weather
    text_city = callback.data.split('_')[2]
    city = callback.data.split('_')[1]
    # callback.data = weather_city_text_city
    await callback.message.edit_text(text=f'Погода в {text_city} 🏘\n' + get_weather(city=city))
    await callback.answer()  # Завершаем callback


@dp.message_handler(content_types='photo')
async def message_photo(message: types.Message) -> None:
    # Функция определитель дальнейших действий с фото
    photo_id = message.photo[-1].file_id
    f = await bot.get_file(photo_id)
    path = f.file_path
    await message.answer(text='Что сделать с фото?',
                         reply_markup=kb.photo(path))


@dp.callback_query_handler(Text(startswith='phototext_@_'))
async def callback_photo(callback: types.CallbackQuery) -> None:
    # Функция вывода распознанного текста на фото
    path = callback.data.split('_@_')[1]
    #  callback.data = phototext_@_path
    await callback.message.edit_text(text='Какой язык на фото?',
                                     reply_markup=kb.photo_leng(path))


@dp.callback_query_handler(Text(startswith='leng_@_'))
async def callback_text_photo(callback: types.CallbackQuery) -> None:
    # Функция вывода распознанного текста на фото
    path = callback.data.split('_@_')[2]
    lang = callback.data.split('_@_')[1].split('/')
    # callback.data = leng_@_leng/leng_@_patg
    img = Photo(path=path, tokenBot=tokenBot)
    text_img = img.recognition_text(lang=lang)
    await callback.message.edit_text(text=text_img)


@dp.callback_query_handler(Text(startswith='photogray_@_'))
async def callback_text_photo(callback: types.CallbackQuery) -> None:
    # Функция перевода чб изображения в цвет
    await callback.answer(text='Функция пока не реализована.',
                          show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           skip_updates=True)
