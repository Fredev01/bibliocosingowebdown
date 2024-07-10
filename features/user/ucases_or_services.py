import uuid
from flask_jwt_extended import current_user
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.user.models import User, UserForm
from features.core.bd import db, execute_query


class UserCU():
    def get_all(self, param_limit, search_value):
        # Prepara la condición de filtrado
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, ' ', 'username', 'like', search_value, ' ')
        if cond:
            cond = f"WHERE {cond}"
        
        # Obtener el total de registros a retornar
        sql_query = f"SELECT COUNT(1) FROM user {cond}"
        registros = execute_query(sql_query, sqlParams)
        total = registros[0][0]

        # Obtener los registros a retornar
        sql_query = f"""
            SELECT u.id, u.username, u.email, u.is_active,u.tipo,u.full_name
            FROM user u
            {cond} {param_limit}
            """
        registros = execute_query(sql_query, sqlParams)

        # Retornar el total y los registros
        return total, registros
        
    def save(self, data : UserForm):
        email_existe = None
        if data.id is None or data.id.data == '':
            obj = User.query.filter(User.username == data.username.data).first() or None
            objEmail = User.query.filter(User.email == data.email.data).first() or None
            if obj :
                return {"obj": None}
            if objEmail:
                return {"obj": "email_exist"}
        else:
            objValid = User.query.filter(User.username==data.username.data).first() or None
            objExistEmail = User.query.filter(User.email==data.email.data).first() or None
            if objValid :
                if objValid.id != int(data.id.data):
                    return {"obj": None}
            if objExistEmail:
                email_existe = self.get_email_exist(data.email.data)
                if email_existe:
                    if objValid.email != data.email.data:
                        return {"obj":"email_exist"}
            obj = User.query.get(data.id.data)

        if obj is None:
            obj = User()
            obj.public_id = str(uuid.uuid4())
            
        if len(data.passwd.data) > 0:
            obj.passwd = data.passwd.data
            obj.encrypt_password()

        obj.username = data.username.data
        obj.email = data.email.data
        obj.tipo = data.tipo.data
        obj.is_active = data.is_active.data
        obj.full_name = data.full_name.data
        # obj.id_personal = current_user.id

        db.session.add(obj)
        db.session.commit()

        return {"obj": obj.get_data()}
 
    def delete(self, id : int):
        obj = User.query.filter(User.id == id).first()
        if obj == None:
            return {"oper": None}
        else:
            # Hacer el delete del obj en la BD
            db.session.delete(obj)
            db.session.commit()
            return { "oper": True }
        
    def generar(self):
        # Preparar la condición a filtrar
        cond = ""
        sqlParams = {}
        
        # Obtener los registros a retornar
        sql_query = f"""
            SELECT u.id, 
                u.username, 
                u.full_name, 
                u.email, 
                CASE u.tipo 
                    WHEN 1 THEN 'afiliado' 
                    WHEN 2 THEN 'admin' 
                    ELSE 'otro' 
                END AS tipo_etiqueta, 
                CASE u.is_active 
                    WHEN 0 THEN 'no' 
                    WHEN 1 THEN 'si' 
                    ELSE 'desconocido' 
                END AS is_active_etiqueta
            FROM user u
            {cond} 
        """
        result = execute_query(sql_query, sqlParams)

# Crear objeto PDF con orientación horizontal
        pdf = FPDF(orientation='L')
        pdf.add_page()

        col_widths = [10, 40, 73, 70, 30, 20]  # Ancho de las columnas
        row_height = 8 # Altura de las filas
        page_width = pdf.w - 2 * pdf.l_margin

        pdf.image("static/img/log.png", x=10, y=10, w=30)  # Ajusta las coordenadas (x, y) y el tamaño (w) según tus necesidades

        color_titulo = (0, 0, 0)  # Color para los títulos
        color_fondo = (244, 229, 192)  # Color arenoso para el fondo de las celdas
        color_texto = (0, 0, 0)  # Color para el texto
        
        pdf.set_fill_color(*color_fondo)  # Color de fondo de las celdas
        pdf.set_text_color(*color_texto)  # Color de texto

        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)
        pdf.set_text_color(*color_titulo)  # Aplicar color a los títulos
        pdf.cell(page_width, 0.0, 'Biblioteca municipal "Fray Pedro de Laurecio"', align='C')
        pdf.ln(8)
        pdf.set_font('Times', 'B', 15.0)
        pdf.cell(page_width, 0.0, 'Ocosingo.Chis', align='C')

        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)        
        pdf.cell(page_width, 0.0, 'Registro de Usuarios', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 10)  # Cambio de fuente y negrita para los títulos de las columnas

# Agregar títulos a las columnas
        titles = ['Id', 'Cuenta', 'Nombre', 'Correo', 'Tipo.U', 'Activo?']
        for title, width in zip(titles, col_widths):
            pdf.set_margin(25)
            pdf.cell(width, row_height, title, border=3, align='C')
        pdf.ln(row_height)

        pdf.set_font('Arial', '', 10)  # Restaurar la fuente normal y reducir tamaño
        
        # Agregar datos de la tabla
        alternating_color = False

        for row in result:           
            if alternating_color:   # Cambiar el color de fondo para filas alternas
                pdf.set_fill_color(*color_fondo)
            else:
                pdf.set_fill_color(255, 255, 255)  
            alternating_color = not alternating_color # Color blanco para filas alternas
            for item, width in zip(row, col_widths):
                pdf.cell(width, row_height, str(item), align="C", border=1, fill=True)
            pdf.ln(row_height)

        return pdf
    

    
    def get_email_exist(self, email):
        sql_params = {}
        sql_query = f"""
        select u.email from user u
        WHERE u.email = '{email}'
        """
        registros = execute_query( sql_query, sql_params) or []

        return registros[0][0] if len(registros) > 0 else None

        def get_combo(self, data : dict):
                cond = ""
                condId = ""
                sqlParams = {}
                if data.get('q'):
                    cond += prepParam(sqlParams, '', 'e.titulo', 'like', data.get('q'), ' ')
                if data.get('id'):
                    condId = prepParam(sqlParams, '', 'e.id', '=', data.get('id'), ' ')
                if cond and condId:
                    cond = " where " + cond + ' and ' + condId
                elif cond or condId:
                    cond = " where " + cond + condId

                # Para los combos, retornar el id y el texto a mostrar como item del select
                sql_query = "select id, email text from user e " + cond
                registros = execute_query( sql_query, sqlParams)

                return registros