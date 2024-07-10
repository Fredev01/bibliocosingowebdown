from flask import Blueprint, Response, jsonify
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.recomendacion.models import RecomendacionForm
from features.recomendacion.ucases_or_services import RecomendacionCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('RecomendacionAPIs', __name__, url_prefix='/recomendacion/api/')

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


@app.get('/recomendacions')
@jwt_required()
def recomendacions_get_all():
    try:
        recomendacioncu = RecomendacionCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = recomendacioncu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_recomendacion_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        recomendacion_form = RecomendacionForm()
        if recomendacion_form.validate_on_submit():
            objRecomendacion = RecomendacionCU()
            resp = objRecomendacion.save(recomendacion_form)
            if resp:
                return {'success': 'ok', 'data':resp['obj'] }
            else:
                return {'errormsg': 'El recomendacion ya se encuentra registrado' }
        else:
            return {'errors': recomendacion_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/recomendacion')
@jwt_required()
def recomendacion_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        recomendacioncu = RecomendacionCU()
        recomendacion_form = RecomendacionForm()
        return jsonify ( {'data': recomendacioncu.delete(recomendacion_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        recomendacioncu = RecomendacionCU()
        # Obtener los registros paginados y retornarlos
        pdf = recomendacioncu.generar()
        
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        # return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=escuelas_reporte.pdf'})
        return Response(pdf_bytes, mimetype='application/pdf')

    except Exception as err:
        return response_bad_request(err)

