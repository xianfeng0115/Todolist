import click
from Todolist import db,app
from Todolist.models import User,Task

# 设置选项,编写一个自定义命令来自动执行创建数据库表操作
@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop: # 判断是否输入了选项
        db.drop_all()
        db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    name = 'Xianfeng'
    tasks = [
        {'title': '考到二建', 'year': '2020.10', 'isAchieve':'0'},
        {'title': '拿到本科证', 'year': '2021.01', 'isAchieve':'0'},
        {'title': '做一个web界面', 'year': '2020.05', 'isAchieve':'0'},
        {'title': '学会CAPL编程', 'year': '2020.7', 'isAchieve':'0'},
        {'title': '学会Labview', 'year': '2020.8', 'isAchieve':'0'},
        {'title': '年存款5W', 'year': '2021.2', 'isAchieve':'0'},
        {'title': '攒够首付', 'year': '2022.5', 'isAchieve':'0'},
        {'title': '使用编程接一单生意', 'year': '2020.12', 'isAchieve':'0'},
        {'title': '去广州看一场球赛', 'year': '2021.5', 'isAchieve':'1'},
        {'title': '录播一期属于自己的课程', 'year': '2021.3', 'isAchieve':'1'},
    ]
    user = User(name=name)
    db.session.add(user)
    for t in tasks:
        task = Task(title=t['title'], year=t['year'],isAchieve=t['isAchieve'])
        db.session.add(task)
    db.session.commit()
    click.echo('Done.')