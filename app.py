from email.policy import default
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:home@localhost:5432/todoapp'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable= False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable = True)

    def __repr__(self):
        return f'<Task {self.id} {self.description} >'


class TodoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    task = db.relationship('Task', backref='list', lazy = True)

db.create_all()
@app.route('/')
def index():

    print('asdfg')
    
    tasks = Task.query.order_by('id').all()
    return render_template('index.html', data=tasks)


@app.route("/todos/create", methods=['POST'])
def create():
    # description = request.form.get('description','')
    # redirect(url_for('index'))
    print('lets know if anything comes here')

    description = request.get_json()['description']

    print(description)
    task = Task(description=description)

    db.session.add(task)
    db.session.commit()
    return jsonify({'description': task.description, 'completed': task.completed})


@app.route('/todo/<todo_id>/check-completed', methods=['POST'])
def set_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        task = Task.query.get(todo_id)
        task.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

        


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000)
