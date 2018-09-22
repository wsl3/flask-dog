# encoding: utf8

# 在main_Blue文件的__init__ 中构建蓝本

from flask import Blueprint

main = Blueprint('main', __name__)

from . import errors, views
