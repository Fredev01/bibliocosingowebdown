from flask_jwt_extended import current_user
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.escuelanivel.models import Escuelanivel, EscuelanivelForm
from features.core.bd import db, execute_query


class EscuelanivelCU():
    def get_all(self, param_limit, search_value):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, ' ', 'nombre', 'like', search_value, ' ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f"select count(1) From escuelanivel {cond}"
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]

        # Obtener los registros a retornar
        sql_query = f"""
            select e.id, e.nombre from escuelanivel e    
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
            cond += prepParam(sqlParams, '', 'e.nombre', 'like', data.get('q'), ' ')
        if data.get('id'):
            condId = prepParam(sqlParams, '', 'e.id', '=', data.get('id'), ' ')
        if cond and condId:
            cond = " where " + cond + ' and ' + condId
        elif cond or condId:
            cond = " where " + cond + condId

        # Para los combos, retornar el id y el texto a mostrar como item del select
        sql_query = "select id, nombre text from escuelanivel e " + cond
        registros = execute_query( sql_query, sqlParams)

        return registros
        
    def save(self, data : EscuelanivelForm):
        if data.id.data == '' or data.id.data == None:
            objList = Escuelanivel.query.filter(Escuelanivel.nombre==data.nombre.data).first() or []
            if objList:
                return {"obj": None}
        else:
            objValid = Escuelanivel.query.filter(Escuelanivel.nombre==data.nombre.data).first() or None
            if objValid :
                if objValid.id != int(data.id.data):
                    return {"obj": None}
            objList = Escuelanivel.query.filter(Escuelanivel.id == data.id.data).all()
        obj : Escuelanivel = objList[0] if len(objList)>0 else None
        if obj == None:
            obj = Escuelanivel()
        obj.nombre= data.nombre.data
    
        # Hacer el insert en la BD
        db.session.add(obj)
        db.session.commit()
        return { "obj": obj.get_data() }
 
    def delete(self, id : int):
        obj = Escuelanivel.query.filter(Escuelanivel.id == id).first()
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
            select e.id, e.nombre from escuelanivel e
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
        pdf.cell(page_width, 0.0, 'Registros de Escuelas', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 10)  # Cambio de fuente y negrita para los títulos de las columnas

        # Agregar títulos a las columnas
        titles = ['ID', 'Nivel']
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
    