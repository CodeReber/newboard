from flask import Flask, jsonify, request, redirect, url_for, render_template
from sqlalchemy import create_engine, func
from flask_sqlalchemy import SQLAlchemy
import datetime

database_path = "my.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.TEXT(255))
    Position = db.Column(db.Integer, unique=True)
    task = db.relationship("Task",backref="person")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.TEXT(255))
    Personid = db.Column(db.ForeignKey("person.id"))
    



@app.route('/')
def index():
    people = Person.query.all()
    return render_template('index.html', people=people)

@app.route('/task',methods=["POST"])
def addtask():
    req = request.get_json()
    name = req.get("name")
    personid = req.get("personid")
    if not personid:
        personid = Person.query.order_by(Person.Position.asc()).first().id
    task = Task(Name=name, Personid=personid)
    db.session.add(task)
    db.session.commit()
    return {"id":task.id,"name":name,"personid":personid}

@app.route('/task')
def gettask():
    tasks = Task.query.all()
    tasklist = []
    for t in tasks:
        tasklist.append({"id":t.id,"name":t.Name,"personid":t.Personid,"personname":t.person.Name})
    return {"tasks":tasklist}


if __name__ == "__main__":
    app.run(debug=True)