# encoding:utf8
# 构建启动脚本

from app import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.model import User, Role
from app import db

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
