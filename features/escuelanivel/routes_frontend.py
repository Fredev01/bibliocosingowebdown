from flask import Blueprint, redirect, render_template, url_for
from flask_jwt_extended import current_user
from features.core.auth.routes_back import user_has_session
from features.escuelanivel.models import EscuelanivelForm

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('EscuelanivelPages', __name__, url_prefix='/escuelanivel')

@app.get('/')
def get_escuelanivel():
    try:
        if not user_has_session():
            return redirect( url_for("AuthRoute.get_login", ret=url_for("EscuelanivelPages.get_escuelanivel") ) )        
        usuario_autenticado = True
        if current_user.tipo != "2":
            return render_template ("sinacceso.html", usuario_autenticado=usuario_autenticado)
        obj_form = EscuelanivelForm()
        context={
            'obj_form': obj_form,
            'usuario_autenticado' : True,
            'full_name': current_user.full_name
        }
        return render_template ("escuelanivel.html", **context)
    except BaseException as err:
        print(err)

    return redirect( url_for("AuthRoute.get_login") )

