from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import current_user, verify_jwt_in_request
from features.core.auth.routes_back import user_has_session

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('DireccionPages', __name__, url_prefix='/direccion')

@app.get('/')
def get_mostrar_mapa():

        usuario_autenticado = False
        resp = None
        user_name = None
        try:
            resp = verify_jwt_in_request(optional=True)
        except (BaseException) as err:
            pass
        if resp != None:
            usuario_autenticado = True
        if current_user:
            user_name = current_user.full_name
        context={ 
            # 'temp_form': LoginForm(),
            'usuario_autenticado' : usuario_autenticado,
            'full_name': user_name
        }
        return render_template ("mapa.html", **context)
        # return render_template('mapa.html')

