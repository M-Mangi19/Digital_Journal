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
        self.creator = data['creator']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.rogue = None

#Create
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO favorites (title, creator, description, user_id)
                VALUE (%(title)s, %(creator)s,  %(description)s, %(user_id)s);
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
        query = f"UPDATE favorites SET title=%(title)s, creator=%(creator)s, description=%(description)s WHERE id = {favorite_id}"
        return connectToMySQL(db).query_db(query, form_data)
#Delete
    @classmethod
    def delete(cls, favorite_id):
        query = "DELETE from favorites WHERE id = %(id)s"
        data ={'id': favorite_id}
        results = connectToMySQL(db).query_db(query, data)
        return results


#One to Many
    @classmethod
    def get_all_favorites_with_subject(cls):
        query = "SELECT * FROM favorites JOIN subjects ON favorites.subject_id = subjects.id"
        results = connectToMySQL(db).query_db(query)
        fans = []
        for fan in results:
            fan_favorite = cls(fan)
            one_favorite_fan_info = {
                "id": fan ['subjects.id'],
                "hobby": fan ['hobby'],
                "created_at":fan ['subjects.created_at'],
                "updated_at": fan ['subjects.updated_at']
            }
            fan_favorite.rogue = Subject(one_favorite_fan_info)
            fans.append(fan_favorite)
        return writers


#One to Many

#Create and Edit Validators
    @staticmethod
    def favorite_validator(data):
            is_valid = True
            if len(data['title']) <= 0:
                flash("Title is required")
                is_valid = False
            if len(data['creator']) <= 0:
                flash("Requires content")
                is_valid = False
            if len(data['description']) <= 0:
                flash("Must have a description")
                is_valid = False
            return is_valid