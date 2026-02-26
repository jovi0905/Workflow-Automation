from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

app=Flask(__name__)
app.config.from_object(config)
CORS(app,origins="*")

mysql=MySQL(app)
jwt=JWTManager(app)

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.superadmin import superadmin_bp
from routes.member import member_bp

app.register_blueprint(auth_bp,url_prefix='/api/auth')
app.register_blueprint(admin_bp,url_prefix='/api/admin')
app.register_blueprint(superadmin_bp,url_prefix='/api/superadmin')
app.register_blueprint(member_bp,url_prefix='/api/member')



@app.route('/')
def index():
    return {"message":"API is running"},200
if __name__=='__main__':
    app.run(debug=True)
