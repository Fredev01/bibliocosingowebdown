from flask_jwt_extended import current_user
from features.core.projectdefs import prepParam
from features.notificacion.models import Notificacion, NotificacionForm
from features.core.bd import db, execute_query


class NotificacionCU():
    def get_all(self, param_limit, search_value):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, ' ', 'notificacion', 'like', search_value, ' ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f"select count(1) From notificacion {cond}"
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]

        # Obtener los registros a retornar
        sql_query = f"""
            select t.id, idUser, t.mensaje
            from notificacion t
            
            {cond} {param_limit}
            """
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return total, registros

        
    def save(self, data : NotificacionForm):
        if (data.id.data == None or data.id.data == ''  ) :
            objList = Notificacion.query.filter(Notificacion.nombre==data.nombre.data).first() or []
        else:
            objList = Notificacion.query.filter(Notificacion.id == data.id.data).all()
        obj : Notificacion = objList[0] if len(objList)>0 else None
        if obj == None:
            obj = Notificacion()
        obj.nombre= data.nombre.data, 
        
        # Obtener el registro directamente del id del usuario actualmente autentificado
        # ignorando el recibido del cliente
        # obj.registro_id= data.registro_id.data
        #obj.registro_id= current_user.id
        # Hacer el insert en la BD
        db.session.add(obj)
        db.session.commit()
        return { "obj": obj.get_data() }
 
    def delete(self, id : int):
        obj = Notificacion.query.filter(Notificacion.id == id).first()
        if obj == None:
            return {"oper": None}
        else:
            # Hacer el delete del obj en la BD
            db.session.delete(obj)
            db.session.commit()
            return { "oper": True }

