from flask import Flask
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
import os,sys
import click
app=Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev' 
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

@app.context_processor
def inject_user():
    from Todolist.models import User
    user = User.query.first()
    return dict(user=user)

from Todolist import views, errors, commands