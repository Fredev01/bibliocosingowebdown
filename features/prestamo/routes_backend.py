import datetime
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request
from features.prestamo.models import AcervoPrestamoDevolverForm, AcervoPrestamoExtensionForm, AcervoPrestamoForm
from features.prestamo.ucases_or_services import PrestamoCU

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('AcervoPrestamoAPIs', __name__, url_prefix='/acervoprestamo/api/')

@app.get('/acervoprestamos')
@jwt_required()
def prestamos_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        prestamocu = PrestamoCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        respuesta = prestamocu.get_all(param_limit, search_value)
        if respuesta['Prestamo']:
            pdf = respuesta['data']
            print(pdf)
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            nombre_archivo = f'Prestamos_{fecha_actual}.pdf'
            # Convertir el PDF a bytes
            pdf_bytes = bytes(pdf.output(dest='S'))
            return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Prestamos_{fecha_actual}.pdf'})
        else:
            return jsonify ( {"draw":draw,"recordsTotal":respuesta['total'] ,"recordsFiltered":respuesta['total'],'data': respuesta['registros'] } )
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/acervoprestamosafiliado')
@jwt_required()
def prestamos_get_all_afiliado():
    try:
        # if current_user.tipo != "2":
        #     return {'errormsg': 'Acceso Restringido' }
        prestamocu = PrestamoCU(  )
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = prestamocu.get_by_afiliado(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)

@app.post('/add')
@jwt_required()
def api_acervoprestamo_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        prestamo_form = AcervoPrestamoForm()
        if prestamo_form.validate_on_submit():
            objPrestamo = PrestamoCU()
            resp = objPrestamo.save(prestamo_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': "El acervo ejemplar ya está prestado y no puede ser prestado nuevamente." }
            
            else:
                return {'errormsg': 'error de al registrar en la BD' }
        else:
            return {'errors': prestamo_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.post('/devolver')
@jwt_required()
def api_acervoprestamo_devolver():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        prestamo_form = AcervoPrestamoDevolverForm()
        if prestamo_form.validate_on_submit():
            objPrestamo = PrestamoCU()
            resp = objPrestamo.save_devolucion(prestamo_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': "El prestamo no existe." }
            else:
                return {'errormsg': 'error de al registrar en la BD' }
        else:
            return {'errors': prestamo_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.post('/extension')
@jwt_required()
def api_acervoprestamo_extension():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        prestamo_form = AcervoPrestamoExtensionForm()
        if prestamo_form.validate_on_submit():
            objPrestamo = PrestamoCU()
            resp = objPrestamo.save_extension(prestamo_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': "La fecha de devolución planificada no coincide con la fecha originalmente registrada." }
            else:
                return {'errormsg': 'error de al registrar en la BD' }
        else:
            return {'errors': prestamo_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def acervo_get_combo():
    if current_user.tipo != "2":
        return {'errormsg': 'Acceso Restringido' }
    """API que retorna todos los registros de afiliados para combos"""
    try:
        query_form = request.args.to_dict()
        prestamocu = PrestamoCU( )
        return {'data': prestamocu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)