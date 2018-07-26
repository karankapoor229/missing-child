from mongoengine import *
import string
import random


class Child(Document):
    child_id = StringField(required=True, unique=True)
    child_name = StringField(required=True)
    age = IntField(required=True)
    place_of_missing = StringField()
    date_of_missing = StringField
    guardian_name = StringField(required=True)
    phone_number = StringField(required=True)
    is_lost = BooleanField(default=True)
    image_url = StringField()
    image_path = StringField()
    connect(db='child', host='localhost:27017', alias='default')

    @staticmethod
    def generate_id():
        charset = string.ascii_lowercase + string.ascii_letters
        return "".join([random.choice(charset) for _ in range(10)])
