import random
import string
import time

from unidecode import unidecode


def convert_to_ascii(text):
    text_convert = unidecode(text)
    text_replace = text_convert.replace(' ', '-')
    return text_replace.lower()


def generate_custom_id(prefix):
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{timestamp}-{random_chars}"
