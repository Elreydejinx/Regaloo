import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rootuser:Gitkoding@AX15:3306/regaloo'
    SQLALCHMEY_TRACT_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USS_SSL = False
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')