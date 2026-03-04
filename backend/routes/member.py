from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from middleware.auth_guard import role_required
from app import get_db

member_bp = Blueprint('member', __name__)

@member_bp.route('/tasks', methods=['GET'])
@role_required('member', 'admin', 'superadmin')
def get_my_tasks():
    try:
        identity = get_jwt_identity()
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM tasks WHERE assigned_to=%s", (identity['id'],))
        tasks = cur.fetchall()
        cur.close()
        db.close()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@member_bp.route('/tasks/<int:task_id>/status', methods=['PUT'])
@role_required('member', 'admin', 'superadmin')
def update_status(task_id):
    try:
        data = request.json
        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (data['status'], task_id))
        db.commit()
        cur.close()
        db.close()
        return jsonify({'message': 'Status Updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@member_bp.route('/notifications', methods=['GET'])
@role_required('member', 'admin', 'superadmin')
def get_notifications():
    try:
        identity = get_jwt_identity()
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC",
                    (identity['id'],))
        notifs = cur.fetchall()
        cur.close()
        db.close()
        return jsonify(notifs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500