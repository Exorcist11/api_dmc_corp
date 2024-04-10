from unidecode import unidecode


def convert_to_ascii(text):
    text_convert = unidecode(text)
    text_replace = text_convert.replace(' ', '-')
    return text_replace.lower()
