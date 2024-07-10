import datetime
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.municipio.models import MunicipioForm
from features.municipio.ucases_or_services import MunicipioCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('MunicipioAPIs', __name__, url_prefix='/municipio/api/')

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


@app.get('/municipios')
@jwt_required()
def municipios_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        municipiocu = MunicipioCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = municipiocu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_municipio_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        municipio_form = MunicipioForm()
        if municipio_form.validate_on_submit():
            objMunicipio = MunicipioCU()
            resp = objMunicipio.save(municipio_form)
            if resp:
                if resp["obj"]:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El municipio ya se encuentra registrado' }
            else:
                return {'errormsg': 'El municipio ya se encuentra registrado' }
        else:
            return {'errors': municipio_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.delete('/municipio')
@jwt_required()
def municipio_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        municipiocu = MunicipioCU()
        municipio_form = MunicipioForm()
        return jsonify ( {'data': municipiocu.delete(municipio_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        municipiocu = MunicipioCU()
        # Obtener los registros paginados y retornarlos
        pdf = municipiocu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Municipios_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)

# @app.get('/getcombo')
# @jwt_required()
# def escuela_get_combo():
#     """API que retorna todos los registros de estados para combos"""
#     try:
#         query_form = request.args.to_dict()
#         estadocu = EstadoCU( )
#         return {'data': estadocu.get_combo(query_form) }
#     except (BaseException) as err:
#         return response_bad_request(err)
