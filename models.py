from app import db, app

class User(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    passw = db.Column(db.String(100), nullable=False)

# class Guideline(db.Model):
#     guidelineID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     hip = db.Column(db.String(50), nullable=False)
#     sed = db.Column(db.String(50), nullable=False)
#     cft = db.Column(db.String(50), nullable=False)
#     devExFac = db.Column(db.String(50), nullable=False)
#     ksc = db.Column(db.String(5000), nullable=False)
#     example = db.Column(db.String(5000), nullable=False)




with app.app_context():
    db.create_all()