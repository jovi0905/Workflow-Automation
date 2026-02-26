from flask import Blueprint,jsonify,request
from flask_jwt_extended import get_jwt_identity
from middleware.auth_gaurd import role_required
from app import mysql

member_bp=Blueprint('member',__name__)

@member_bp.route('/tasks', methods=['GET'])
@role_required('member', 'admin', 'superadmin')
def get_my_tasks():
    identity=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE assigned_to=%s",(identity['id'],))
    tasks=cur.fetchall()
    cur.close()
    return jsonify(tasks)

@member_bp.route('/tasks/<int:task_id>/status',methods=['PUT'])
@role_required('member','admin','superadmin')
def update_status(task_id):
    data=request.json
    cur= mysql.connection.cursor()
    cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (data['status'], task_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Status Updated'})

@member_bp.route('/notifications',methods=['GET'])
@role_required('member','admin','superadmin')
def get_notifications():
    identity=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC",
                (identity['id'],))
    notifs = cur.fetchall() 
    cur.close()
    return jsonify(notifs)