SECRET_KEY = 'LabESC'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{passw}@{server}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'root',
        passw = 'admin',
        server = 'localhost',
        database = 'tool_portal'
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False