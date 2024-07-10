import datetime
from urllib import request
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.ciudad.models import CiudadForm
from features.ciudad.ucases_or_services import CiudadCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('CiudadAPIs', __name__, url_prefix='/ciudad/api/')

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


@app.get('/ciudads')
@jwt_required()
def ciudads_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        ciudadcu = CiudadCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = ciudadcu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_ciudad_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        ciudad_form = CiudadForm()
        if ciudad_form.validate_on_submit():
            objCiudad = CiudadCU()
            resp = objCiudad.save(ciudad_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El ciudad ya se encuentra registrado' }
            else:
                return {'errormsg': 'El ciudad ya se encuentra registrado' }
        else:
            return {'errors': ciudad_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/ciudad')
@jwt_required()
def ciudad_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        ciudadcu = CiudadCU()
        ciudad_form = CiudadForm()
        return jsonify ( {'data': ciudadcu.delete(ciudad_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)


@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        ciudadcu = CiudadCU()
        # Obtener los registros paginados y retornarlos
        pdf = ciudadcu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Ciudades_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def escuela_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        query_form = request.args.to_dict()
        ciudadcu = CiudadCU( )
        return {'data': ciudadcu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
