from flask_app import app
from flask import Flask, request, render_template, redirect, session, flash
from flask_app.models.models_user import User
from flask_app.models.models_entry import Entry
from flask_app.models.models_favorite import Favorite
from flask_app.models.models_subject import Subject
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


#Subject Archive Page
@app.route('/subject')
def subject():
    if 'user_id' not in session:
        return redirect('/')
    else:
        user_data = {
            'id' : session['user_id']
        }
        user = User.get_one(user_data)
        subjects = Subject.get_all_subjects_with_user()
        return render_template('subject_archive.html', subjects = subjects, user = user)

#Create Subject page
@app.route('/create/subject')
def create_subject():
    if 'user_id' not in session:
        return redirect('/')
    else:
        user_data = {
            'id' : session['user_id']
        }
        return render_template('create_subject.html')



#Create Subject
@app.route('/create/new_subject', methods=['POST'])
def create_new_subject():
    if not Subject.subject_validator(request.form):
        return redirect('/create/subject')
    data = {
        'hobby' : request.form['hobby'],
        'user_id' : session['user_id']
    }
    Subject.create(data)
    return redirect('/create/subject')

#Edit page
@app.route('/edit/<int:subject_id>')
def edit_subject(subject_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : subject_id
    }
    # entry = Entry.get_one(data)
    return render_template('edit_subject.html')

# Update
@app.route('/update/subject/<int:subject_id>', methods=['POST'])
def update_subject(subject_validator_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Subject.subject_validator(request.form):
        return redirect('/subject')
    Subject.update(request.form, subject_id)
    return redirect('/subject')

