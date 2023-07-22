from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.models_user import User
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'digital_journal'

class Entry:

    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']

#Create
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO entries (content, date, user_id)
                VALUE (%(content)s, %(date)s, %(user_id)s);
                """
        results = connectToMySQL(db).query_db(query, data)
        return results

#Get All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM entries;"
        results = connectToMySQL(db).query_db(query)
        entries = []
        for entry in results:
            entries.append(cls(entry))
        return entries

#Get One
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM entries WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return cls(results[0])



#Update
    @classmethod
    def update(cls, form_data, entry_id):
        query = f"UPDATE entries SET content=%(content)s, date=%(date)s WHERE id = {show_id}"
        return connectToMySQL(db).query_db(query, form_data)
#Delete
    @classmethod
    def delete(cls, entry_id):
        query = "DELETE from entries WHERE id = %(id)s"
        data ={'id': entry_id}
        results = connectToMySQL(db).query_db(query, data)
        return results


#One to Many

#One to Many

#Create and Edit Validators
    @staticmethod
    def entry_validator(data):
            is_valid = True
            if len(data['content']) <= 0:
                flash("Must have content")
                is_valid = False
            if len(data['date']) <= 0:
                flash("Date is required")
                is_valid = False
            return is_valid