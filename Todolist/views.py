from flask import render_template,request,url_for,flash,redirect

from Todolist import app, db
from Todolist.models import User, Task

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
