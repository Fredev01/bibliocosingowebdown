from flask import Blueprint, redirect, render_template, url_for
from flask_jwt_extended import current_user
from features.core.auth.routes_back import user_has_session
from features.recomendacion.models import RecomendacionForm

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('RecomendacionPages', __name__, url_prefix='/recomendacion')

@app.get('/')
def get_recomendacion():
    try:
        if not user_has_session():
            return redirect( url_for("AuthRoute.get_login", ret=url_for("RecomendacionPages.get_recomendacion") ) )        
        obj_form = RecomendacionForm()
        context={
            'obj_form': obj_form,
            'usuario_autenticado' : True,
            'full_name': current_user.full_name
        }
        return render_template ("recomendacion.html", **context)
    except BaseException as err:
        print(err)

    return redirect( url_for("AuthRoute.get_login") )

