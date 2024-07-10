import datetime
from urllib import request
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.estado.models import EstadoForm
from features.estado.ucases_or_services import EstadoCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('EstadoAPIs', __name__, url_prefix='/estado/api/')

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


@app.get('/estados')
@jwt_required()
def estados_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        estadocu = EstadoCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = estadocu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_estado_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        estado_form = EstadoForm()
        if estado_form.validate_on_submit():
            objEstado = EstadoCU()
            resp = objEstado.save(estado_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El estado ya se encuentra registrado' }
            else:
                return {'errormsg': 'El estado ya se encuentra registrado' }
        else:
            return {'errors': estado_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/estado')
@jwt_required()
def estado_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        estadocu = EstadoCU()
        estado_form = EstadoForm()
        return jsonify ( {'data': estadocu.delete(estado_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        estadocu = EstadoCU()
        # Obtener los registros paginados y retornarlos
        pdf = estadocu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Estados_{fecha_actual}.pdf'})
        # return Response(pdf_bytes, mimetype='application/pdf')

    except Exception as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def escuela_get_combo():
    """API que retorna todos los registros de estados para combos"""
    try:
        query_form = request.args.to_dict()
        estadocu = EstadoCU( )
        return {'data': estadocu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
