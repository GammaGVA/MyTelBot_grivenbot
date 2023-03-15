import easyocr


def recognition_text_in_photo(img, leng):
    """
    Функция по сбору текста с картинки.

    :param img:
    :return:
    """
    reader = easyocr.Reader(lang_list=leng)
    result = reader.readtext(img, paragraph=True, detail=0)

    return '\n'.join(result)
