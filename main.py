import datetime
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, redirect, render_template, request, url_for
import pymysql
from flask_wtf.csrf import CSRFProtect
from features.acervotitulo.models import AcervotituloForm
from features.core.auth.model import LoginForm, User
# librerias para el registro de los 50000
# import pandas as pd
from sqlalchemy import create_engine
from flask_jwt_extended import current_user

from features.prestamo.ucases_or_services import PrestamoCU

pymysql.install_as_MySQLdb()

from flask_jwt_extended import get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request
from flask_jwt_extended import JWTManager

app = Flask(__name__)

basedir = os.path.abspath( os.path.dirname(__file__) )
load_dotenv( os.path.join(basedir, ".env") )
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

# Here you can globally configure all the ways you want to allow JWTs to
# be sent to your web application. By default, this will be only headers.
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=2)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./temp.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
# db = SQLAlchemy()
csrf = CSRFProtect(app)

from flask_login import LoginManager, logout_user
login_manager = LoginManager()
login_manager.login_view = 'AuthRoute.get_login'
login_manager.init_app(app)

from features.core.bd import db
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = None
    try:
        user = User.query.filter_by(public_id=user_id).one_or_none()
    except (BaseException) as err:
        print (err)
    return user

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    # return User.query.filter_by(id=identity).one_or_none()
    user = None
    try:
        user = User.query.filter_by(id=identity).one_or_none()
    except (BaseException) as err:
        print (err)
    return user

# Empleado para apis del backend
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401

from features.core.auth.routes_back import app as app_auth
from features.core.auth.routes_front import app as app_auth_front, get_login
from features.recomendacion.routes_frontend import app as app_recomendacion_front
from features.recomendacion.routes_backend import app as app_recomendacion_back
from features.visitantetipo.routes_frontend import app as app_visitantetipo_front
from features.visitantetipo.routes_backend import app as app_visitantetipo_back
from features.clasificacion.routes_backend import app as app_clasificacion_back
from features.clasificacion.routes_frontend import app as app_clasificacion_front
from features.escuela.routes_frontend import app as app_escuela_front
from features.escuela.routes_backend import app as app_escuela_back
from features.escuelanivel.routes_frontend import app as app_escuelanivel_front
from features.escuelanivel.routes_backend import app as app_escuelanivel_back
from features.tipoAcervo.routes_frontend import app as app_tipoAcervo_front
from features.tipoAcervo.routes_backend import app as app_tipoAcervo_back
from features.areas_fisicas.routes_frontend import app as app_areafisica_front
from features.areas_fisicas.routes_backend import app as app_areafisica_back
from features.editorial.routes_frontend import app as app_editorial_front
from features.editorial.routes_backend import app as app_editorial_back
from features.backups.routes_backend import app as app_backup_back
from features.afiliado.routes_frontend import app as app_afiliado_front
from features.afiliado.routes_backend import app as app_afiliado_back
from features.personal.routes_backend import app as app_personal_back
from features.personal.routes_frontend import app as app_personal_front
from features.mapa.routes_backend import app as app_mapa_back
from features.user.routes_frontend import app as app_user_front
from features.user.routes_backend import app as app_user_back
from features.registro_visita.routes_backend import app as app_visita_front
from features.registro_visita.routes_frontend import app as app_visita_back
from features.prestamo.routes_backend import app  as app_prestamo_back
from features.prestamo.routes_frontend import app as app_prestamo_front
from features.personal.routes_frontend import app as app_personal_front
from features.personal.routes_backend import app as app_personal_back
from features.estado.routes_frontend import app as app_estado_front
from features.estado.routes_backend import app as app_estado_back
from features.municipio.routes_frontend import app as app_municipio_front
from features.municipio.routes_backend import app as app_municipio_back
from features.ciudad.routes_frontend import app as app_ciudad_front
from features.ciudad.routes_backend import app as app_ciudad_back
from features.estante.routes_frontend import app as app_estante_front
from features.estante.routes_backend import app as app_estante_back
from features.acervotitulo.routes_frontend import app as app_acervotitulo_front
from features.acervotitulo.routes_backend import app as app_acervotitulo_back
from features.acervoejemplar.routes_frontend import app as app_acervoEjemplar_front
from features.acervoejemplar.routes_backend import app as app_acervoEjemplar_back

app.register_blueprint(app_auth)
app.register_blueprint(app_auth_front)
app.register_blueprint(app_recomendacion_back)
app.register_blueprint(app_recomendacion_front)
app.register_blueprint(app_clasificacion_back)
app.register_blueprint(app_clasificacion_front)
app.register_blueprint(app_escuela_back)
app.register_blueprint(app_escuela_front)
app.register_blueprint(app_escuelanivel_back)
app.register_blueprint(app_escuelanivel_front)
app.register_blueprint(app_tipoAcervo_back)
app.register_blueprint(app_tipoAcervo_front)
app.register_blueprint(app_areafisica_back)
app.register_blueprint(app_areafisica_front)
app.register_blueprint(app_editorial_back)
app.register_blueprint(app_editorial_front)
app.register_blueprint(app_visitantetipo_back)
app.register_blueprint(app_visitantetipo_front)
app.register_blueprint(app_backup_back)
app.register_blueprint(app_afiliado_back)
app.register_blueprint(app_afiliado_front)
app.register_blueprint(app_visita_back)
app.register_blueprint(app_visita_front)
app.register_blueprint(app_prestamo_back)
app.register_blueprint(app_prestamo_front)
app.register_blueprint(app_user_back)
app.register_blueprint(app_user_front)
app.register_blueprint(app_personal_back)
app.register_blueprint(app_personal_front)
app.register_blueprint(app_mapa_back)
app.register_blueprint(app_ciudad_back)
app.register_blueprint(app_ciudad_front)
app.register_blueprint(app_estado_back)
app.register_blueprint(app_estado_front)
app.register_blueprint(app_municipio_back)
app.register_blueprint(app_municipio_front)
app.register_blueprint(app_estante_back)
app.register_blueprint(app_estante_front)
app.register_blueprint(app_acervotitulo_back)
app.register_blueprint(app_acervotitulo_front)
app.register_blueprint(app_acervoEjemplar_back)
app.register_blueprint(app_acervoEjemplar_front)



@app.route("/api/movil/login", methods=["POST"])
@csrf.exempt
def api_login_json():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({'errors': {'fields': 'Username and password are required'} }), 400
        if len(username) > 50 or len(password) > 50:
            return {"error": "El nombre de usuario y la contraseña no deben exceder los 50 caracteres."}, 400
        
        user = User.query.filter(User.username == username).first()
        if not user or not user.check_password(password):
            return jsonify({'statusCode':401,'message':  'Wrong username or password' }), 401
        if not user.is_active:
            return jsonify({'errors': {'fields': 'Inactive account'} }), 401

        response = jsonify({'data': user.get_json()})
        return response
    except Exception as err:
        print(err)
        return jsonify({'errors': 'Internal server error'}), 500

@app.get('/api/movil/acervoprestamosafiliado')
def prestamos_get_all_afiliado():
    try:
        data = request.json
        username = data.get("username")
        if len(username) > 50:
            return {"error": "El nombre de usuario y la contraseña no deben exceder los 50 caracteres."}, 400
        prestamocu = PrestamoCU(  )
        # Obtener los datos de paginación
        # Obtener los registros paginados y retornarlos
        registros = prestamocu.get_prestamo_afiliado(username)
        return jsonify ( {'data': registros } )
    except Exception as err:
        print(err)
        return jsonify({'errors': 'Internal server error'}), 500
    
@app.get('/api/movil/cantidadprestamosafiliado')
def get_cantidad_prestamos_afiliado():
    try:
        data = request.json
        username = data.get("username")
        if len(username) > 50:
            return {"error": "El nombre de usuario y la contraseña no deben exceder los 50 caracteres."}, 400
        prestamocu = PrestamoCU(  )
        # Obtener los datos de paginación
        # Obtener los registros paginados y retornarlos
        cantidad = prestamocu.get_cantidad_prestamos_pendientes_afiliado(username)
        return jsonify ( {'cantidad': cantidad } )
    except Exception as err:
        print(err)
        return jsonify({'errors': 'Internal server error'}), 500
    
@app.get('/api/movil/acervoprestamosadmin')
def prestamos_get_all_admin():
    try:
        prestamocu = PrestamoCU(  )
        # Obtener los datos de paginación
        # Obtener los registros paginados y retornarlos
        registros = prestamocu.get_prestamos_admim()
        return jsonify ( {'data': registros } )
    except Exception as err:
        print(err)
        return jsonify({'errors': 'Internal server error'}), 500

@app.get('/api/movil/notificaciones')
def get_notificaciones():
    try:
        data = request.json
        username = data.get("username")
        if len(username) > 50:
            return {"error": "El nombre de usuario y la contraseña no deben exceder los 50 caracteres."}, 400
        prestamocu = PrestamoCU(  )
        # Obtener los datos de paginación
        # Obtener los registros paginados y retornarlos
        registros = prestamocu.get_notificaciones(username)
        return jsonify ( {'data': registros } )
    except Exception as err:
        print(err)
        return jsonify({'errors': 'Internal server error'}), 500

@app.route("/", methods=["GET"])
def get_index():
    usuario_autenticado = False
    resp = None
    try:
        resp = verify_jwt_in_request(optional=True)
    except (BaseException) as err:
        pass
    # preparar los datos para el público en general
    page = "indexpublic.html"
    obj_form = AcervotituloForm()
    context={
        'obj_form': obj_form,
        'usuario_autenticado' : False
    }
    if resp != None:
        # Si el usuario está autentificado
        usuario_autenticado = True
        is_admin = True
        if current_user.tipo != "2":
            is_admin = False
        page = "index.html"
        context={ 
            'temp_form': LoginForm(),
            'usuario_autenticado' : usuario_autenticado,
            'is_admin': is_admin,
            'full_name': current_user.full_name
        }
    return render_template (page, **context)

@app.route("/admin_sys", methods=["GET"])
def get_index_admin():
    try:
        # resp = verify_jwt_in_request(optional=True, locations=["cookies"], verify_type=False )
        resp = verify_jwt_in_request(optional=True)
        if resp == None:
            return redirect(url_for("AuthRoute.get_login"))
    except (BaseException) as err :
        print(err.args[0])
        response = make_response( get_login() )
        if err.args[0] in ['Signature has expired', 'Signature verification failed']:
            # clear cookies
            unset_jwt_cookies(response)
            logout_user()
        return response

    context={ 
            'temp_form': LoginForm(),
            'usuario_autenticado' : True
             }
    return render_template ("index.html", **context)

def create_user(username_given, email, full_name, passwd, public_id, tipo):
    user: User = db.session.query(User).filter_by(username=username_given).first()
    if user == None:
        user = User(username_given, email, full_name, passwd, public_id, tipo)
        user.encrypt_password()
        db.session.add(user)
        db.session.commit()

with app.app_context():
    try:
        db.create_all()
        create_user("alfonso", "alfonso@hotmail.com", "Lic. Jose Alfonso Cruz Rodas", "alfonso", str(uuid.uuid4()), "2" ) # 1 = Afiliado
        create_user("test", "test@hotmail.com", "Bruce Wayne", "test", str(uuid.uuid4()), "1" ) # 2 = Admin
    except (BaseException) as err:
        print(err.__dict__)

# def insert_recomendacion():
#     engine = create_engine(os.environ.get('DATABASE_URL'))
#     # Lee el archivo CSV utilizando pandas
#     df = pd.read_csv('recomendaciones.csv')

#     # Realiza la inserción en la base de datos utilizando sqlalchemy
#     with engine.connect() as connection:
#         df.to_sql('recomendacion', connection, index=False, if_exists='append')

# # Llama a la función para realizar la inserción
# flag = False
# if flag:
#     insert_recomendacion()

if __name__ == "__main__":
    # Ejecución sin ssl: flask --app main run --debug
    app.run()

    # Ejecución con ssl: python main.py
    # app.run (host='0.0.0.0', port=5000, ssl_context='adhoc')
    