from features.core.projectdefs import prepParam
from features.core.bd import execute_query

class UserCU():
    def get_combo(self, data : dict):
        cond = ""
        condId = ""
        sqlParams = {}
        if data.get('q'):
            cond += prepParam(sqlParams, '(', 'u.username', 'like', data.get('q'), 'or')
            cond += prepParam(sqlParams, '', 'u.email', 'like', data.get('q'), ')')
        if data.get('id'):
            condId = prepParam(sqlParams, '', 'u.id', '=', data.get('id'), ' ')
        if cond and condId:
            cond = " where " + cond + ' and ' + condId
        elif cond or condId:
            cond = " where " + cond + condId

        # Para los combos, retornar el id y el texto a mostrar como item del select
        sql_query = "select id, concat(username, ' ' ) text from user u " + cond
        registros = execute_query( sql_query, sqlParams)

        return registros
    
    def get_combo_afiliado(self, data: dict):
        cond = ""
        sqlParams = {}
        # Construir la condición de búsqueda para 'username' y 'email'
        if data.get('q'):
            cond += prepParam(sqlParams, '(', 'u.username', 'like', data.get('q'), 'or')
            cond += prepParam(sqlParams, '', 'u.email', 'like', data.get('q'), ')')

        # No necesitamos condId aquí, ya que parece que solo afecta al tipo de usuario.
        # Siempre agregaremos la condición del tipo de usuario.
        condTipo = prepParam(sqlParams, '', 'u.tipo', '=', "1", ' ')

        if cond:
            cond = " where " + cond

        # Si hay alguna condición, agregamos la condición del tipo de usuario
        if cond:
            cond += ' and ' + condTipo
        else:
            cond = " where " + condTipo

        # Para los combos, retornar el id y el texto a mostrar como item del select
        sql_query = "select id, concat(username, ' ' ) text from user u " + cond
        registros = execute_query(sql_query, sqlParams)

        return registros
    
    def get_combo_admin(self, data: dict):
        cond = ""
        sqlParams = {}
        # Construir la condición de búsqueda para 'username' y 'email'
        if data.get('q'):
            cond += prepParam(sqlParams, '(', 'u.username', 'like', data.get('q'), 'or')
            cond += prepParam(sqlParams, '', 'u.email', 'like', data.get('q'), ')')

        # No necesitamos condId aquí, ya que parece que solo afecta al tipo de usuario.
        # Siempre agregaremos la condición del tipo de usuario.
        condTipo = prepParam(sqlParams, '', 'u.tipo', '=', "2", ' ')

        if cond:
            cond = " where " + cond

        # Si hay alguna condición, agregamos la condición del tipo de usuario
        if cond:
            cond += ' and ' + condTipo
        else:
            cond = " where " + condTipo

        # Para los combos, retornar el id y el texto a mostrar como item del select
        sql_query = "select id, concat(username, ' ' ) text from user u " + cond
        registros = execute_query(sql_query, sqlParams)

        return registros

    