from flask_app import app
from flask import Flask, request, render_template, redirect, session, flash
from flask_app.models.models_user import User
from flask_app.models.models_entry import Entry
from flask_app.models.models_favorite import Favorite
from flask_app.models.models_subject import Subject
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


#Homepage
@app.route('/homepage')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : session['user_id']
        }
        user = User.get_one(data)
        return render_template('homepage.html', user = user)

#Dashboard
@app.route('/journal_dashboard')
def journal_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id' : session['user_id']
        }
        user = User.get_one(data)
        entries = Entry.get_all_entries_with_user()
        return render_template('journal_dashboard.html', user = user, entries = entries)

#Create Entry Page
@app.route('/create/entry')
def create_entry():
    if 'user_id' not in session:
        return redirect('/')
    else:
        user_data = {
            'id' : session['user_id']
        }
        user = User.get_one(user_data)
        entries = Entry.get_all_entries_with_user()
        return render_template('create_journal_entry.html', user = user, entries = entries)

#Create Entry
@app.route('/create/new_entry', methods=['POST'])
def create_new_entry():
    if not Entry.entry_validator(request.form):
        return redirect('/create/entry')
    data = {
        'heading' : request.form['heading'],
        'content' : request.form['content'],
        'date' : request.form['date'],
        'user_id' : session['user_id']
    }
    Entry.create(data)
    return redirect('/create/entry')

#Edit page
@app.route('/edit/<int:entry_id>')
def edit(entry_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : entry_id
    }
    entry = Entry.get_one(data)
    return render_template('edit_entry.html', entry = entry)

#Update
@app.route('/update/entry/<int:entry_id>', methods=['POST'])
def update(entry_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Entry.entry_validator(request.form):
        return redirect('/create/entry')
    Entry.update(request.form, entry_id)
    return redirect('/create/entry')

#View
@app.route('/view/entry/<int:entry_id>')
def view(entry_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : entry_id
    }
    user_data = {
            'id' : session['user_id']
    }
    user = User.get_one(user_data)
    entry = Entry.get_one(data)
    return render_template('view_journal.html', entry = entry, user = user)


#Delete
@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    if 'user_id' not in session:
        return redirect('/')
    Entry.delete(entry_id)
    return redirect('/create/entry')
