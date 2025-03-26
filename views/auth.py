from flask import render_template, request, redirect, session, url_for
from app import app, db
from models import User

message = '' # Error sign in message
messageReg = '' # Success sign up message
messageEA = '' # Existent account message

@app.route('/signin')
def signin():
    return render_template('sign_in.html', message = message, messageEA = messageEA, messageReg = messageReg)

@app.route('/auth', methods=['POST',])
def auth():
    user = User.query.filter_by(email = request.form.get('email')).first()
    if user:
        if request.form.get('passw') == user.passw:
            global message
            global messageEA
            global messageReg

            session['user_signed_in'] = user.email

            message = ''
            messageReg = ''
            messageEA = ''
            return redirect(url_for('index'))
        else:
            message = 'Email or password are incorrect'
            messageReg = ''
            messageEA = ''
            return redirect(url_for('signin'))
    else:
        message = 'Email or password are incorrect'
        messageReg = ''
        messageEA = ''
        return redirect(url_for('signin'))

@app.route('/signup')
def signup():
    return render_template('sign_up.html', message = message, messageEA = messageEA, messageReg = messageReg)

@app.route('/register', methods=['POST',])
def register():
    email = request.form.get('email')
    name = request.form.get('name')
    passw = request.form.get('passw')

    account = User.query.filter_by(email = email).first()
    if account:
        global message
        global messageReg
        global messageEA
        message = ''
        messageReg = ''
        messageEA = 'This email is already registered, sign in'
        return redirect(url_for('signin'))
    
    new_account = User(email = email, name = name, passw = passw)
    db.session.add(new_account)
    db.session.commit()

    message = ''
    messageReg = 'Account created sucsessfully'
    messageEA = ''

    return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session['user_signed_in'] = None
    return redirect(url_for('index'))