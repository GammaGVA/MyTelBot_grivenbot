from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from keyboard import kb_menu, ikb_weather, ikb_photo, ikb_photo_leng, text_hello, text_help, text_description
from config import TOKEN
from weather import get_weather
from photo_handler import recognition_text_in_photo
from get_file import get_pat_photo, get_photo

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


async def on_startup(_):
    print('Бот запущен!')


@dp.message_handler(commands=['start'])
@dp.message_handler(Text(equals='Рестарт 🌟'))
async def send_welcome(message: types.Message):
    # Кнопка рестарт/Начало работы
    await message.delete()
    await message.answer(text_hello, protect_content=True)
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAEICX1kBuxgStdLz9-zDJmGlJ12yiX3jAACNQADrWW8FPWlcVzFMOXgLgQ',
                           reply_markup=kb_menu())


@dp.message_handler(commands=['menu'])
async def send_welcome(message: types.Message):
    # Кнопка возврата в главное меню
    await message.delete()
    await message.answer(text='Главное меню', reply_markup=kb_menu())


@dp.message_handler(commands=['help'])
@dp.message_handler(Text(equals='Команды 🫡'))
async def send_help(message: types.Message):
    # Кнопка списка команд
    await message.delete()
    await message.answer(text=text_help,
                         parse_mode='HTML')


@dp.message_handler(commands=['description'])
@dp.message_handler(Text(equals='О боте 😜'))
async def send_description(message: types.Message):
    # Кнопка описания бота
    await message.delete()
    await message.answer(text=text_description)


@dp.message_handler(content_types='sticker')
async def sticker_id(message: types.Message):
    # Функция получения id стикеров
    await message.answer("Лови ID стикера 😜")
    await message.answer(message.sticker.file_id)


@dp.message_handler(commands=['weather'])
@dp.message_handler(Text(equals='Погода ⛅️'))
async def weather(message: types.Message):
    # Функция по выбору просмотра погоды
    await message.delete()
    await message.answer(text=' Погода в...',
                         reply_markup=ikb_weather())


@dp.callback_query_handler(Text(startswith='weather_'))
async def callback_weather(callback: types.CallbackQuery):
    # Обработчик callback weather
    text_city = callback.data.split('_')[2]
    city = callback.data.split('_')[1]
    # callback.data = weather_city_text_city
    await callback.message.edit_text(text=f'Погода в {text_city} 🏘\n' + get_weather(city=city))
    await callback.answer()  # Завершаем callback


@dp.message_handler(content_types='photo')
async def message_photo(message: types.Message):
    # Функция определитель дальнейших действий с фото
    photo_id = message.photo[-1].file_id
    path = get_pat_photo(id=photo_id)
    await message.answer(text='Что сделать с фото?',
                         reply_markup=ikb_photo(path))


@dp.callback_query_handler(Text(startswith='phototext_@_'))
async def callback_photo(callback: types.CallbackQuery):
    # Функция вывода распознанного текста на фото
    path = callback.data.split('_@_')[1]
    #  callback.data = phototext_@_path
    await callback.message.edit_text(text='Какой язык на фото?',
                                     reply_markup=ikb_photo_leng(path))


@dp.callback_query_handler(Text(startswith='leng_@_'))
async def callback_text_photo(callback: types.CallbackQuery):
    # Функция вывода распознанного текста на фото
    path = callback.data.split('_@_')[2]
    leng = callback.data.split('_@_')[1].split('/')
    # callback.data = leng_@_leng/leng_@_patg
    await callback.message.edit_text(text=recognition_text_in_photo(get_photo(path), leng))


@dp.callback_query_handler(Text(startswith='photogray_@_'))
async def callback_text_photo(callback: types.CallbackQuery):
    # Функция перевода чб изображения в цвет
    await callback.answer(text='Функция пока не реализована.',
                          show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           skip_updates=True)
