from flask import render_template, request, redirect, session, url_for
from app import app, db

@app.route('/doc')
def doc():
    return render_template('doc.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')