# encoding:utf8

from . import auth
from flask import render_template, redirect, url_for, request, flash
from app.auth.forms import LoginForm, RegisterForm
from ..model import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from ..email import send_mail


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # 用户访问未授权url时会先让用户登录,再跳转到之前用户想要访问的页面
            # 用户点击邮件中的链接时 必须先登录,登录后必须再次跳转到confirm界面进行认证
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("email or password wrong!")

    return render_template('auth/login.html', form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 注册成功,把用户添加到数据库中
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # 发送邮件确认账户
        token = user.generate_confirmtion_token()
        send_mail(user.email, "Confirm your Account!", "auth/email/confirm",
                  user=user, token=token)
        flash("我们已经给你发送了一封邮件！")
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


# 用户点击邮件中的链接进行认证
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    print("confirm-------------------")
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        flash("认证成功！")
    else:
        flash("认证失败！")
    return redirect(url_for("main.index"))


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for("main.index"))


# 用请求钩子过滤未确认的账户
# 该账户必须已经 登录但没有confirm,可以自由访问login,register,confirm页面
# 使用before_app_request对全局request有效
@auth.before_app_request
def before_request():
    # 用户登录但没有认证,同时访问非(auth蓝本界面和static)时会跳转到unconfirmed界面
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint != 'static' and request.endpoint[:5] != "auth.":
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed/')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# 必须有login_required装饰器保护,要知道当前用户
@auth.route('/reconfirmed/')
@login_required
def resend_email():
    token = current_user.generate_confirmtion_token()
    send_mail(current_user.email, "重新确认账户！", "auth/email/confirm", token=token, user=current_user)
    flash("我们已经重新给你发送了邮件！")
    return redirect(url_for('main.index'))
