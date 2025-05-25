from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy.sql import case
from datetime import datetime, timedelta, date

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=True)
    completed = db.Column(db.Integer, nullable=True, default=0)
    created_at = db.Column(db.DateTime, nullable=True, server_default=db.func.now())

@app.route('/')
def index():
    # Calculate tomorrow's date and current date
    tomorrow = (datetime.now().date() + timedelta(days=1))
    current_date = datetime.now().date()

    # Fetch all tasks, ordered by priority and due date
    tasks = Task.query.order_by(
        case(
            (Task.priority == 'High', 1),
            (Task.priority == 'Medium', 2),
            else_=3
        ),
        Task.due_date
    ).all()

    # Fetch tasks due tomorrow
    tasks_due_tomorrow = Task.query.filter(
        Task.due_date == tomorrow,
        Task.completed == 0
    ).all()

    # Calculate the number of completed tasks and total tasks
    completed_count = Task.query.filter_by(completed=1).count()
    total_count = Task.query.count()

    # Calculate the reward message
    if completed_count >= 1:
        reward_message = "🎉 Congratulations! You're completing your tasks! Keep it up! 🎉"
    else:
        reward_message = None

    return render_template(
        'index.html',
        tasks=tasks,
        completed_count=completed_count,
        total_count=total_count,
        reward_message=reward_message,
        tasks_due_tomorrow=tasks_due_tomorrow,
        current_date=current_date
    )

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']

        # Validate priority
        if priority not in ['High', 'Medium', 'Low']:
            return render_template('add_task.html', error="Invalid priority value")

        new_task = Task(
            title=title if title else None,
            description=description if description else None,
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None,
            priority=priority if priority else None
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/complete_task/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = 1 if task.completed == 0 else 0  # Toggle between 0 and 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)