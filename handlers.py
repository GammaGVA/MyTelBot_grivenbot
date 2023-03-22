import requests
import io
from PIL import Image
import easyocr
from transformers import logging
from recasepuncRUS.recasepunc import CasePuncPredictor
from recasepuncRUS.recasepunc import WordpieceTokenizer
from recasepuncRUS.recasepunc import Config


class Photo(object):
    def __init__(self, path, tokenBot):
        URL_file = f'https://api.telegram.org/file/bot{tokenBot}/{path}'
        img = requests.get(URL_file).content
        self.img = Image.open(io.BytesIO(img))
        # BytesIO - Buffered I/O implementation using an in-memory bytes buffer.
        # Сохранили в буфер картинку

    def recognition_text(self, lang: list) -> str:
        """

        :param lang:  Список
        :return:
        """
        reader = easyocr.Reader(lang_list=lang)
        text = reader.readtext(self.img, paragraph=True, detail=0)
        logging.set_verbosity_error()

        if lang == 'ru':
            # Если распознавание чисто русского языка, то пробуем указать пунктуацию.
            predictor = CasePuncPredictor('recasepuncRUS/checkpoint', lang="ru")
            results = ""
            for words in text:
                tokens = list(enumerate(predictor.tokenize(words)))
                for token, case_label, punc_label in predictor.predict(tokens, lambda x: x[1]):
                    prediction = predictor.map_punc_label(predictor.map_case_label(token[1], case_label), punc_label)
                    if token[1][0] != '#':
                        results = results + ' ' + prediction
                    else:
                        results = results + prediction
                results += '\n'

            return results
        return '\n'.join(text)


if __name__ == '__main__':
    pass
