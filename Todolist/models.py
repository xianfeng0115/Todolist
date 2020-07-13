from Todolist import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
class Task(db.Model): # 表名将会是 Task
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 标题
    year = db.Column(db.String(10)) # 年份
    isAchieve = db.Column(db.String(4)) # 默认任务初始未完成
