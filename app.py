from flask import Flask,render_template,request,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
import os,sys
import click
app=Flask(__name__)

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html'), 404 # 返回模板和状态码

# 完成页面
@app.route('/task/achieve/', methods=['GET', 'POST']) #限定只接受 POST 请求
def achieve():
    user = User.query.first()
    altasks = Task.query.filter(Task.isAchieve == '1').all()
    return render_template('achieve.html', user=user, tasks=altasks)

# 新增条目
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title') # 传入表单对应输入字段的name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 10 or len(title)> 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页
        # 保存表单数据到数据库
        task = Task(title=title, year=year,isAchieve='0') # 创建记录
        db.session.add(task) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('index')) # 重定向回主页
    user = User.query.first()
    untasks = Task.query.filter(Task.isAchieve == '0').all()
    return render_template('index.html', user=user, tasks=untasks)

@app.route('/test', methods=['GET', 'POST'])
def test():
    user = User.query.first()
    untasks = Task.query.filter(Task.isAchieve == '0').all()
    a=1
    b=2
    c=a+b
    return render_template('index.html', result=c,user=user, tasks=untasks)

# 编辑条目
@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 10 or len(title)> 60:
            flash('Invalid input.')
            return redirect(url_for('edit', task_id=task_id))
            # 重定向回对应的编辑页面
        task.title = title # 更新标题
        task.year = year # 更新年份
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index')) # 重定向回主页
    return render_template('edit.html', task=task) # 传入被编辑的任务记录

# 删除条目
@app.route('/task/delete/<int:task_id>', methods=['POST']) #限定只接受 POST 请求
def delete(task_id):
    task = Task.query.get_or_404(task_id) # 获取任务记录
    db.session.delete(task) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index')) # 重定向回主页

# 完成条目
@app.route('/task/achieve/<int:task_id>', methods=['POST']) #限定只接受 POST 请求
def complete(task_id):
    task = Task.query.get_or_404(task_id) # 获取任务记录
    task.isAchieve = '1'
    db.session.commit() # 提交数据库会话
    flash('Congratulation, Task Complete.')
    return redirect(url_for('achieve')) # 重定向回完成页

# 重新做条目
@app.route('/task/redo/<int:task_id>', methods=['POST']) #限定只接受 POST 请求
def redo(task_id):
    task = Task.query.get_or_404(task_id) # 获取任务记录
    task.isAchieve = '0'
    db.session.commit() # 提交数据库会话
    flash('OK，Re-do Task.')
    return redirect(url_for('index')) # 重定向回主页

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

# 用户名设置
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')


# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev' 
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
class Task(db.Model): # 表名将会是 Task
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 标题
    year = db.Column(db.String(10)) # 年份
    isAchieve = db.Column(db.String(4)) # 默认任务初始未完成
