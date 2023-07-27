from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# from flask_app.models.models_subject import Subject
from flask_app.models.models_user import User
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'digital_journal'

class Subject:

    def __init__(self,data):
        self.id = data['id']
        self.hobby = data['hobby']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

#Create
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO subjects (hobby, user_id)
                VALUE (%(hobby)s, %(user_id)s);
                """
        results = connectToMySQL(db).query_db(query, data)
        return results

#Get All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM subjects;"
        results = connectToMySQL(db).query_db(query)
        subjects = []
        for subject in results:
            subjects.append(cls(subject))
        return subjects

#Get One
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM subjects WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return cls(results[0])


#Update
    @classmethod
    def update(cls, form_data, subject_id):
        query = f"UPDATE subjects SET hobby=%(hobby)s WHERE id = {subject_id}"
        return connectToMySQL(db).query_db(query, form_data)
#Delete
    @classmethod
    def delete(cls, subject_id):
        query = "DELETE from subjects WHERE id = %(id)s"
        data ={'id': subject_id}
        results = connectToMySQL(db).query_db(query, data)
        return results


# One to Many
    @classmethod
    def get_all_subjects_with_user(cls):
        query = "SELECT * FROM subjects JOIN users ON subjects.user_id = users.id"
        results = connectToMySQL(db).query_db(query)
        creators = []
        for creator in results:
            creator_subject = cls(creator)
            one_subject_creator_info = {
                "id":creator['users.id'],
                "first_name":creator['first_name'],
                "last_name":creator['last_name'],
                "email":creator['email'],
                "password":creator['password'],
                "created_at":creator['users.created_at'],
                "updated_at":creator['users.updated_at']
            }
            creator_subject.author = User(one_subject_creator_info)
            creators.append(creator_subject)
        return creators


#One to Many

#Create and Edit Validators
    @staticmethod
    def subject_validator(data):
            is_valid = True
            if len(data['hobby']) <= 0:
                flash("Must have content")
                is_valid = False
            return is_valid