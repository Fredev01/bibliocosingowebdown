from flask_jwt_extended import current_user
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.estado.models import Estado, EstadoForm
from features.core.bd import db, execute_query


class EstadoCU():
    def get_all(self, param_limit, search_value):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, ' ', 'estado', 'like', search_value, ' ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f"select count(1) From estado {cond}"
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]

        # Obtener los registros a retornar
        sql_query = f"""
            select t.id, t.nombre
            from estado t
            
            {cond} {param_limit}
            """
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return total, registros

        
    def save(self, data : EstadoForm):
        if (data.id.data == None or data.id.data == ''  ) :
            objList = Estado.query.filter(Estado.nombre==data.nombre.data).first() or []
            if objList:
                return {"obj": None}
        else:
            objValid = Estado.query.filter(Estado.nombre==data.nombre.data).first() or None
            if objValid :
                if objValid.id != int(data.id.data):
                    return {"obj": None}
            objList = Estado.query.filter(Estado.id == data.id.data).all()
        obj : Estado = objList[0] if len(objList)>0 else None
        if obj == None:
            obj = Estado()
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
        obj = Estado.query.filter(Estado.id == id).first()
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
            select t.id, t.nombre
            from estado t
            {cond} 
        """
        result = execute_query(sql_query, sqlParams)

        pdf = FPDF()
        pdf.add_page()

        col_widths = [10, 80]  # Ancho de las columnas
        row_height = 10  # Altura de las filas
        page_width = pdf.w - 2 * pdf.l_margin

        pdf.image("static/img/log.png", x=10, y=10, w=30)  # Ajusta las coordenadas (x, y) y el tamaño (w) según tus necesidades

        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Biblioteca municipal "Fray Pedro de Laurecio"', align='C')
        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Registros de Estados', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 12)  # Cambio de fuente y negrita para los títulos de las columnas

        # Agregar títulos a las columnas
        titles = ['ID', 'Estado']
        for title, width in zip(titles, col_widths):
            pdf.set_margin(35)
            pdf.cell(width, row_height, title, border=3, align='C')
        pdf.ln(row_height)

        pdf.set_font('Helvetica', '', 12)  # Restaurar la fuente normal
        
        # Agregar datos de la tabla
        for row in result:
            pdf.set_margin(35)
            for i, item in enumerate(row):
                pdf.cell(col_widths[i], row_height, str(item), align="C", border=1)
            pdf.ln(row_height)
            
        # Guardar el PDF en un archivo temporal
        # temp_file = "reporte_escuelas.pdf"
        # pdf.output(temp_file)


        return pdf
    
