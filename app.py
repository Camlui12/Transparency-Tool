from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('database.py')

db = SQLAlchemy(app)

# Importing views
from views.index import *
from views.pages import *
from views.auth import *
from views.admin import *
from external.tasks import *

if __name__ == "__main__":
    app.run(debug=True)