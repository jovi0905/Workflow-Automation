from flask import Blueprint,request,jsonify
from flask_jwt_extended import get_jwt_identity
from middleware.auth_gaurd import role_required
from app import mysql

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/projects',methods=['POST'])
@role_required('admin','superadmin')
def create_project():
    data=request.json
    identity=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO projects(name,descripton,admin_id)VALUEs(%s,%s,%s)",data['name'],data['description'],identity['id'])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Project Created'}),201
@admin_bp.route('/projects',methods=['GET'])
@role_required('admin','superadmin')
def get_projects():
    identity=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM projects WHERE admin_id=%s",(identity['id'],))
    projects=cur.fetchall()
    cur.close()
    return jsonify(projects)

@admin_bp.route('/tasks',methods=['POST'])
@role_required('admin','superadmin')
def assign_task():
    data=request.json
    cur=mysql.connection.cursor()
    cur.execute("""INSERT INTO tasks(title,description,deadline,project_id,assigned_to)VALUES(%s,%s,%s,%s,%s)""",
                (data['title'],data['description'],data['deadline'],data['project_id'],data['assigned_to']))
    cur.execute("INSERT INTO notifications (user_id, message) VALUES (%s,%s)",
                (data['assigned_to'],f"You have been assigned a new task:{data['title']}"))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Task assigned'}),201

@admin_bp.route('/members',methods=['GET'])
@role_required('admin','superadmin')
def get_members():
    cur=mysql.connection.cursor()
    cur.execute("SELECT id, name, email FROM users WHERE role = 'member'")
    members=cur.fetchall()
    cur.close()
    return jsonify(members)
