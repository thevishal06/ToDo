from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from firebase_admin import credentials, initialize_app
from datetime import datetime
# from app import db

# # Use app.app_context() to create the database within the application context
# with app.app_context():
#     db.create_all()


app = Flask(__name__)

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate('path/to/your/firebase/credentials.json')
# firebase_app = initialize_app(cred)

# Configure SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Todo {self.id}>'
    


# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['Get', "POST"])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc= desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'Fuck Off'
@app.route('/update')
def update():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'Fuck Off'
@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    desc = request.form['desc']
    new_todo = Todo(title=title, desc=desc)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
