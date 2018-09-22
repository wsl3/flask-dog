# encoding:utf8
import os


class Config(object):
    # 设置通用配置
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess"
    FLASK_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASK_MAIL_SENDER = "FLASK ADMIN <2350622075@qq.com>"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 服务器和端口号
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = '2350622075@qq.com'
    # 下面这个是授权码, 不是邮箱的密码！！！！
    MAIL_PASSWORD = '授权码'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format('root', '密码', "127.0.0.1", "3306",
                                                                                   "flask_dog")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = dict(developmentConfig=DevelopmentConfig)
