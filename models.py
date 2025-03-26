from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_mixin
from enum import Enum
# Enum for the user type
class UserType(Enum):
    ADMIN = 1
    SECO_MANAGER = 2
    USER = 3

# Enum for the performed task status
class PerformedTaskStatus(Enum):
    SOLVED = 1
    UNSOLVED = 2

# Function to get the db and app
def get_db_and_app():
    from app import db, app
    return db, app

# Getting db and app
db, app = get_db_and_app()

# Association Tables
guideline_conditioning_factor = db.Table('guideline_conditioning_factor',
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.guidelineID')),
    db.Column('conditioning_factor_transp_id', db.Integer, db.ForeignKey('conditioning_factor_transp.conditioning_factor_transp_id'))
)

guideline_dx_factor = db.Table('guideline_dx_factor',
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.guidelineID')),
    db.Column('dx_factor_id', db.Integer, db.ForeignKey('dx_factor.dx_factor_id'))
)

guideline_seco_process = db.Table('guideline_seco_process',
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.guidelineID')),
    db.Column('seco_process_id', db.Integer, db.ForeignKey('seco_process.seco_process_id'))
)

guideline_seco_dimension = db.Table('guideline_seco_dimension',
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.guidelineID')),
    db.Column('seco_dimension_id', db.Integer, db.ForeignKey('seco_dimension.seco_dimension_id'))
)

guideline_task = db.Table('guideline_task',
    db.Column('guideline_id', db.Integer, db.ForeignKey('guideline.guidelineID')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.task_id'))
)

task_question = db.Table('task_question',
    db.Column('task_id', db.Integer, db.ForeignKey('task.task_id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.question_id'))
)

# Main Tables
class User(db.Model):
    __tablename__ = 'user'
    
    # Main Rows
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    passw = db.Column(db.String(100), nullable=False)

    # Discriminator to identify the user type
    type = db.Column(db.Enum(UserType), nullable=False)

    # Polymorphic identity for User
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

class Admin(User):
    # Polymorphic identity for Admin
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class SECO_MANAGER(User):
    # Polymorphic identity for SECO_MANAGER
    __mapper_args__ = {
        'polymorphic_identity': 'seco_manager'
    }
    
    # Relationship with CollectionData
    collection_data = db.relationship('CollectionData',
                                        backref=db.backref('seco_manager', lazy=True))

class Evaluation(db.Model):
    __tablename__ = 'evaluation'

    # Main Rows
    evaluation_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Foreign key to the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # Relationship with CollectionData
    collection_data = db.relationship('CollectionData',
                                        backref=db.backref('evaluation', lazy=True))
    

class CollectionData(db.Model):
    __tablename__ = 'collection_data'
    
    # Main Rows
    collectionID = db.Column(db.Integer, primary_key=True)
    seco_portal = db.Column(db.String(500), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    # Relationship with PerformedTask
    performed_tasks = db.relationship('PerformedTask',
                                        backref=db.backref('collection_data', lazy=True))
    
    # Relationship with ProfileQuestionnaire
    profile_questionnaire = db.relationship('ProfileQuestionnaire',
                                            backref=db.backref('collection_data', lazy=True, uselist=False),
                                            uselist=False)
    
    # Relationship with FinalQuestionnaire
    final_questionnaire = db.relationship('FinalQuestionnaire',
                                            backref=db.backref('collection_data', lazy=True, uselist=False),
                                            uselist=False)

    # Foreign key to the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # Foreign key to the evaluation table
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluation.evaluation_id'), nullable=False)

class ProfileQuestionnaire(db.Model):
    __tablename__ = 'profile_questionnaire'

    # Main Rows
    profile_questionnaire_id = db.Column(db.Integer, primary_key=True)
    academic_level = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    seco = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    # Foreign key to the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # Foreign key to the collection data table
    collection_data_id = db.Column(db.Integer, db.ForeignKey('collection_data.collectionID'), nullable=False, unique=True)

class FinalQuestionnaire(db.Model):
    __tablename__ = 'final_questionnaire'

    # Main Rows
    final_questionnaire_id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(1000), nullable=False)
    emotion = db.Column(db.Integer, nullable=False)

    # Foreign key to the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    # Foreign key to the collection data table
    collection_data_id = db.Column(db.Integer, db.ForeignKey('collection_data.collectionID'), nullable=False, unique=True)

class PerformedTask(db.Model):
    __tablename__ = 'performed_task'
    
    # Main Rows
    performed_task_id = db.Column(db.Integer, primary_key=True)
    initial_timestamp = db.Column(db.DateTime, nullable=False)
    final_timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(PerformedTaskStatus), nullable=False)

    # Relationship with Answer
    answers = db.relationship('Answer',
                                backref=db.backref('performed_task', lazy=True))

    # Foreign key to the collection data table
    collection_data_id = db.Column(db.Integer, db.ForeignKey('collection_data.collectionID'), nullable=False)

    # Foreign key to the task table
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), nullable=False)

class Answer(db.Model):
    __tablename__ = 'answer'
    
    # Main Rows
    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000), nullable=False)

    # Foreign key to the performed task table
    performed_task_id = db.Column(db.Integer, db.ForeignKey('performed_task.performed_task_id'), nullable=False)

    # Foreign key to the question table
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)

class Task(db.Model):
    __tablename__ = 'task'
    
    # Main Rows
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    # Relationship with PerformedTask
    performed_tasks = db.relationship('PerformedTask',
                                        backref=db.backref('task', lazy=True))

    # Relationship with Question
    questions = db.relationship('Question',
                                secondary=task_question,
                                backref=db.backref('tasks', lazy=True))

    # Relationship with Guideline
    guidelines = db.relationship('Guideline',
                                secondary=guideline_task,
                                back_populates='related_tasks')

class Question(db.Model):
    __tablename__ = 'question'
    
    # Main Rows
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000), nullable=False)

    # Relationship with Answer
    answers = db.relationship('Answer',
                                backref=db.backref('question', lazy=True))

class Guideline(db.Model):
    __tablename__ = 'guideline'
    
    # Main Rows
    guidelineID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    # Relationship with Key_success_criterion
    key_success_criteria = db.relationship('Key_success_criterion', 
                                            backref=db.backref('guideline', lazy=True))
    
    # Relationship with Conditioning_factor_transp
    conditioning_factors = db.relationship('Conditioning_factor_transp',
                                            secondary=guideline_conditioning_factor,
                                            backref=db.backref('guidelines', lazy=True))
    
    # Relationship with DX_factor
    dx_factors = db.relationship('DX_factor',
                                secondary=guideline_dx_factor,
                                backref=db.backref('guidelines', lazy=True))
    
    # Relationship with SECO_process
    seco_processes = db.relationship('SECO_process',
                                    secondary=guideline_seco_process,
                                    backref=db.backref('guidelines', lazy=True))
    
    # Relationship with SECO_dimension
    seco_dimensions = db.relationship('SECO_dimension',
                                        secondary=guideline_seco_dimension,
                                        backref=db.backref('guidelines', lazy=True))
    
    # Relationship with Task
    related_tasks = db.relationship('Task',
                            secondary=guideline_task,
                            back_populates='guidelines')

class SECO_dimension(db.Model):
    __tablename__ = 'seco_dimension'

    # Main Rows
    seco_dimension_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Key_success_criterion(db.Model):
    __tablename__ = 'key_success_criterion'

    # Main Rows
    key_success_criterion_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    # Relationship with Example
    examples = db.relationship('Example',
                                backref=db.backref('key_success_criteria', lazy=True))

    # Foreign key to the guideline table
    guideline_id = db.Column(db.Integer, db.ForeignKey('guideline.guidelineID'), nullable=False)



class Conditioning_factor_transp(db.Model):
    __tablename__ = 'conditioning_factor_transp'

    # Main Rows
    conditioning_factor_transp_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)

class DX_factor(db.Model):
    __tablename__ = 'dx_factor'

    # Main Rows
    dx_factor_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)

class SECO_process(db.Model):
    __tablename__ = 'seco_process'

    # Main Rows
    seco_process_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)

class Example(db.Model):
    __tablename__ = 'example'

    # Main Rows
    example_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)

    # Foreign key to the key_success_criterion table
    key_success_criterion_id = db.Column(db.Integer, db.ForeignKey('key_success_criterion.key_success_criterion_id'), nullable=False)

# Initialize the database only when the module is imported directly
def init_db():
    with app.app_context():
        db.create_all()

# Calling the initialization
init_db()