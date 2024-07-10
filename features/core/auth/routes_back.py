from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required, \
    set_access_cookies, unset_jwt_cookies, verify_jwt_in_request
from flask_login import login_user, logout_user
from features.core.auth.model import LoginForm, User
from features.core.auth.ucases_or_services import UserCU
from features.core.projectdefs import response_bad_request

app = Blueprint("AuthApi", __name__, url_prefix="/api/auth")

def user_has_session():
    try:
        # resp = verify_jwt_in_request(optional=True, locations=["cookies"], verify_type=False )
        resp = verify_jwt_in_request(optional=True)
        if resp != None:
            return True
    except BaseException as err:
        print ("user_has_session()")
        print (err)
    return False


@app.route("/login", methods=["POST"])
def api_login():
    try:
        obj_form = LoginForm()
        if not obj_form.validate_on_submit():
            return {'errors': obj_form.errors }
        # username = request.form.get("username", None)
        # password = request.form.get("password", None)
        user: User = User.query.filter(User.username == obj_form.username.data).first()
        if not user or not user.check_password(obj_form.password.data):
            return {'errors': {'fields':'Wrong username or password'} }, 401
        if not user.is_active:
            return {'errors': {'fields':'Inactive account'} }, 401

        user.passwd = "" # limpiar el pwd para que no sea accesible en la web
        access_token = create_access_token(identity=user)
        ## refresh_token = create_refresh_token(identity=user)
        ## response = jsonify({'success': 'ok', 'access_token':access_token, 'refresh_token':refresh_token, 'data':user.get_json() })
        response = jsonify({'success': 'ok', 'access_token':access_token, 'data':user.get_json() })
        set_access_cookies(response, access_token)
        # response.set_cookie('username', user.username)
        login_user(user)
        return response
    except (BaseException) as err:
        print(err)
        return response_bad_request(err)


@app.route("/logout", methods=["GET", "DELETE"])
def logout():
    response = jsonify({"ok": True})
    unset_jwt_cookies(response)
    logout_user()
    return response


@app.get('/getcombo')
@jwt_required()
def users_get_combo():
    """API que retorna todos los registros de cuentas de usuario para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        usercu = UserCU( )
        return {'data': usercu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
    

@app.get('/getcomboafiliado')
@jwt_required()
def users_afiliado_get_combo():
    """API que retorna todos los registros de cuentas de usuario para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        usercu = UserCU( )
        return {'data': usercu.get_combo_afiliado(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/getcomboadmin')
@jwt_required()
def users_admin_get_combo():
    """API que retorna todos los registros de cuentas de usuario para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        usercu = UserCU( )
        return {'data': usercu.get_combo_admin(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)

