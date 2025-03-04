from flask import render_template, request, redirect, session, url_for
from app import app, db
from models import User

message = '' # Mensagem de erro de login
messageReg = '' # Mensagem de login com sucesso
messageCE = '' # Mensagem de conta existente

@app.route('/signin')
def signin():
    return render_template('sign_in.html', message = message, messageCE = messageCE, messageReg = messageReg)

@app.route('/auth', methods=['POST',])
def auth():
    user = User.query.filter_by(email = request.form.get('email')).first()
    if user:
        if request.form.get('passw') == user.passw:
            global message
            global messageCE
            global messageReg

            session['user_signed_in'] = user.email

            message = ''
            messageReg = ''
            messageCE = ''
            return redirect(url_for('index'))
        else:
            message = 'Email or password are incorrect'
            messageReg = ''
            messageCE = ''
            return redirect(url_for('signin'))
    else:
        message = 'Email or password are incorrect'
        messageReg = ''
        messageCE = ''
        return redirect(url_for('signin'))

@app.route('/signup')
def signup():
    return render_template('sign_up.html', message = message, messageCE = messageCE, messageReg = messageReg)

@app.route('/register', methods=['POST',])
def register():
    email = request.form.get('email')
    name = request.form.get('name')
    passw = request.form.get('passw')

    conta = User.query.filter_by(email = email).first()
    if conta:
        global message
        global messageReg
        global messageCE
        message = ''
        messageReg = ''
        messageCE = 'This email is already registered, sign in'
        return redirect(url_for('signin'))
    
    nova_conta = User(email = email, name = name, passw = passw)
    db.session.add(nova_conta)
    db.session.commit()

    message = ''
    messageReg = 'Account created sucsessfully'
    messageCE = ''

    return redirect(url_for('signin'))