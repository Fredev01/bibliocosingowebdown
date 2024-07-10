from flask_jwt_extended import current_user
from fpdf import FPDF
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.personal.models import PersonalForm, Personal
from features.core.bd import db, execute_query

class PersonalCU():
    def get_all(self, param_limit, search_value):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, ' ', 'p.nombre', 'like', search_value, ' ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f"select count(1) From personal p LEFT JOIN user u ON u.id = p.user_id {cond}"
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]
        # Obtener los registros a retornar
        sql_query = f"""
            select p.id,  p.nombre, p.apellidos, p.correo, p.phone, u.id user_id, u.username 
            from personal p
            LEFT JOIN user u ON u.id = p.user_id
            {cond} {param_limit}
            """
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return total, registros

        
    def save(self, data : PersonalForm):
        user_existe = None
        email_existe = None
        phone_existe = None
        user_id = int(data.user_id.data)
        if (data.id.data == None or data.id.data == ''):
            objList = Personal.query.filter(Personal.nombre==data.nombre.data).all() or []
            objUserExist = Personal.query.filter(Personal.user_id==data.user_id.data).first() or None
            objEmailExist = Personal.query.filter(Personal.correo==data.correo.data).first() or None
            objPhoneExist = Personal.query.filter(Personal.phone==data.phone.data).first() or None
            if objUserExist:
                return {"obj": None}
            if objEmailExist:
                return {"obj":"email_exist"}
            if objPhoneExist:
                return {"obj": "phone_exist"}
        else:
            objList = Personal.query.filter(Personal.id == data.id.data).all()
            if len(objList)>0:
                user_existe = self.get_user_exist(user_id)
                email_existe = self.get_email_exist(data.correo.data)
                print(email_existe)
                phone_existe = self.get_phone_exist(data.phone.data)
                if user_existe:
                    if objList[0].user_id != user_id:
                        return {"obj": None}
                if email_existe:
                    if objList[0].correo != data.correo.data:
                        return {"obj":"email_exist"}
                if phone_existe:
                    if objList[0].phone != data.phone.data:
                        return {"obj": "phone_exist"}
        obj : Personal = objList[0] if len(objList)>0 else None
        if obj == None:
            user_existe = Personal.query.filter_by(user_id=data.user_id.data).first()
            if user_existe:
                return {"obj": None}
            obj = Personal()
        obj.nombre= data.nombre.data, 
        obj.apellidos = data.apellidos.data,
        obj.correo = data.correo.data,
        obj.phone = data.phone.data
        obj.user_id = data.user_id.data
        # Hacer el insert en la BD
        db.session.add(obj)
        db.session.commit()
        return { "obj": obj.get_data() }
 
    def delete(self, id : int):
        obj = Personal.query.filter(Personal.id == id).first()
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
            select p.id,  p.nombre, p.apellidos, p.correo, p.phone
            from personal p
            {cond} 
        """
        result = execute_query(sql_query, sqlParams)

        pdf = FPDF()
        pdf.add_page()

        col_widths = [10, 80, 50]  # Ancho de las columnas
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
        pdf.cell(page_width, 0.0, 'Registros de Areas Fisicas', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 10)  # Cambio de fuente y negrita para los títulos de las columnas
        pdf.cell(page_width, 0.0, 'Registros de Personal', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 12)  # Cambio de fuente y negrita para los títulos de las columnas

        # Agregar títulos a las columnas
        titles = ['ID', 'Nombres', 'Apellidos', 'Correo', 'telefono' ]
        for title, width in zip(titles, col_widths):
            pdf.set_margin(30)
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
    
    def get_combo(self, data : dict):
        cond = ""
        condId = ""
        sqlParams = {}
        if data.get('q'):
            cond += prepParam(sqlParams, '', 'e.nombre', 'like', data.get('q'), ' ')
        if data.get('id'):
            condId = prepParam(sqlParams, '', 'e.id', '=', data.get('id'), ' ')
        if cond and condId:
            cond = " where " + cond + ' and ' + condId
        elif cond or condId:
            cond = " where " + cond + condId

        # Para los combos, retornar el id y el texto a mostrar como item del select
        sql_query = "select id, nombre text from personal e " + cond
        registros = execute_query( sql_query, sqlParams)

        return registros
    
    def get_user_exist(self, user_id):
        sql_params = {}
        sql_query = f"""
        select pe.user_id from personal pe 
        WHERE pe.user_id = {user_id}
        """
        registros = execute_query( sql_query, sql_params) or []

        return registros[0][0] if len(registros) > 0 else None
    
    def get_email_exist(self, email):
        sql_params = {}
        sql_query = f"""
        select pe.correo from personal pe 
        WHERE pe.correo = '{email}'
        """
        registros = execute_query( sql_query, sql_params) or []

        return registros[0][0] if len(registros) > 0 else None
    
    def get_phone_exist(self, phone):
        sql_params = {}
        sql_query = f"""
        select pe.phone from personal pe 
        WHERE pe.phone = {phone}
        """
        registros = execute_query( sql_query, sql_params) or []

        return registros[0][0] if len(registros) > 0 else None
