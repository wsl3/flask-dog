# encoding:utf8

from ..model import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("keep me logged in")
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(1, 64), Regexp('^[a-zA-Z][0-9a-zA-Z._]*$', 0,
                                                                         "用户名只包含字母,数字,.和_,并且以字母开头！")])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message="password must match")])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # 自定义验证函数
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已经注册！")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("该用户名正在使用！")

