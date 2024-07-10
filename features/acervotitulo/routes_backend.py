import datetime
import os
from flask import Blueprint, Response, jsonify, request, send_from_directory
from flask_jwt_extended import current_user, jwt_required
from features.core.projectdefs import getPageDataRequested, getUploadsPathBase, response_bad_request
from features.acervotitulo.models import AcervotituloFileForm, AcervotituloForm
from features.acervotitulo.ucases_or_services import AcervotituloCU
from werkzeug.utils import secure_filename

# Rutas o EndPoints compuestas con el prefijo referente a la feature actual (user)
app = Blueprint('AcervotituloAPIs', __name__, url_prefix='/acervotitulo/api/')


@app.route('/acervosT', methods=["GET", "POST"])
# @jwt_required()
def acervosT_get_all():
    try:
        acervotitulocu = AcervotituloCU()
        # Obtener los datos de paginación
        draw, search_value, param_limit = getPageDataRequested()
        # en el cliente se hace la petición vía post
        if request.method == "POST":
            draw, search_value, param_limit = getPageDataRequested(data_by = "form")
            
        # Obtener los registros paginados y retornarlos
        total, registros = acervotitulocu.get_all(param_limit, search_value)
        return jsonify ( {"draw":draw,"recordsTotal":total ,"recordsFiltered":total,'data': registros } )
    except (BaseException) as err:
        return response_bad_request(err)


@app.post('/add')
@jwt_required()
def api_acervotitulo_add():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        acervotitulo_form = AcervotituloForm()
        if acervotitulo_form.validate_on_submit():
            objAcervotitulo = AcervotituloCU()
            resp = objAcervotitulo.save(acervotitulo_form)
            if resp:
                return {'success': 'ok', 'data':resp['obj'] }
            else:
                return {'errormsg': 'El título indicado ya se encuentra registrado' }
        else:
            return {'errors': acervotitulo_form.errors }
    except (BaseException) as err:
        return response_bad_request(err)

@app.delete('/acervotitulo')
@jwt_required()
def acervotitulo_delete():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        acervotitulocu = AcervotituloCU()
        acervotitulo_form = AcervotituloForm()
        # return jsonify ( {'data': acervotitulocu.delete(acervotitulo_form.id.data)} )
        return jsonify ( {'data': {"oper": None} })
    except (BaseException) as err:
        return response_bad_request(err)

dir_files = "acervo"
tipo_esperado_1 = "foto"
@app.post('/img_up/<tipo>')
@jwt_required()
def reg_upload_file(tipo: str = tipo_esperado_1):
    # Asegurar que el tipo recibido sea del tipo esperado
    tipo = tipo_esperado_1 if tipo not in [tipo_esperado_1,] else tipo
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        form = AcervotituloFileForm()
        if form.validate_on_submit():
            idReg = dict(request.form).get("id") or 0 # OBLIGATORIO. Cualquier archivo recibido debe recibirse con un id
            acervocu = AcervotituloCU()
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

@app.get('/getcombo')
@jwt_required()
def acervotitulo_get_combo():
    """API que retorna todos los registros de esculas para combos"""
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }
        query_form = request.args.to_dict()
        acervotitulocu = AcervotituloCU( )
        return {'data': acervotitulocu.get_combo(query_form) }
    except (BaseException) as err:
        return response_bad_request(err)
    
@app.route('/download/report/pdf')
@jwt_required()
def download_report():
    try:
        if current_user.tipo != "2":
            return {'errormsg': 'Acceso Restringido' }

        acervotitulocu = AcervotituloCU()
        # Obtener los registros paginados y retornarlos
        pdf = acervotitulocu.generar()
        
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Convertir el PDF a bytes
        pdf_bytes = bytes(pdf.output(dest='S'))
        
        return Response(pdf_bytes, mimetype='application/pdf', headers={'Content-Disposition': f'attachment;filename=AcervoTitulo_{fecha_actual}.pdf'})

    except Exception as err:
        return response_bad_request(err)

