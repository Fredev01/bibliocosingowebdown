import datetime
import os
from flask import Blueprint, Response, jsonify, request, request, send_from_directory
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, response_bad_request,getUploadsPathBase
from features.registro_visita.ucases_or_services import RegistroVisitaCU
from features.registro_visita.models import RegistroVisitaForm, VisitaFileForm
from werkzeug.utils import secure_filename

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (registro_visita)
app = Blueprint('RegistroVisitaAPIs', __name__, url_prefix='/registro_visita/api/')

@app.get('/registrosvisita')
@jwt_required()
def registros_get_all():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        registro_cu = RegistroVisitaCU()
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # Obtener los registros paginados y retornarlos
        total, registros = registro_cu.get_all(param_limit, search_value)
        return jsonify({"draw": draw, "recordsTotal": total, "recordsFiltered": total, 'data': registros})
    except (BaseException) as err:
        return response_bad_request(err)

@app.post('/add')
@jwt_required()
def api_registro_visita_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        registro_form = RegistroVisitaForm()
        if registro_form.validate_on_submit():
            objRegistroVisita = RegistroVisitaCU()
            resp = objRegistroVisita.save(registro_form)
            if resp:
                if resp['obj'] == "bibliusuario_id_vacio":
                    return {'errormsg': 'Debe seleccionar un visitante.'}
                if resp['obj'] == "escuela_id_vacio":
                    return {'errormsg': 'Debe seleccionar una escuela.'}
                if resp['obj'] == "visitantetipo_id_vacio":
                    return {'errormsg': 'Debe seleccionar el tipo de visitante.'}
                return {'success': 'ok', 'data': resp['obj']}
            else:
                return {'errormsg': 'Error al agregar el registro de visita'}
        else:
            return {'errors': registro_form.errors}
    except (BaseException) as err:
        return response_bad_request(err)

@app.delete('/registro')
@jwt_required()
def registro_visita_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        registro_cu = RegistroVisitaCU()
        registro_form = RegistroVisitaForm()
        return jsonify({'data': registro_cu.delete(registro_form.id.data)})
    except (BaseException) as err:
        return response_bad_request(err)
    

@app.get('/getcombo')
@jwt_required()
def registro_visita_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        query_form = request.args.to_dict()
        registro_cu = RegistroVisitaCU( )
        return {'data': registro_cu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        registro_cu = RegistroVisitaCU()
        # Obtener los registros paginados y retornarlos
        pdf = registro_cu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=RegistroVisitas_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)


dir_files = "visitas"
tipo_esperado_1 = "foto"
@app.post('/img_up/<tipo>')
@jwt_required()
def reg_upload_file(tipo: str = tipo_esperado_1):
    # Asegurar que el tipo recibido sea del tipo esperado
    tipo = tipo_esperado_1 if tipo not in [tipo_esperado_1,] else tipo
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        form = VisitaFileForm()
        if form.validate_on_submit():
            idReg = dict(request.form).get("id") or 0 # OBLIGATORIO. Cualquier archivo recibido debe recibirse con un id
            acervocu = RegistroVisitaCU()
            objReg = acervocu.get_reg(idReg)
            if objReg == None:
                return response_bad_request("No existe ningún registro asociado", 404) #status.HTTP_404_NOT_FOUND)
            file = form.file.data
            # fhms = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"{idReg}_{tipo}_{secure_filename(file.filename)}"
            print('filename: ', filename)
            file.save( os.path.join( getUploadsPathBase([dir_files]), filename) )
            # actualizar el nombre del archivo en la BD
            acervocu.save_file(idReg, filename)
            return {'success': 'ok', 'data':{'filename': filename} }
        else:
            return {'errors': form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.get('/img_down/<filename>')
# @jwt_required()
def reg_download_file(filename: str):
    # simplemente retornar el archivo solicitado
    return send_from_directory( getUploadsPathBase([dir_files]), filename)
