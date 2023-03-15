import requests
from config import TOKEN
import io
from PIL import Image


def get_pat_photo(id: str, __TOKEN=TOKEN):
    URL_file = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={id}'
    response = requests.get(url=URL_file)
    img_path = response.json()['result']['file_path']
    return img_path


def get_photo(img_path: str, __TOKEN=TOKEN):
    URL_file = f'https://api.telegram.org/file/bot{TOKEN}/{img_path}'
    img = requests.get(URL_file).content
    img = Image.open(io.BytesIO(img))
    # BytesIO - Buffered I/O implementation using an in-memory bytes buffer.
    return img


if __name__ == '__main__':
    id = 'AgACAgIAAxkBAAIH9GQO2GLifshuLxd4ZnHF85C7mTsgAALJxzEbktxwSP3iymTcSzNCAQADAgADbQADLwQ'
    path = get_pat_photo(id)
    print(path)
    file = get_photo(path)
    print(type(file))
    print(file)
