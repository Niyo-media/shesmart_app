from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ---------------- Models ----------------

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_date = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    cycle_length = db.Column(db.String(50), nullable=False)

# Create all tables
with app.app_context():
    db.create_all()

# ---------------- Routes ----------------

@app.route('/')
def index():
    return jsonify({"message": "Flask API with SQLite is running!"})

# Register a new user
@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        new_user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Register a new task
@app.route('/register_task', methods=['POST'])
def register_task():
    data = request.get_json()
    try:
        new_task = Task(
            user_id=data['user_id'],
            start_date=data['start_date'],
            duration=data['duration'],
            cycle_length=data['cycle_length']
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task registered successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "user_id": u.user_id,
        "name": u.name,
        "email": u.email,
        "phone": u.phone
    } for u in users])

# User login
@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# ---------------- Error Handlers ----------------

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

# ---------------- Run App ----------------

if __name__ == '__main__':
    app.run(debug=False)

