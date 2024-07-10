from flask import Blueprint, redirect, render_template, url_for
from features.core.auth.routes_back import user_has_session
from features.acervoejemplar.models import AcervoejemplarForm
from flask_jwt_extended import current_user
# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('AcervoejemplarPages', __name__, url_prefix='/acervoejemplar')

@app.get('/<acervotitulo_id>')
def get_acervoejemplar(acervotitulo_id : int):
    try:
        if not user_has_session():
            return redirect( url_for("AuthRoute.get_login", ret=url_for("AcervoejemplarPages.get_acervoejemplar") ) )        
        usuario_autenticado = True
        if current_user.tipo != "2":
            return render_template ("sinacceso.html", usuario_autenticado=usuario_autenticado)
        obj_formejemplar = AcervoejemplarForm()
        context={
            'obj_formejemplar': obj_formejemplar,
            'usuario_autenticado' : True,
            'full_name': current_user.full_name,
            'acervotitulo_idDado' : acervotitulo_id
        }
        return render_template ("acervoejemplar.html", **context)
    except BaseException as err:
        print(err)

    return redirect( url_for("AuthRoute.get_login") )

