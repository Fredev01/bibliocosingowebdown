import json
import os
from os.path import exists

from flask import Response, request

def getPageDataRequested(data_by = "args"):
    search_value = ""
    start = 0   # num de página
    length = 10 #tamaño de página
    draw = 1
    param_limit = f"LIMIT {start},{length}"
    try:
        if data_by == "args":
            data = dict(request.args)
        if data_by == "form":
            data = dict(request.form)
        
        start = (int(data['start']))
        length = (int(data['length']))
        draw = 1 if data.get('draw') == None else int(data['draw'])
        search_value = "" if (data['search[value]'] == None) else data['search[value]']
        # param_limit = "" if (length == -1) else f"LIMIT {start},{length}"
        # asegurarnos que el tamaño máximo sea 1000 registros
        length = length if (length <=1000) else 1000
        param_limit = f"LIMIT {start},{length}"
    except (BaseException) as err2:
        print ("getPageDataRequested: " + str(err2) )
    return draw, search_value, param_limit

def response_bad_request(msgError, status_code_given = None):
    # Función que retornará una respuesta de status 500 de forma predeterminada, con el msgError indicado
    print("Error: ", msgError)
    msgErrorToSend = str(msgError)
    try:
        posMissing = msgErrorToSend.find("missing")
        if ( "SQLAlchemyError" in msgErrorToSend or "HTTPException" in msgErrorToSend or \
            "pymysql.err.OperationalError" in msgErrorToSend ):
            msgErrorToSend = "Error en el Servicio, o temporalmente suspendido"
        elif ( posMissing > 0  ):
            msgErrorToSend = msgErrorToSend[posMissing:]
            status_code_given = 400 #status.HTTP_400_BAD_REQUEST
    except (BaseException) as err:
        pass
    if status_code_given == None:
        status_code_given = 500 #status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response( json.dumps( {'errors': {'message':msgErrorToSend} } ), status_code_given, \
                    content_type='application/json')

def getUploadsPathBase(dir_given):
    # upload_dir = f"{os.getcwd()}/uploads/{dir_given}/"
    upload_dir = os.path.join(os.getcwd(), "uploads")
    for dir in dir_given:
        upload_dir = os.path.join(upload_dir, dir)
    if not exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir

def prepParam(sqlParams, parentesisOpen, campoTbl, comparacion, valor, parentesisCloseAndOr):
    # Preparar parámetro para consulta sql
    cond = ""
    if (valor):
        campoTblLimpio = campoTbl.replace(".","_")
        cond = f"{parentesisOpen} {campoTbl} {comparacion} :{campoTblLimpio} {parentesisCloseAndOr} "
        if (comparacion=="like"):
            sqlParams[campoTblLimpio] = f'%{valor}%'
        else:
            sqlParams[campoTblLimpio] = valor
    return cond
