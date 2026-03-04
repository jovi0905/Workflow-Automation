from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from app import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        role = data.get('role', 'member')

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
                    (name, email, password.decode('utf-8'), role))
        db.commit()
        cur.close()
        db.close()
        return jsonify({'message': 'User registered'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data['email']
        password = data['password'].encode('utf-8')

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        db.close()

        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            token = create_access_token(
                identity={'id': user['id'], 'role': user['role']})
            return jsonify({'token': token, 'role': user['role'], 'name': user['name']})
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 