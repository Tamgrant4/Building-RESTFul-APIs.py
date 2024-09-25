# Q 1
# Task 1
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/fitness_center'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes

# Create tables
with app.app_context():
    db.create_all()

# Task 2
# app.py
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], email=data['email'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member added successfully!"}), 201

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    return jsonify({"name": member.name, "email": member.email})

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully!"})

# Task 3
@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.get_json()
    new_workout = WorkoutSession(member_id=data['member_id'], date=data['date'], duration=data['duration'])
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({"message": "Workout session added!"}), 201

@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    workout = WorkoutSession.query.get(id)
    if not workout:
        return jsonify({"error": "Workout session not found"}), 404
    data = request.get_json()
    workout.date = data['date']
    workout.duration = data['duration']
    db.session.commit()
    return jsonify({"message": "Workout session updated!"})

@app.route('/members/<int:id>/workouts', methods=['GET'])
def get_member_workouts(id):
    workouts = WorkoutSession.query.filter_by(member_id=id).all()
    if not workouts:
        return jsonify({"error": "No workouts found for this member"}), 404
    return jsonify([{"date": workout.date, "duration": workout.duration} for workout in workouts])
