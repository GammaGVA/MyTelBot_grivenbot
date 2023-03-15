import requests
from bs4 import BeautifulSoup
from config import headers  # Взял свои куки и заголовки, https://curlconverter.com/ - удобный сервис для cURL


def __separator(period: str):
    #  Функция определяющая разделитель между блоками периодов погоды.
    if period == 'ночью':
        separator = '🌑🌘🌗🌖🌕🌔🌓🌒🌑'
    elif period == 'утром':
        separator = '🌄🌄🌄🌄🌄🌄🌄🌄'
    elif period == 'вечером':
        separator = '🌉🌉🌉🌉🌉🌉🌉🌉'
    elif period == 'днем':
        separator = '🌤🌥⛅️☀️☀️⛅️🌥🌤'
    else:
        separator = '☁️☁️☁️☁️☁️☁️☁️☁️'
    return separator


def get_weather(city):
    """Парсер погоды с сайта https://pogoda.mail.ru/

    :param city:
    :return text_weather:"""
    try:
        response = requests.get(f'https://pogoda.mail.ru/prognoz/{city}/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        card = soup.find('div', class_="information")  # Вся карта данных
        # Ниже текущие данные
        temperature = 'Температура сейчас ' + card.find('div', class_="information__content__temperature").text.strip()
        # Температура ()
        date = card.find('div', class_="information__header__left__date").text.strip().title() + ' 🗓🕜'  # Дата и время

        all_point = card.find_all('div', class_="information__content__additional__item")  # Всё остальное
        # Кроме текущей температуры и времени, все остальные блоки одноимённы.

        feels = all_point[0].text.strip().title() + ' 😶‍🌫️'  # Температура ощущается как
        weather = 'На улице ' + all_point[1].text.strip() + ' 👀'  # Облачно/пасмурно/дымка/итд.
        pressure = 'Давление ' + ' '.join(all_point[2].text.strip().split())  # Давление
        humidity = ' '.join(all_point[3].text.strip().split()) + ' 💦'  # Влажность
        wind = ' '.join(all_point[4].text.strip().split()) + ' 🌬'  # Ветер

        text_weather = f'{date}\n{weather}\n{temperature}\n{feels}\n{wind}\n{pressure}\n{humidity}'

        if all_point[-1].text.count(':') == 2:
            # Не всегда есть время восхода и заката, но это единственный элемент с двоеточиями и всегда последний
            time = all_point[-1].text.strip().split()
            # Общий список иногда 5 элементов содержит, иногда 6. Но всегда последний.
            sunrise = 'Время восхода ' + time[0] + ' 🌅'
            sunset = 'Время заката ' + time[1] + ' 🌃'
            text_weather += f'\n{sunrise}\n{sunset}'

        # Данные на потом, недалёкое будущие.
        right = card.find('div', class_="information__content__wrapper_right")  # Правая часть карты данных
        morning_evening = right.find_all('div', class_="information__content__period")
        morning_period = morning_evening[0].find('div', class_="information__content__period__title").text.strip()
        evening_period = morning_evening[1].find('div', class_="information__content__period__title").text.strip()
        # Периоды утро/день/вечер/ночь

        morning_temp = morning_evening[0].find('div', class_="information__content__period__temperature").text.strip()
        evening_temp = morning_evening[1].find('div', class_="information__content__period__temperature").text.strip()
        # Температуры

        morning_block = morning_evening[0].find_all('div', class_="information__content__period__additional__item")
        morning_pressure = 'Давление ' + morning_block[0].text.strip()
        morning_wind = 'Скорость ветра ' + morning_block[2].text.strip()
        morning_deposition = 'Вероятность осадков ' + morning_block[4].text.strip()

        text_weather += f'\n{__separator(morning_period)}\n{morning_period.title()} {morning_temp}\n{morning_pressure}\
        \n{morning_wind}\n{morning_deposition}'

        evening_block = morning_evening[1].find_all('div', class_="information__content__period__additional__item")
        evening_pressure = 'Давление ' + evening_block[0].text.strip()
        evening_wind = 'Скорость ветра ' + evening_block[2].text.strip()
        evening_deposition = 'Вероятность осадков ' + evening_block[4].text.strip()

        text_weather += f'\n{__separator(evening_period)}\n{evening_period.title()} {evening_temp}\n{evening_pressure}\
        \n{evening_wind}\n{evening_deposition}'

        return text_weather

    except Exception as ex:
        return f'Ошибка получения данных\n{ex}'


if __name__ == '__main__':
    print(get_weather(city='anna'))
