import json
from flask import Response

def response_bad_request(msgError, status_code_given = None):
    """Función que retornará una respuesta de status 500 de forma predeterminada, con el msgError indicado"""
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
