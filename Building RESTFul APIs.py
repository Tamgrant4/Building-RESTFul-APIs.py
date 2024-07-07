# Q 1
# Task 1
mkdir fitness_center
cd fitness_center
python -m venv venv
venv\Scripts\activate
pip install Flask Flask-Marshmallow flask-mysqldb

# config.py
MYSQL_HOST = 'localhost'
MYSQL_USER = 'your_username'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'fitness_center'
# app.py
from flask import Flask
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)
ma = Marshmallow(app)

if __name__ == "__main__":
    app.run(debug=True)
CREATE TABLE Members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE WorkoutSessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    date DATE,
    duration INT,
    FOREIGN KEY (member_id) REFERENCES Members(id)
);

# Task 2
# app.py
from flask import request, jsonify

@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Member added successfully'}), 201

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
    member = cursor.fetchone()
    cursor.close()

    if member:
        return jsonify({'id': member[0], 'name': member[1], 'email': member[2], 'phone': member[3]})
    else:
        return jsonify({'message': 'Member not found'}), 404

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Members SET name = %s, email = %s, phone = %s WHERE id = %s", (name, email, phone, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Member updated successfully'})

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Members WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Member deleted successfully'})

# Task 3
@app.route('/workout_sessions', methods=['POST'])
def add_workout_session():
    member_id = request.json['member_id']
    date = request.json['date']
    duration = request.json['duration']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO WorkoutSessions (member_id, date, duration) VALUES (%s, %s, %s)", (member_id, date, duration))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Workout session added successfully'}), 201

@app.route('/workout_sessions/<int:id>', methods=['GET'])
def get_workout_session(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM WorkoutSessions WHERE id = %s", (id,))
    session = cursor.fetchone()
    cursor.close()

    if session:
        return jsonify({'id': session[0], 'member_id': session[1], 'date': session[2], 'duration': session[3]})
    else:
        return jsonify({'message': 'Workout session not found'}), 404

@app.route('/workout_sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    member_id = request.json['member_id']
    date = request.json['date']
    duration = request.json['duration']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE WorkoutSessions SET member_id = %s, date = %s, duration = %s WHERE id = %s", (member_id, date, duration, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Workout session updated successfully'})

@app.route('/workout_sessions/<int:id>', methods=['DELETE'])
def delete_workout_session(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM WorkoutSessions WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Workout session deleted successfully'})
@app.route('/members/<int:member_id>/workout_sessions', methods=['GET'])
def get_member_workout_sessions(member_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (member_id,))
    sessions = cursor.fetchall()
    cursor.close()

    workout_sessions = []
    for session in sessions:
        workout_sessions.append({'id': session[0], 'member_id': session[1], 'date': session[2], 'duration': session[3]})

    return jsonify(workout_sessions)
@app.route('/members/<int:member_id>/workout_sessions', methods=['GET'])
def get_member_workout_sessions(member_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (member_id,))
    sessions = cursor.fetchall()
    cursor.close()

    workout_sessions = []
    for session in sessions:
        workout_sessions.append({'id': session[0], 'member_id': session[1], 'date': session[2], 'duration': session[3]})

    return jsonify(workout_sessions)
