"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, User
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
#from datetime import timedelta
#------import datetime para los refresh
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#from flask_jwt_extended import create_refresh_token
#------import refresh------

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../dist/')
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_KEY')

#ACCESS_MIN = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MIN", "60"))
#REFRESH_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "30"))
#----------------------------------------------
#    Pruevas para los refrsh tokens /\  \/
#--------------------------------------------------
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=ACCESS_MIN)
#app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=REFRESH_DAYS)


jwt = JWTManager(app)

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response



@app.route('/login', methods=['POST'])
def login():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': ' Debes enviar informacion en el body'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'El campo email es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': ' El campo password es obligatorio'}), 400
    
    user = User.query.filter_by(email=body['email']).first() 
    
    # var = VarEnModels.query.filer_by(nombredelcampo=body['nombredelcampo']).first() 
    # para  traer el usuario orphan en cascade
    ##########!!!!!   \/
    # user = User.query.filter_by(email=body['email'], password=body['password']).first() 
    #       idea de Leon para ahorrarse el if de password!!! Idea alternativa
    print(user)
    if user is None:
        return jsonify({'msg': 'Usuario o contraseña incorrecta'}), 400
    if user.password != body['password']:
        return jsonify({'msg': 'Usuario o contraseña incorrecta'}), 400 
    
    acces_token = create_access_token(identity=user.email)
    #refresh_token = create_refresh_token(identity=user.email)
    #-----refresh token
    #print(user)
    return jsonify({'msg': 'Usuario logeado correctamente!', \
                    'token': acces_token}), 200
                    #'refresh_token': refresh_token,-------
                    #'access_expires_minutes': ACCESS_MIN,------SOLO PRUEBAS REFRESH
                    #'refresh_expires_days': REFRESH_DAYS}), 200 ------

#-----ENDPOINTS PROTEGIDOS \/ 
@app.route('/private', methods=['GET'])
@jwt_required()
def privado():
    current_user = get_jwt_identity()
    #print(current_user)
    user = User.query.filter_by(email=current_user).first
    #----Para autorizar por primera vez un token en Postman /headers -> //crear key// -> Authorization y //Value -> Bearer (espacio) nuevo token
    #---Una vez autorizado -> /Authorization/Bearer Token/ poner el token
    return jsonify({'msg': 'Gracias por probar que estas logeado'}), 200
    #return jsonify({"id": user.email, "username": user.username }), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
