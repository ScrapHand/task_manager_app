from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
CORS(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(300))
    status = db.Column(db.String(50), default="pending")

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([{'id': t.id, 'title': t.title, 'description': t.description, 'status': t.status} for t in Task.query.all()])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(title=data['title'], description=data['description'], status=data.get('status', 'pending'))
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created'}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
