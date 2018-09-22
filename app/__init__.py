# encoding: utf8
# 创建app函数工厂

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
# 可以设置为 none, basic, strong来提供不同程度的回话保护强度
login_manager.session_protection = "strong"
# 设置登录页面的端点
login_manager.login_view = "auth.login"


def create_app(config_name="developmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 下面这个有什么用？ 这个函数里没有任何代码
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # 注册蓝本main
    from .main import main
    app.register_blueprint(main)

    # 注册蓝本auth
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app


# if __name__ == '__main__':
#     app = create_app()
