from flask_jwt_extended import current_user
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.acervotitulo.models import Acervotitulo, AcervotituloForm
from features.core.bd import db, execute_query


class AcervotituloCU():
    def get_all(self, param_limit, search_value):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, '( ', 't.titulo', 'like', search_value, ' or ')
            cond += prepParam(sqlParams, ' ', 't.autores', 'like', search_value, ' ) ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f"select count(1) From acervotitulo t {cond}"
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]

        # Obtener los registros a retornar
        sql_query = f"""
            select t.id, t.titulo, t.autores, t.editorial_id, ed.editorial, t.tipo_id, ti.nombre, t.descripcion, t.foto
                    , GROUP_CONCAT(DISTINCT concat(est.anaquel, 'N', t.nivel, ' ', c.nombre)  SEPARATOR ', ')  estante
                    , max(t.totalprestados) as totalprestados, t.totalejemplares
            From (
                select t.id, t.titulo, t.autores, t.editorial_id, t.tipo_id, t.descripcion, t.foto, e.nivel, e.estante_id
                    , t.totalejemplares, count(ap.id) totalprestados
                from (
                    SELECT t.id, t.titulo, t.autores, t.editorial_id, t.tipo_id, t.descripcion, t.foto
                        , COUNT(e.id) AS totalejemplares
                    FROM (
                        SELECT t.id, t.titulo, t.autores, t.editorial_id, t.tipo_id, t.descripcion, t.foto
                        FROM acervotitulo t
                        {cond} {param_limit}
                        # LIMIT 0,10
                    ) t
                    LEFT JOIN acervoejemplar e ON t.id = e.acervotitulo_id
                    GROUP BY t.id, t.titulo, t.autores, t.editorial_id, t.tipo_id, t.descripcion, t.foto
                ) t
                LEFT JOIN acervoejemplar e on t.id = e.acervotitulo_id
                LEFT JOIN acervoprestamo ap on ap.acervoejemplar_id = e.id and ap.status = 'P'
                group by t.id, t.titulo, t.autores, t.editorial_id, t.tipo_id, t.descripcion, t.foto, e.nivel, e.estante_id
                    , t.totalejemplares
            ) t
            LEFT JOIN editorial AS ed ON t.editorial_id = ed.id
            LEFT JOIN tipo AS ti ON t.tipo_id = ti.id 
            LEFT JOIN estante est on t.estante_id = est.id
            LEFT JOIN clasificacion c on est.clasificacion_id = c.id
            GROUP BY t.id, t.titulo, t.autores, t.editorial_id, ed.editorial, t.tipo_id, ti.nombre, t.descripcion, t.foto, t.totalejemplares;
            """
        # print(sql_query)
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return total, registros

        
    def save(self, data : AcervotituloForm):
        if (data.id.data == None or data.id.data == ''  ) :
            objList = Acervotitulo.query.filter(Acervotitulo.titulo==data.titulo.data).first() or []
            if (objList):
                # Retornar None para indicar que ya se encuentra 
                # registrado el título actual...
                return None
        else:
            objList = Acervotitulo.query.filter(Acervotitulo.id == data.id.data).all()
        obj : Acervotitulo = objList[0] if len(objList)>0 else None
        if obj == None:
            obj = Acervotitulo()
        obj.titulo= data.titulo.data, 
        obj.autores = data.autores.data,
        obj.editorial_id = data.editorial_id.data,
        obj.tipo_id = data.tipo_id.data,
        obj.descripcion = data.descripcion.data,
        # la foto se guardará de forma independiente al subir el archivo
        # obj.foto = data.foto.data,
        
        # Obtener el registro directamente del id del usuario actualmente autentificado
        # ignorando el recibido del cliente
        # obj.registro_id= data.registro_id.data
        #obj.registro_id= current_user.id
        # Hacer el insert en la BD
        try:
            db.session.add(obj)
            db.session.commit()
            return { "obj": obj.get_data() }
        except:
            return None

 
    def delete(self, id : int):
        obj = Acervotitulo.query.filter(Acervotitulo.id == id).first()
        if obj == None:
            return {"oper": None}
        else:
            # Hacer el delete del obj en la BD
            db.session.delete(obj)
            db.session.commit()
            return { "oper": True }
 
    # retornar un solo registro
    def get_reg(self, id : int):
        obj = Acervotitulo.query.filter(Acervotitulo.id == id).first()
        return obj

    def save_file(self, id, filename):
        obj = Acervotitulo.query.filter(Acervotitulo.id == id).first()
        if obj == None:
            return {"oper": None}
        obj.foto = filename
        # Hacer el update en la BD
        db.session.add(obj)
        db.session.commit()
        return {"oper": True}

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
                sql_query = "select id, titulo text from acervotitulo e " + cond
                registros = execute_query( sql_query, sqlParams)

                return registros
            
            
    def generar(self):
        # Preparar los parámetros de la consulta
        sqlParams = {}

        # Obtener los registros a retornar
        sql_query = f"""
            SELECT t.id, t.titulo, t.autores, ed.editorial, ti.nombre, t.descripcion
            FROM acervotitulo t
            LEFT JOIN editorial AS ed ON t.editorial_id = ed.id
            LEFT JOIN tipo AS ti ON t.tipo_id = ti.id 
        """
        result = execute_query(sql_query, sqlParams)

        # Crear objeto PDF con orientación horizontal
        pdf = FPDF(orientation='L')
        pdf.add_page()

        col_widths = [10, 50, 50, 40, 40, 55]  # Ancho de las columnas
        row_height = 8  # Altura de las filas
        page_width = pdf.w - 2 * pdf.l_margin

        # Definir colores RGB para el diseño
        color_titulo = (0, 0, 0)  # Color para los títulos
        color_fondo = (244, 229, 192)  # Color arenoso para el fondo de las celdas
        color_texto = (0, 0, 0)  # Color para el texto

        pdf.set_fill_color(*color_fondo)  # Color de fondo de las celdas
        pdf.set_text_color(*color_texto)  # Color de texto

        pdf.image("static/img/log.png", x=10, y=10, w=30)  # Ajusta las coordenadas (x, y) y el tamaño (w) según tus necesidades

        pdf.ln(17)
        pdf.set_font('Times', 'B', 15.0)
        pdf.set_text_color(*color_titulo)  # Aplicar color a los títulos
        pdf.cell(page_width, 0.0, 'Biblioteca municipal "Fray Pedro de Laurecio"', align='C')
        pdf.ln(8)
        pdf.set_font('Times', 'B', 15.0)
        pdf.cell(page_width, 0.0, 'Ocosingo.Chis', align='C')

        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Registros de Acervos', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 9)
                # Agregar títulos a las columnas
        titles = ['ID', 'Título', 'Autores', 'Editorial', 'Tipo', 'Descripción']
        for title, width in zip(titles, col_widths):
            pdf.set_margin(25)
            pdf.cell(width, row_height, title, border=1, ln=False, align='C')
        pdf.ln(row_height)

        pdf.set_font('Arial', '', 9)

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