import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.escuelanivel.models import EscuelanivelForm
from features.escuelanivel.ucases_or_services import EscuelanivelCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('EscuelanivelAPIs', __name__, url_prefix='/escuelanivel/api/')

@app.get('/escuelanivel')
@jwt_required()
def escuelasnivel_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelanivelcu = EscuelanivelCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = escuelanivelcu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_escuelanivel_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelanivel_form = EscuelanivelForm()
        if escuelanivel_form.validate_on_submit():
            objEscuelanivel = EscuelanivelCU()
            resp = objEscuelanivel.save(escuelanivel_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'La escuela ya se encuentra registrado' }
            else:
                return {'errormsg': 'La escuela ya se encuentra registrado' }
        else:
            return {'errors': escuelanivel_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/escuela')
@jwt_required()
def escuelanivel_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelanivelcu = EscuelanivelCU()
        escuelanivel_form = EscuelanivelForm()
        return jsonify ( {'data': escuelanivelcu.delete(escuelanivel_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def escuelanivel_get_combo():
    """API que retorna todos los registros de nivel de escuela para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        escuelanivelcu = EscuelanivelCU( )
        return {'data': escuelanivelcu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelanivelcu = EscuelanivelCU()
        # Obtener los registros paginados y retornarlos
        pdf = escuelanivelcu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=NivelEscolar_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)
