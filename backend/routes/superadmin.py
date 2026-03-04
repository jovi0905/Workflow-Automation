from flask import Blueprint,request,jsonify
from middleware.auth_guard import role_required
from app import get_db

superadmin_bp=Blueprint('superadmin',__name__)

@superadmin_bp.route('/users',methods=['GET'])
@role_required('superadmin')
def get_all_users():
    cur=db.cursor
    cur.execute("SELECT id, name, email, role, created_at FROM users")
    users=cur.fetchall()
    return jsonify(users)

@superadmin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@role_required('superadmin')
def delete_user(user_id):
    db=get_db()
    cur=db.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    db.close()
    cur.close()
    return jsonify({'message': 'User deleted'})

@superadmin_bp.route('/users/<int:user_id>', methods=['PUT'])
@role_required('superadmin')
def change_role(user_id):
    data=request.json
    db=get_db()
    cur=db.cursor()
    cur.execute("UPDATE users SET role=%s WHERE id=%s",(data['role'],user_id))
    db.commit()
    db.close()
    cur.close()
    return jsonify({'message':'Role Updated'})