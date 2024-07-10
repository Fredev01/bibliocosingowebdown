
import datetime
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.areas_fisicas.models import AreaFisicaForm
from features.areas_fisicas.ucases_or_services import AreaFisicaCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('AreaFisicaAPIs', __name__, url_prefix='/areafisica/api/')

@app.get('/areafisica')
@jwt_required()
def area_fisica_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        areafisicacu = AreaFisicaCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = areafisicacu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_area_fisica_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        areafisica_form = AreaFisicaForm()
        if areafisica_form.validate_on_submit():
            objAreaFisica = AreaFisicaCU()
            resp = objAreaFisica.save(areafisica_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El área física ya se encuentra registrada.' }
            else:
                return {'errormsg': 'El Area Fisica ya se encuentra registrada' }
        else:
            return {'errors': areafisica_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/areafisicas')
@jwt_required()
def area_fisica_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        areafisicacu = AreaFisicaCU()
        areafisica_form = AreaFisicaForm()
        return jsonify ( {'data': areafisicacu.delete(areafisica_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)
    


@app.get('/getcombo')
@jwt_required()
def areasfisicas_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        areasfisicascu = AreaFisicaCU( )
        return {'data': areasfisicascu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        areafisicacu = AreaFisicaCU()
        # Obtener los registros paginados y retornarlos
        pdf = areafisicacu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=AreasFisicas_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)

