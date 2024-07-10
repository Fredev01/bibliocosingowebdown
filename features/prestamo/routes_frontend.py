from flask import Blueprint, redirect, render_template, url_for
from features.core.auth.routes_back import user_has_session
from features.prestamo.models import AcervoPrestamoDevolverForm, AcervoPrestamoExtensionForm, AcervoPrestamoForm
from datetime import datetime, timedelta
from flask_jwt_extended import current_user
# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('AcervoPrestamoPages', __name__, url_prefix='/acervoprestamo')

@app.get('/')
def get_acervoprestamo():
    try:
        if not user_has_session():
            return redirect( url_for("AuthRoute.get_login", ret=url_for("AcervoPrestamoPages.get_acervoprestamo") ) )        
        usuario_autenticado = True
        if current_user.tipo != "2":
            return render_template ("sinacceso.html", usuario_autenticado=usuario_autenticado)
        obj_form = AcervoPrestamoForm()
        obj_form_devolver = AcervoPrestamoDevolverForm()
        obj_form_extension = AcervoPrestamoExtensionForm()
        context = {
            'obj_form': obj_form,
            'obj_form_devolver': obj_form_devolver,
            'obj_form_extension':obj_form_extension,
            'usuario_autenticado': True,
            'full_name': current_user.full_name
        }
        return render_template ("acervoprestamo.html", **context)
    except BaseException as err:
        print(err)

    return redirect( url_for("AuthRoute.get_login") )

@app.get('/afiliado')
def get_acervoprestamo_afiliado():
    try:
        if not user_has_session():
            return redirect( url_for("AuthRoute.get_login", ret=url_for("AcervoPrestamoPages.get_acervoprestamo") ) )        
        # usuario_autenticado = True
        # if current_user.tipo != "2":
        #     return render_template ("sinacceso.html", usuario_autenticado=usuario_autenticado)
        # obj_form = AcervoPrestamoForm()
        # obj_form_devolver = AcervoPrestamoDevolverForm()
        # obj_form_extension = AcervoPrestamoExtensionForm()
        context = {
            'usuario_autenticado': True,
            'full_name': current_user.full_name
        }
        return render_template ("acervoprestamoafiliado.html", **context)
    except BaseException as err:
        print(err)

    return redirect( url_for("AuthRoute.get_login") )
