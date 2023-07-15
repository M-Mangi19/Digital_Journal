from flask_app import app
from flask import Flask, request, render_template, redirect, session, flash
from flask_app.models.models_user import User
from flask_app.models.models_entry import Entry
from flask_app.models.models_favorite import Favorite
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#Login-route
@app.route('/')
def login():
    return render_template('login.html')

#New User
@app.route('/new_user')
def new_user():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user = User.get_one(data)
        return render_template('dashboard.html', user = user)


#Register
@app.route('/register/user', methods=["POST"])
def register_user():
    if not User.register_validator(request.form):
        return redirect('/')
    else:
        data = {
            "first_name" : request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"],
            "password" : bcrypt.generate_password_hash(request.form["password"])
        }
        id = User.create(data)
        if not id:
            flash("Something went wrong here!")
            return redirect('/')
        else:
            session['user_id'] = id
            return redirect('/dashboard')

#Login
@app.route('/login/user', methods=["POST"])
def login_user():
    if not User.login_validator(request.form):
        return redirect('/')
    data = {
        'email': request.form['email']
    }
    user = User.get_email(data)
    if not user:
        flash("This email is not in our database. Please Register!")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("This password is incorrect!")
        return redirect('/')
    else:
        session['user_id'] = user.id
        return redirect ('/dashboard')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Till next time...')
    return redirect('/')