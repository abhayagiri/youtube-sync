import os


project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'secret'
CSRF_ENABLED = True
CSRF_SESSION_KEY = 'secret'

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(project_path, 'data', 'db.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

TEMPLATES_AUTO_RELOAD = True
