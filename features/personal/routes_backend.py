import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.personal.models import PersonalForm
from features.personal.ucases_or_services import PersonalCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('PersonalAPIs', __name__, url_prefix='/personal/api/')


@app.get('/personals')
@jwt_required()
def personals_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        personalcu = PersonalCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = personalcu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_personal_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        personal_form = PersonalForm()
        if personal_form.validate_on_submit():
            objPersonal = PersonalCU()
            resp = objPersonal.save(personal_form)
            if resp:
                if resp['obj']:
                    if resp['obj'] == "email_exist":
                        return {'errormsg': 'El correo ya se encuentra asociado a un personal.' }
                    if resp['obj'] == "phone_exist":
                        return {'errormsg': 'El número de teléfono ya se encuentra asociado a un personal.' }
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El usuario ya se encuentra asociado a un personal' }
            else:
                return {'errormsg': 'El personal ya se encuentra registrado' }
        else:
            return {'errors': personal_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/personal')
@jwt_required()
def personal_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        personalcu = PersonalCU()
        personal_form = PersonalForm()
        return jsonify ( {'data': personalcu.delete(personal_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def personal_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        personalcu = PersonalCU( )
        return {'data': personalcu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        personalcu = PersonalCU()
        # Obtener los registros paginados y retornarlos
        pdf = personalcu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Personal_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)