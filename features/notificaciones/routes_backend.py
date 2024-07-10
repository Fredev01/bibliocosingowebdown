from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.notificacion.models import NotificacionForm
from features.notificacion.ucases_or_services import NotificacionCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('NotificacionAPIs', __name__, url_prefix='/notificacion/api/')

@app.route("/who_am_i", methods=["GET"])
@jwt_required()
# @check_access(roles=["admin", "teacher"])
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username,
    )


@app.get('/notificaciones')
@jwt_required()
def notificaciones_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        notificacioncu = NotificacionCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = notificacioncu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_notificacion_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        notificacion_form = NotificacionForm()
        if notificacion_form.validate_on_submit():
            objNotificacion = NotificacionCU()
            resp = objNotificacion.save(notificacion_form)
            if resp:
                return {'success': 'ok', 'data':resp['obj'] }
            else:
                return {'errormsg': 'El notificacion ya se encuentra registrado' }
        else:
            return {'errors': notificacion_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/notificacion')
@jwt_required()
def notificacion_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        notificacioncu = NotificacionCU()
        notificacion_form = NotificacionForm()
        return jsonify ( {'data': notificacioncu.delete(notificacion_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

