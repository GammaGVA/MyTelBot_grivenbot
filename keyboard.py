from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:
    """
    Клас клавиатур.
    """

    def menu(self) -> ReplyKeyboardMarkup:
        # Меню
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        _help = KeyboardButton(text='Команды 🫡')
        _description = KeyboardButton(text='О боте 😜')
        _restart = KeyboardButton(text='Рестарт 🌟')
        _weather = KeyboardButton(text='Погода ⛅️')
        return kb.add(_help, _description, _restart).add(_weather)

    # Погода
    def weather(self) -> InlineKeyboardMarkup:
        # Погода
        ikb = InlineKeyboardMarkup(row_width=2)
        _voronezh = InlineKeyboardButton(text='Воронеже', callback_data='weather_voronezh_Воронеже')
        _anna = InlineKeyboardButton(text='Анне', callback_data='weather_anna_Анне')
        return ikb.add(_voronezh, _anna)


# Текст/информация кнопок
# Приветствие
text_hello = """Привет!🫡
Я твои инструменты.
Надеюсь что буду полезен."""

# Кнопка help
text_help = """<b>/start</b> - <i>Перезапустить бота</i>
<b>/menu</b> - <i>Возврат в главное меню</i>
<b>/help</b> - <i>Список команд</i>
<b>/description</b> - <i>Описание</i>
<b>/weather</b> - <i>Погода</i>

Если прислать мне стикер, я пришлю тебе его ID.
Если прислать фото, то можно распознать текст на нём."""

# Кнопка description
text_description = """Я бот инструмент🤖🔧.
Сейчас я умею выдавать id стикеров, определять текст на картинках и показывать погоду в Воронеже и Анне.
На этом я не остановлюсь, я буду развиваться!😉"""
