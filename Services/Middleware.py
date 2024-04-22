import random
import string
import time
from Models.Provides import *
from unidecode import unidecode


def convert_to_ascii(text):
    text_convert = unidecode(text)
    text_replace = text_convert.replace(' ', '-')
    return text_replace.lower()


def generate_custom_id(prefix):
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{timestamp}-{random_chars}"


def get_province(code):
    province = Province.query.filter_by(code=code).first()
    return province.name


def get_district(code):
    district = District.query.filter_by(code=code).first()
    return district.name


def get_ward(code):
    ward = Ward.query.filter_by(code=code).first()
    return ward.name
