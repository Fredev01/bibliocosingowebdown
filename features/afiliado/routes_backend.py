import datetime
import os
from flask import Blueprint, Response, jsonify, request, send_from_directory
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request, getUploadsPathBase
from features.afiliado.models import AfiliadoFileForm, AfiliadoForm
from features.afiliado.ucases_or_services import AfiliadoCU
from werkzeug.utils import secure_filename


# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('AfiliadoAPIs', __name__, url_prefix='/afiliado/api/')

@app.get('/afiliados')
@jwt_required()
def afiliados_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        afiliadocu = AfiliadoCU()
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = afiliadocu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_afiliado_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        afilaido_form = AfiliadoForm()
        if afilaido_form.validate_on_submit():
            objAfiliado = AfiliadoCU()
            resp = objAfiliado.save(afilaido_form)
            if resp:
                if resp['obj']:
                    return {'success': 'ok', 'data':resp['obj'] }
                else:
                    return {'errormsg': 'El usuario que se desea asignar ya se encuentra registrado' }
            else:
                return {'errormsg': 'El usuario afiliado ya se encuentra registrado' }
        else:
            return {'errors': afilaido_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.delete('/afiliado')
@jwt_required()
def afiliado_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        afiliadocu = AfiliadoCU()
        afiliado_form = AfiliadoForm()
        return jsonify ( {'data': afiliadocu.delete(afiliado_form.id.data)} )
    except (BaseException) as err:
        return response_bad_request(err)

@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        afiliadocu = AfiliadoCU()
        # Obtener los registros paginados y retornarlos
        pdf = afiliadocu.generar()
        
        # Convertir el PDF a bytes
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=Afiliados_{fecha_actual}.pdf'})
        # return Response(pdf_bytes, mimetype='application/pdf')

    except Exception as err:
        return response_bad_request(err)

@app.get('/getcombo')
@jwt_required()
def afiliado_get_combo():
    """API que retorna todos los registros de afiliados para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        afiliadocu = AfiliadoCU( )
        return {'data': afiliadocu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)

dir_files_frente = "afiliado_frente"
tipo_esperado_1_frente = "foto"
@app.post('/img_up_frente/<tipo>')
@jwt_required()
def reg_upload_file_frente(tipo: str = tipo_esperado_1_frente):
    # Asegurar que el tipo recibido sea del tipo esperado
    tipo = tipo_esperado_1_frente if tipo not in [tipo_esperado_1_frente,] else tipo
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        form = AfiliadoFileForm()
        if form.validate_on_submit():
            idReg = dict(request.form).get("id") or 0 # OBLIGATORIO. Cualquier archivo recibido debe recibirse con un id
            afiliadocu = AfiliadoCU()
            objReg = afiliadocu.get_reg(idReg)
            if objReg == None:
                return response_bad_request("No existe ningún registro asociado", 404) #status.HTTP_404_NOT_FOUND)
            file = form.file.data
            # fhms = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"{idReg}_{tipo}_{secure_filename(file.filename)}"
            print('filename: ', filename)
            file.save( os.path.join( getUploadsPathBase([dir_files_frente]), filename) )
            # actualizar el nombre del archivo en la BD
            afiliadocu.save_file_frente(idReg, filename)
            return {'success': 'ok', 'data':{'filename': filename} }
        else:
            return {'errors': form.errors }
    except (BaseException) as err:
        return response_bad_request(err)


dir_files_reverso = "afiliado_reverso"
tipo_esperado_1_reverso = "foto"
@app.post('/img_up_reverso/<tipo>')
@jwt_required()
def reg_upload_file_reverso(tipo: str = tipo_esperado_1_reverso):
    # Asegurar que el tipo recibido sea del tipo esperado
    tipo = tipo_esperado_1_reverso if tipo not in [tipo_esperado_1_reverso,] else tipo
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        form = AfiliadoFileForm()
        if form.validate_on_submit():
            idReg = dict(request.form).get("id") or 0 # OBLIGATORIO. Cualquier archivo recibido debe recibirse con un id
            afiliadocu = AfiliadoCU()
            objReg = afiliadocu.get_reg(idReg)
            if objReg == None:
                return response_bad_request("No existe ningún registro asociado", 404) #status.HTTP_404_NOT_FOUND)
            file = form.file.data
            # fhms = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"{idReg}_{tipo}_{secure_filename(file.filename)}"
            print('filename: ', filename)
            file.save( os.path.join( getUploadsPathBase([dir_files_reverso]), filename) )
            # actualizar el nombre del archivo en la BD
            afiliadocu.save_file_reverso(idReg, filename)
            return {'success': 'ok', 'data':{'filename': filename} }
        else:
            return {'errors': form.errors }
    except (BaseException) as err:
        return response_bad_request(err)
    
@app.get('/img_down_frente/<filename>')
# @jwt_required()
def reg_download_file_frente(filename: str):
    # simplemente retornar el archivo solicitado
    return send_from_directory( getUploadsPathBase([dir_files_frente]), filename)

@app.get('/img_down_reverso/<filename>')
# @jwt_required()
def reg_download_file_reverso(filename: str):
    # simplemente retornar el archivo solicitado
    return send_from_directory( getUploadsPathBase([dir_files_reverso]), filename)