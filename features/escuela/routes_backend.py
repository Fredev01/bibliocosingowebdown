import datetime
from flask import Blueprint, jsonify, request
from flask import Blueprint, Response, jsonify
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import current_user, jwt_required
from fpdf import FPDF
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.escuela.models import EscuelaForm
from features.escuela.ucases_or_services import EscuelaCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('EscuelaAPIs', __name__, url_prefix='/escuela/api/')

@app.get('/escuelas')
@jwt_required()
def escuelas_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelacu = EscuelaCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = escuelacu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_escuela_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuela_form = EscuelaForm()
        if escuela_form.validate_on_submit():
            objEscuela = EscuelaCU()
            resp = objEscuela.save(escuela_form)
            if resp:
                if resp['obj']:
                    if resp['obj'] == "nivel_vacio":
                        return {'errormsg': 'Debe seleccionar un nivel escolar' }
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'La escuela ya se encuentra registrado' }
            else:
                return {'errormsg': 'La escuela ya se encuentra registrado' }
        else:
            return {'errors': escuela_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/escuela')
@jwt_required()
def escuela_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelacu = EscuelaCU()
        escuela_form = EscuelaForm()
        return jsonify ( {'data': escuelacu.delete(escuela_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)
    
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        escuelacu = EscuelaCU()
        # Obtener los registros paginados y retornarlos
        pdf = escuelacu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Escuelas_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)


@app.get('/getcombo')
@jwt_required()
def escuela_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    if current_user.tipo != "2":
        return {'errormsg': 'Acceso Restringido' }
    try:
        query_form = request.args.to_dict()
        escuelacu = EscuelaCU( )
        return {'data': escuelacu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
