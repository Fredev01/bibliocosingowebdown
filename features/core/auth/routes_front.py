from flask import Blueprint, redirect, render_template, request, url_for
from flask_jwt_extended import verify_jwt_in_request
from features.core.auth.model import LoginForm

app = Blueprint("AuthRoute", __name__, url_prefix="/auth")

@app.route("/login", methods=["GET"])
def get_login():
    try:
        # resp = verify_jwt_in_request(optional=True, locations=["cookies"], verify_type=False )
        resp = verify_jwt_in_request(optional=True)
        # print (resp)
        if resp != None:
            return redirect (url_for("get_index_admin"))
    except (BaseException) as err :
        print(err)
    # Si se tiene que autentificar por que expiró su sesión 
    # retornar la ruta a donde se encontraba para facilitar su reinicio
    ret = request.args.get("ret", "/")
    context = { 'login_form': LoginForm() 
               , 'ret' : ret
               }
    return render_template ("login.html", **context)
