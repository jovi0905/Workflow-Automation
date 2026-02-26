from flask import Blueprint,request,jsonify
from middleware.auth_gaurd import role_required
from app import mysql

superadmin_bp=Blueprint('superadmin',__name__)

@superadmin_bp.route('/users',methods=['GET'])
@role_required('superadmin')
def get_all_users():
    cur=mysql.connection.cursor()
    cur.execute("SELECT id, name, email, role, created_at FROM users")
    users=cur.fetchall()
    return jsonify(users)

@superadmin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@role_required('superadmin')
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User deleted'})

@superadmin_bp.route('/users/<int:user_id>', methods=['PUT'])
@role_required('superadmin')
def change_role(user_id):
    data=request.json
    cur=mysql.connection.cursor()
    cur.execute("UPDATE users SET role=%s WHERE id=%s",(data['role'],user_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Role Updated'})