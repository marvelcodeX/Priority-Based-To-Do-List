from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import case

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    priority = db.Column(db.Enum('High', 'Medium', 'Low'))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/')
def index():
    tasks = Task.query.order_by(
        case(
            (Task.priority == 'High', 1),
            (Task.priority == 'Medium', 2),
            else_=3
        ),
        Task.due_date
    ).all()

    # Calculate the number of completed tasks and total tasks
    completed_count = Task.query.filter_by(completed=True).count()
    total_count = Task.query.count()

    # Calculate the reward message (for example, after completing 5 tasks)
    if completed_count >= 1:
        reward_message = "🎉 Congratulations! You've completed your tasks! Keep it up! 🎉"
    else:
        reward_message = None

    return render_template('index.html', tasks=tasks, completed_count=completed_count, total_count=total_count, reward_message=reward_message)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        new_task = Task(
            title=request.form['title'],
            description=request.form['description'],
            due_date=request.form['due_date'],
            priority=request.form['priority']
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/complete_task/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed  # Toggle the completed state
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
