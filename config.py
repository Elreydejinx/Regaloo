import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rootuser:Gitkoding2024$@localhost/regaloo_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')