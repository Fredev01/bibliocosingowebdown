import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.clasificacion.ucases_or_services import ClasificacionCU
from features.clasificacion.models import ClasificacionForm

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('ClasificacionAPIs', __name__, url_prefix='/clasificacion/api/')



@app.get('/clasificaciones')
@jwt_required()
def clasificaciones_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        clasificacioncu = ClasificacionCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = clasificacioncu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_clasificacion_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        clasificacion_form = ClasificacionForm()
        if clasificacion_form.validate_on_submit():
            objClasificacion = ClasificacionCU()
            resp = objClasificacion.save(clasificacion_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'La clasificación ya se encuentra registrada' }
            else:
                return {'errormsg': 'El recomendacion ya se encuentra registrado' }
        else:
            return {'errors': clasificacion_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/clasificacion')
@jwt_required()
def clasificacion_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        clasificacioncu = ClasificacionCU()
        clasificacion_form = ClasificacionForm()
        return jsonify ( {'data': clasificacioncu.delete(clasificacion_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)
    

@app.get('/getcombo')
@jwt_required()
def clasificacion_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        clasificacioncu = ClasificacionCU( )
        return {'data':clasificacioncu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        clasificacioncu = ClasificacionCU()
        # Obtener los registros paginados y retornarlos
        pdf = clasificacioncu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Clasificaciones_{fecha_actual}.pdf'})
    except Exception as err:
        return response_bad_request(err)

