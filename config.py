import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '87086715981b3b5506de9d7d757953ab002c22e57e76744c' #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    LOG_LEVEL = logging.DEBUG
    SERVER_URL = 'https://ziabrov.pythonanywhere.com/'
    BOT_TOKEN = '5976923303:AAFjzYS3l3DXCfPORmYw5rIh58DbC9C7VXM'
    MANYCHAT_TOKEN = '539030:10f2de6d5f7b21d7587d0e44fcfae370'