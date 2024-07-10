import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.tipoAcervo.models import TipoForm
from features.tipoAcervo.ucases_or_services import TipoCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('TipoAPIs', __name__, url_prefix='/tipo/api/')

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


@app.get('/tipos')
@jwt_required()
def tipos_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        tipocu = TipoCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = tipocu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_tipo_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        tipo_form = TipoForm()
        if tipo_form.validate_on_submit():
            objTipo = TipoCU()
            resp = objTipo.save(tipo_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El tipo de acervo ya se encuentra registrado.' }
            else:
                return {'errormsg': 'El tipo ya se encuentra registrado' }
        else:
            return {'errors': tipo_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/tipo')
@jwt_required()
def tipo_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        tipocu = TipoCU()
        tipo_form = TipoForm()
        return jsonify ( {'data': tipocu.delete(tipo_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        tipocu = TipoCU()
        # Obtener los registros paginados y retornarlos
        pdf = tipocu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=TipoAcervos_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def tipo_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    if current_user.tipo != "2":
        return {'errormsg': 'Acceso Restringido' }
    try:
        query_form = request.args.to_dict()
        tipocu = TipoCU( )
        return {'data': tipocu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
