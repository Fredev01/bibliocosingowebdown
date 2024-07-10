import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.acervoejemplar.models import AcervoejemplarForm
from features.acervoejemplar.ucases_or_services import AcervoejemplarCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('AcervoejemplarAPIs', __name__, url_prefix='/acervoejemplar/api/')


@app.get('/acervoejemplares/<acervotitulo_id>')
@jwt_required()
def acervoejemplares_get_all(acervotitulo_id : int):
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        acervoejemplarcu = AcervoejemplarCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = acervoejemplarcu.get_all(param_limit, search_value, acervotitulo_id)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_acervoejemplar_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        acervoejemplar_form = AcervoejemplarForm()
        if acervoejemplar_form.validate_on_submit():
            objAcervoejemplar = AcervoejemplarCU()
            resp = objAcervoejemplar.save(acervoejemplar_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data': resp['obj']}
                else:
                    return {'errormsg': 'El nivel del estante seleccionado es mayor al que se encuentra registrado o el número de adquisición ya está en uso.'}
            else:
                return {'errormsg': 'El ejemplar o #deAdquisición, ya se encuentra registrado'}
        else:
            return {'errors': acervoejemplar_form.errors}
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/acervoejemplar')
@jwt_required()
def acervoejemplar_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        acervoejemplarcu = AcervoejemplarCU()
        acervoejemplar_form = AcervoejemplarForm()
        return jsonify ( {'data': acervoejemplarcu.delete(acervoejemplar_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def acervoejemplar_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        acervoejemplarcu = AcervoejemplarCU( )
        return {'data': acervoejemplarcu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
    
@app.get('/getejemplaresde/<acervo_id>')
# @jwt_required()
def acervoejemplar_get_ejemplaresde(acervo_id: int):
    """API que retorna los ejemplares asociados a un acervo_id"""
    try:
        acervoejemplarcu = AcervoejemplarCU( )
        # return {'data': acervoejemplarcu.get_ejemplaresde(acervo_id) }
        total, registros = acervoejemplarcu.get_ejemplaresde(acervo_id)
        return jsonify ( {"draw":"1","recordsTotal":total ,"recordsFiltered":total,'data': registros } )

    except (BaseException) as err:
        return response_bad_request(err)    
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        acervoejemplarcu = AcervoejemplarCU()
        # Obtener los registros paginados y retornarlos
        pdf = acervoejemplarcu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=AcervoEjemplar_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)
