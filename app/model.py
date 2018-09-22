# encoding: utf8

from app import db
from flask import current_app
from . import login_manager
from flask_login import UserMixin
# 向数据库中添加密码时加密,登录时进行核查
from werkzeug.security import generate_password_hash, check_password_hash
# 生成加密令牌,向用户注册用户发送安全的确认邮件
from itsdangerous import TimedJSONWebSignatureSerializer as serializer


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref=db.backref('roles'))

    def __repr__(self):
        return "<Role:%s>" % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # confirmed字段对user账户进确认
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 在视图函数中创建User对象时直接对password赋值
    @property
    def password(self):
        raise AttributeError("密码不可读取！")

    @password.setter
    def password(self, password):
        # 注册时把输入的password加密后赋值给password_hash属性
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # 登录时对密码进行检查
        return check_password_hash(self.password_hash, password)

    # 生成加密令牌
    def generate_confirmtion_token(self, time=3600):
        s = serializer(current_app.config['SECRET_KEY'], expires_in=time)
        token = s.dumps({'confirm': self.id})
        return token

    def confirm(self, token):
        s = serializer(current_app.config['SECRET_KEY'])
        # 通过loads()获得原始数据时,如果时间过期或者token被人篡改会抛出异常
        try:
            data = s.loads(token)
        except:
            return False
        # 最后对id进行验证
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        print("111111111111111111")
        db.session.add(self)
        db.session.commit()
        return True




    # def __repr__(self):
    #     return "<User:%s>" % self.username


# flask-login必须实现的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
