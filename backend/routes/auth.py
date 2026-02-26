from flask import Blueprint,request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from app import mysql

auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/register',methods=['POST'])
def register():
    data=request.json
    name=data['name']
    email=data['email']
    password=bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
    role=data.get('role','member')

    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO users(name,email,password,role) VALUES (%s,%s,%s,%s)",(name,email,password,role))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User Registers'}),201

@auth_bp.route('/login',methods=['POST'])
def login():
    data=request.json
    email=data['email']
    password=data['password'].encode('utf-8')

    cur=mysql.connection.cursor()
    cur.execute("SELECT* FROM users WHERE email=%s",(email,))
    user=cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password,user[3].encode('uts-8')):
        token=create_access_token(identity={'id':user[0],'role':user[4]})
        return jsonify({'token':token,'role':user[4],'name':user[1]})
    return jsonify({'message':'Invalid credentials'}),401

