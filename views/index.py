from flask import render_template, request, redirect, session, url_for
from app import app, db
from models import User

@app.route('/')
def index():
    email = session['user_signed_in']
    user = User.query.filter_by(email = email).first()
    return render_template('index.html', email = email, name = user.name)