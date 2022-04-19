import os

basedir = os.path.abspath(os.path.dirname(__file__))

# GIve access to the project in any OS we find ourself in
# Allow outside files/folders to be added to the project from
# base directory

class Config():
    """
    Set Config variables for the flask app.
    Using Enviornment variables where available otherwise
    create a config variable if not done already.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or "You will never guess nanananabooboo"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False