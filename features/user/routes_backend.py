import datetime
import json
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.user.models import UserForm
from features.user.ucases_or_services import UserCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('UserAPIs', __name__, url_prefix='/user/api/')



@app.get('/users')
@jwt_required()
def users_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        usercu = UserCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = usercu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_user_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        user_form = UserForm()
        if user_form.validate_on_submit():
            objUser = UserCU()
            resp = objUser.save(user_form)
            if resp:
                if resp['obj']:
                    if resp['obj'] == "email_exist":
                        return  {'errormsg': 'El correo ya se encuentra registrado.' }
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El Nombre de usuario ya se encuentra registrado' }
            else:
                return {'errormsg': 'El Nombre de usuario ya se encuentra registrado' }
        else:
            return {'errors': user_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


@app.delete('/user')
@jwt_required()
def user_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        usercu = UserCU()
        user_form = UserForm()
        # Validar que no se pueda borrar al usuario actualmente autentificado
        # y que debe existir al menos un usuario administrador vigente
        if user_form.id.data == str(current_user.id):
            # return {'errormsg': 'No se puede eliminar al usuario actual' }
            # return response_bad_request("No se puede eliminar al usuario actual")
            return jsonify ({'data': {"oper": None, 'errormsg': 'No se puede eliminar al usuario actual'}} )

        return jsonify ( {'data': usercu.delete(user_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        usercu = UserCU()
        # Obtener los registros paginados y retornarlos
        pdf = usercu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Usuarios_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def user_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        usercu = UserCU( )
        return {'data': usercu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)