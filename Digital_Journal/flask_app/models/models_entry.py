from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.models_user import User
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'digital_journal'

class Entry:

    def __init__(self,data):
        self.id = data['id']
        self.content = content['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']