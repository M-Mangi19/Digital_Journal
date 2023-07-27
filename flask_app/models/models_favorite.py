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


#Create
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO favorites (title, item, description, user_id)
                VALUE (%(title)s, %(item)s,  %(description)s, %(user_id)s);
                """
        results = connectToMySQL(db).query_db(query, data)
        return results

#Get All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM favorites;"
        results = connectToMySQL(db).query_db(query)
        favorites = []
        for favorite in results:
            favorites.append(cls(favorite))
        return favorites

#Get One
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM favorites WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return cls(results[0])


#Update
    @classmethod
    def update(cls, form_data, favorite_id):
        query = f"UPDATE favorites SET title=%(title)s, item=%(item)s, description=%(description)s WHERE id = {favorite_id}"
        return connectToMySQL(db).query_db(query, form_data)
#Delete
    @classmethod
    def delete(cls, favorite_id):
        query = "DELETE from favorites WHERE id = %(id)s"
        data ={'id': favorite_id}
        results = connectToMySQL(db).query_db(query, data)
        return results


# #One to Many
#     @classmethod
#     def get_all_entries_with_user(cls):
#         query = "SELECT * FROM entries JOIN users ON entries.user_id = users.id ORDER BY entries.id DESC"
#         results = connectToMySQL(db).query_db(query)
#         writers = []
#         for writer in results:
#             writer_entry = cls(writer)
#             one_entry_writer_info = {
#                 "id": writer['users.id'],
#                 "first_name": writer['first_name'],
#                 "last_name": writer['last_name'],
#                 "email": writer['email'],
#                 "password": writer['password'],
#                 "created_at":writer['users.created_at'],
#                 "updated_at": writer['users.updated_at']
#             }
#             writer_entry.creator = User(one_entry_writer_info)
#             writers.append(writer_entry)
#         return writers


#One to Many

#Create and Edit Validators
    @staticmethod
    def favorite_validator(data):
            is_valid = True
            if len(data['title']) <= 0:
                flash("Title is required")
                is_valid = False
            if len(data['item']) <= 0:
                flash("Requires content")
                is_valid = False
            if len(data['description']) < 3:
                flash("Must have a description")
                is_valid = False
            return is_valid