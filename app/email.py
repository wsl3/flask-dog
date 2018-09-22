# encoding:utf8

from flask_mail import Message
from app import mail
from flask import render_template
from config import DevelopmentConfig


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject=subject, recipients=[to], sender=DevelopmentConfig.MAIL_USERNAME)
    # 不太清楚msg.body的作用,没有他的话也可以发送并验证邮件
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)


# 邮件问题参考链接
# https://blog.csdn.net/wbin233/article/details/73222027#%E5%BC%80%E5%90%AFqq%E9%82%AE%E7%AE%B1smtp%E6%9C%8D%E5%8A%A1
# 邮箱必须开启 IMAP/SMTP 服务,MAIL-PASSWORD是授权码