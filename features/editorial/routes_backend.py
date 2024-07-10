import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.editorial.models import EditorialForm
from features.editorial.ucases_or_services import EditorialCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('EditorialAPIs', __name__, url_prefix='/editorial/api/')


@app.get('/editoriales')
@jwt_required()
def editoriales_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        editorialcu = EditorialCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = editorialcu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_editorial_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        editorial_form = EditorialForm()
        if editorial_form.validate_on_submit():
            objEditorial = EditorialCU()
            resp = objEditorial.save(editorial_form)
            if resp:
                if resp["obj"]:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'La editorial ya se encuentra registrado' }
            else:
                return {'errormsg': 'La editorial ya se encuentra registrado' }
        else:
            return {'errors': editorial_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/editorial')
@jwt_required()
def editorial_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        editorialcu = EditorialCU()
        editorial_form = EditorialForm()
        return jsonify ( {'data': editorialcu.delete(editorial_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)
        
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        editorialcu = EditorialCU()
        # Obtener los registros paginados y retornarlos
        pdf = editorialcu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Editoriales_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)


@app.get('/getcombo')
@jwt_required()
def editorial_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        editorialcu = EditorialCU( )
        return {'data': editorialcu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
