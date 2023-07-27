from flask_app import app
from flask import Flask, request, render_template, redirect, session, flash
from flask_app.models.models_user import User
from flask_app.models.models_entry import Entry
from flask_app.models.models_favorite import Favorite
from flask_app.models.models_subject import Subject
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


#Dashboard
@app.route('/favorite_dashboard')
def favorites():
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template('favorite_dashboard.html')


#Create Item Page
@app.route('/create_favorite')
def create_favorite():
    if 'user_id' not in session:
        return redirect('/')
    else:
        subjects = Subject.get_all()
        return render_template('create_favorite.html')


#Create Item
@app.route('/create/new_favorite', methods=['POST'])
def create_new_favorite():
    if not Favorite.favorite_validator(request.form):
        return redirect('/create/favorite')
    data = {
        'title' : request.form ['title'],
        'creator' : request.form ['creator'],
        'description' : request.form ['description'],
        'subject_id' : session['subject_id']
            }
    Favorite.create(data)
    return redirect('/favorite_dashboard')

#Edit page
@app.route('/edit/favorite/<int:favorite_id>')
def edit_favorite(favorite_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : favorite_id
    }
    favorite = Favorite.get_one(data)
    return render_template('edit_favorite.html', favorite = favorite)


#Update
@app.route('/update/favorite/<int:favorite_id>', methods=['POST'])
def update_favorite(favorite_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Favorite.favorite_validator(request.form):
        return redirect('/favorite_dashboard')
    Subject.update(request.form, subject_id)
    return redirect('/favorite_dashboard')


#View


#Delete
@app.route('/delete/favorites/<int:favorite_id>')
def delete_favorite(favorite_id):
    if 'user_id' not in session:
        return redirect('/')
    Subject.delete(favorite_id)
    return redirect('/favorite_dashboard')

