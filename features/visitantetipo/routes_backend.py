import datetime
from flask import Blueprint, jsonify, request
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.visitantetipo.models import VisitantetipoForm
from features.visitantetipo.ucases_or_services import VisitantetipoCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('VisitantetipoAPIs', __name__, url_prefix='/visitantetipo/api/')




@app.get('/visitantetipos')
@jwt_required()
def visitantetipos_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        visitantetipocu = VisitantetipoCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = visitantetipocu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_visitantetipo_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        visitantetipo_form = VisitantetipoForm()
        if visitantetipo_form.validate_on_submit():
            objVisitantetipo = VisitantetipoCU()
            resp = objVisitantetipo.save(visitantetipo_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El visitantetipo ya se encuentra registrado' }
            else:
                return {'errormsg': 'El visitantetipo ya se encuentra registrado' }
        else:
            return {'errors': visitantetipo_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/visitantetipo')
@jwt_required()
def visitantetipo_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        visitantetipocu = VisitantetipoCU()
        visitantetipo_form = VisitantetipoForm()
        return jsonify ( {'data': visitantetipocu.delete(visitantetipo_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)


@app.get('/getcombo')
@jwt_required()
def visitantetipo_get_combo():
    """API que retorna todos los registros de afiliados para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        visitantetipocu = VisitantetipoCU( )
        return {'data': visitantetipocu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        visitantetipocu = VisitantetipoCU()
        # Obtener los registros paginados y retornarlos
        pdf = visitantetipocu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=TipoVisitante_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)
