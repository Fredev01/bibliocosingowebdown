from flask_jwt_extended import current_user
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.afiliado.models import Afiliado, AfiliadoForm
from features.core.bd import db, execute_query

class AfiliadoCU():
    def get_all(self, param_limit, search_value):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, '( ', 'a.nombrecompleto', 'like', search_value, ' or ')
            cond += prepParam(sqlParams, ' ', 'u.username', 'like', search_value, ' ) ')
            
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f"""select count(1) From afiliado a
        LEFT JOIN user u ON u.id = a.user_id {cond}
        """
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]

        # Obtener los registros a retornar
        sql_query = f"""
            select a.id, a.nombrecompleto, DATE_FORMAT(a.fechanacimiento, '%Y/%m/%d')
                , a.sexo, a.capacidaddiferente, a.observaciones, a.credencialfrente, a.credencialreverso,
                u.id user_id, u.username 
            from afiliado a  
            LEFT JOIN user u ON u.id = a.user_id
            {cond} {param_limit}
            """
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return total, registros

    def get_combo(self, data : dict):
        cond = ""
        condId = ""
        sqlParams = {}
        if data.get('q'):
            cond += prepParam(sqlParams, '', 'e.nombrecompleto', 'like', data.get('q'), ' ')
        if data.get('id'):
            condId = prepParam(sqlParams, '', 'e.id', '=', data.get('id'), ' ')
        if cond and condId:
            cond = " where " + cond + ' and ' + condId
        elif cond or condId:
            cond = " where " + cond + condId

        # Para los combos, retornar el id y el texto a mostrar como item del select
        sql_query = "select id, nombrecompleto text from afiliado e " + cond
        registros = execute_query( sql_query, sqlParams)

        return registros
        
        
    def save(self, data : AfiliadoForm):
        user_existe = None
        user_id = data.user_id.data
        if (user_id):
            user_id = int(user_id)
        if (data.id.data == None):
            objList = Afiliado.query.filter(Afiliado.nombrecompleto==data.nombrecompleto.data).first() or None
        else:
            objList = Afiliado.query.filter(Afiliado.id == data.id.data).all()
            if len(objList)>0 and user_id:
                user_existe = self.get_user_exist(user_id)
                if user_existe:
                    if objList[0].user_id != user_id:
                        return {"obj": None}
        obj : Afiliado = objList[0] if len(objList)>0 else None
        if obj == None:
            if user_id:
                user_existe = Afiliado.query.filter_by(user_id=data.user_id.data).first()
                if user_existe:
                    return {"obj": None}
            obj = Afiliado()
        obj.nombrecompleto= data.nombrecompleto.data, 
        obj.fechanacimiento= data.fechanacimiento.data,
        obj.sexo= data.sexo.data,
        obj.capacidaddiferente= data.capacidaddiferente.data,
        obj.observaciones= data.observaciones.data,
        obj.user_id = data.user_id.data,
        # Hacer el insert en la BD
        db.session.add(obj)
        db.session.commit()
        return { "obj": obj.get_data() }
 
    def delete(self, id : int):
        obj = Afiliado.query.filter(Afiliado.id == id).first()
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
            SELECT a.id, a.nombrecompleto, DATE_FORMAT(a.fechanacimiento, '%Y/%m/%d')
                , a.sexo, a.capacidaddiferente, a.observaciones
            FROM afiliado a    
            {cond} 
        """
        result = execute_query(sql_query, sqlParams)

        # Crear objeto PDF con orientación horizontal
        pdf = FPDF(orientation='L')
        pdf.add_page()

        col_widths = [10, 70, 40, 25, 20, 75]  # Ancho de las columnas
        row_height = 8  # Altura de las filas
        page_width = pdf.w - 2 * pdf.l_margin

        pdf.image("static/img/log.png", x=10, y=10, w=30)  # Ajusta las coordenadas (x, y) y el tamaño (w) según tus necesidades

        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Biblioteca municipal "Fray Pedro de Laurecio"', align='C')
        pdf.ln(8)
        pdf.set_font('Times', 'B', 15.0)
        pdf.cell(page_width, 0.0, 'Ocosingo.Chis', align='C')

        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Registros de Afiliados', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 10)  # Cambio de fuente y negrita para los títulos de las columnas


        # Definir colores RGB para el diseño
        color_fondo = (244, 229, 192)  # Color arenoso para el fondo de las celdas
        color_texto = (0, 0, 0)  # Color para el texto

        pdf.set_fill_color(*color_fondo)  # Color de fondo de las celdas
        pdf.set_text_color(*color_texto)  # Color de texto

        # Agregar títulos a las columnas
        titles = ['Id', 'Nombre Completo', 'F.Nacimiento', 'Sexo', 'C.D', 'Observaciones']
        for title, width in zip(titles, col_widths):
            pdf.set_margin(30)
            pdf.cell(width, row_height, title, border=1, ln=False, align='C')
        pdf.ln(row_height)

        pdf.set_font('Arial', '', 10)  # Restaurar la fuente normal
        pdf.set_margin(10)
        alternating_color = False

        for row in result:
            # Cambiar el color de fondo para filas alternas
            if alternating_color:
                pdf.set_fill_color(*color_fondo)
            else:
                pdf.set_fill_color(255, 255, 255)  # Color blanco para filas alternas
            alternating_color = not alternating_color

            for i in range(len(row)):
                pdf.set_margin(30)
                pdf.cell(col_widths[i], row_height, str(row[i]), align="C", border=1, fill=True)
            pdf.ln(row_height)
            
        return pdf    
    
    def get_user_exist(self, user_id):
        sql_params = {}
        sql_query = f"""
        select af.user_id from afiliado af 
        WHERE af.user_id = {user_id}
        """
        registros = execute_query( sql_query, sql_params)
        if len(registros) == 0:
            return False
        return True
    
# retornar un solo registro
    def get_reg(self, id : int):
        obj = Afiliado.query.filter(Afiliado.id == id).first()
        return obj

    def save_file_frente(self, id, filename):
        obj = Afiliado.query.filter(Afiliado.id == id).first()
        if obj == None:
            return {"oper": None}
        obj.credencialfrente = filename
        # Hacer el update en la BD
        db.session.add(obj)
        db.session.commit()
        return {"oper": True}
    

    def save_file_reverso(self, id, filename):
        obj = Afiliado.query.filter(Afiliado.id == id).first()
        if obj == None:
            return {"oper": None}
        obj.credencialreverso = filename
        # Hacer el update en la BD
        db.session.add(obj)
        db.session.commit()
        return {"oper": True}
