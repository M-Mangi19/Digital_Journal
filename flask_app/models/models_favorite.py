from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.models_subject import Subject
# from flask_app.models.models_subject import subject
# favorite.subject.append( subject.Subject(subject_data))


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'digital_journal'

class Favorite:

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.item = data['item']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']