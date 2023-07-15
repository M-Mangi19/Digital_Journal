from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'digital_journal'


class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#Create
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO users ( first_name , last_name , email, password)
                VALUE ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        results = connectToMySQL(db).query_db(query,data)
        return results
#Get All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        users = []
        for user in results:
            users.append(cls(user))
        return users
#Get One
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return cls(results[0])

#Update
    @classmethod
    def update(cls, form_data, user_id):
        query = f"UPDATE users SET first_name =%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id = {user_id}"
        results = connectToMySQL(db).query_db(query, form_data)
        return results
#Delete
    @classmethod
    def delete(cls, data):
        query = "DELETE from users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return results

#email login
    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


# REG Validators
    @staticmethod
    def register_validator(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", 'register')
            is_valid = False
        if len(data['email']) <= 0:
            flash("Email can not be blank!", 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash("Please use at least 8 characters for the password", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        connection = connectToMySQL(db)
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connection.query_db(query, data)
        if len(results) != 0:
            flash("This Email already exists! Try logging in!", 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match!", 'register')
            is_valid = False
        return is_valid
#Login Validators
    @staticmethod
    def login_validator(data):
        is_valid = True
        if len(data['email']) <= 0:
            flash("Email can not be blank!", 'login')
            is_valid = False
        if len(data['password']) < 8:
            flash("Please use at least 8 characters for the password", 'login')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'login')
            is_valid = False
        connection = connectToMySQL(db)
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connection.query_db(query, data)
        if len(results) == 0:
            flash("This Email doesn't exist! Please register!", 'login')
            is_valid = False
        return is_valid