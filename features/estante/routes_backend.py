import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.estante.models import EstanteForm
from features.estante.ucases_or_services import EstanteCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('EstanteAPIs', __name__, url_prefix='/estante/api/')


@app.get('/estantes')
@jwt_required()
def estantes_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        estantecu = EstanteCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = estantecu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_estante_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        estante_form = EstanteForm()
        if estante_form.validate_on_submit():
            objEstante = EstanteCU()
            resp = objEstante.save(estante_form)
            if resp:
                if resp['obj']:
                    if resp['obj'] == "nivel_mayor" :
                        return {'errormsg': 'El número de niveles debe ser menor a 13.' }
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El estante ya se encuentra registrado' }
            else:
                return {'errormsg': 'El estante ya se encuentra registrado' }
        else:
            return {'errors': estante_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/estante')
@jwt_required()
def estante_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        estantecu = EstanteCU()
        estante_form = EstanteForm()
        return jsonify ( {'data': estantecu.delete(estante_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def estante_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        estantecu = EstanteCU( )
        return {'data': estantecu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelacu = EstanteCU()
        # Obtener los registros paginados y retornarlos
        pdf = escuelacu.generar()
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Estantes_reporte_{fecha_actual}.pdf'})
        # return Response(pdf_bytes, mimetype='application/pdf')

    except Exception as err:
        return response_bad_request(err)
