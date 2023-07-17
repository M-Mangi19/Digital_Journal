from flask_app import app
from flask import Flask, request, render_template, redirect, session, flash
from flask_app.models.models_user import User
from flask_app.models.models_entry import Entry
from flask_app.models.models_favorite import Favorite
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


#Homepage
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

#Create Journal Page
@app.route('/create/entry')
def create_entry():
    return render_template('journal_entry.html')