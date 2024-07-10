from flask_jwt_extended import current_user
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.acervoejemplar.models import Acervoejemplar, AcervoejemplarForm
from features.estante.models import Estante
from features.core.bd import db, execute_query


class AcervoejemplarCU():
    def get_all(self, param_limit, search_value, acervotitulo_id):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        cond = "t.acervotitulo_id = :acervotitulo_id  "
        sqlParams ['acervotitulo_id'] = acervotitulo_id
        """ if search_value:
            cond += prepParam(sqlParams, ' and ', 'estante_id', 'like', search_value, ' ') """
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f"select count(1) From acervoejemplar t {cond}"
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]
        print(sql_query)

        # Obtener los registros a retornar
        sql_query = f"""
            select t.id, t.estante_id, an.anaquel, t.acervotitulo_id , act.titulo,  t.numadquisicion, t.fecharegistro, t.nivel, t.estado, t.esdonado,  t.puedeprestarse, t.asignacion_topografica
            from (
				Select t.id, t.estante_id, t.acervotitulo_id, t.numadquisicion, t.fecharegistro, t.nivel, t.estado, t.esdonado,  t.puedeprestarse, t.asignacion_topografica
				From acervoejemplar t  
				#{cond} {param_limit}
            ) t  
            LEFT JOIN estante AS an ON t.estante_id = an.id
            LEFT JOIN acervotitulo AS act ON t.acervotitulo_id = act.id
            order by t.fecharegistro desc
            """
        print(sql_query)
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return total, registros

        
    def save(self, data : AcervoejemplarForm):
        objListEstante = Estante.query.filter(Estante.id == data.estante_id.data).all()
        # obtener el numadquisición a agregar o editar del navegador web
        obj = Acervoejemplar.query.filter_by(numadquisicion=data.numadquisicion.data).first()
        if (data.id.data == None or data.id.data == ''  ) :
            # si se desea insertar un nuevo registro...
            # entonces no debería existir ningun obj con el num adqu. dado
            if (obj):
                # Retornar None para indicar que ya se encuentra 
                # registrado el num adq. dado...
                return None
        else:
            # si se desea editar un registro...
            # buscar el obj con el id dado en la BD
            objEnBD = Acervoejemplar.query.filter_by(id=data.id.data).first()
            # si el num num adq. encontrado en la BD = dado
            if (obj and objEnBD.id != obj.id):
                # el numadq. ya se encuentra en uso por otro ejemplar
                return None

        objEstante = objListEstante[0] if len(objListEstante) > 0 else None
        if objEstante != None:
            if int(data.nivel.data) > int(objEstante.niveles):
                return {"obj": None}

        if obj == None:
            obj = Acervoejemplar()
        obj.estante_id = data.estante_id.data
        obj.acervotitulo_id = data.acervotitulo_id.data
        obj.numadquisicion = data.numadquisicion.data
        obj.fecharegistro = data.fecharegistro.data
        obj.esdonado = data.esdonado.data
        obj.nivel = data.nivel.data
        obj.estado = data.estado.data
        obj.puedeprestarse = data.puedeprestarse.data
        obj.asignacion_topografica = data.asignacion_topografica.data,
        db.session.add(obj)
        db.session.commit()
        return {"obj": obj.get_data()}

 
    def delete(self, id : int):
        obj = Acervoejemplar.query.filter(Acervoejemplar.id == id).first()
        if obj == None:
            return {"oper": None}
        else:
            # Hacer el delete del obj en la BD
            db.session.delete(obj)
            db.session.commit()
            return { "oper": True }

    def get_combo(self, data : dict):
            cond = ""
            condId = ""
            sqlParams = {}
            if data.get('q'):
                cond += prepParam(sqlParams, '', 'e.estante_id', 'like', data.get('q'), ' ')
            if data.get('id'):
                condId = prepParam(sqlParams, '', 'e.id', '=', data.get('id'), ' ')
            if cond and condId:
                cond = " where " + cond + ' and ' + condId
            elif cond or condId:
                cond = " where " + cond + condId

            # Para los combos, retornar el id y el texto a mostrar como item del select
            sql_query = "select id, estante_id text from acervoejemplar e " + cond
            registros = execute_query( sql_query, sqlParams)
            return registros

    def get_ejemplaresde(self, acervo_id : int):
        # Obtener el total de registros a retornar
        sqlParams = {}
        sql_query = f"""
            SELECT count(1)
            FROM acervoejemplar t 
            Where t.acervotitulo_id = {acervo_id}
            """
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]

        sql_query = f"""
            Select e.id, e.estante, e.numadquisicion, e.asignacion_topografica, e.titulo, e.puedeprestarse
            , e.fechaprestamo, p.fechadevolucion
            , case when puedeprestarse = 1 and coalesce(p.status, '') != 'P' 
				and e.estado != 'Baja' then 'Disponible' 
				when e.estado = 'Baja' then 'Baja' 
                else '' 
                end status
            From ( 
                Select e.id, concat( s.anaquel, 'N', e.nivel) estante, e.numadquisicion, e.asignacion_topografica, t.titulo, e.puedeprestarse, e.estado
                    , max(p.fechaprestamo) fechaprestamo
                From (
                    SELECT e.id, e.nivel, e.numadquisicion, e.asignacion_topografica, e.puedeprestarse, e.acervotitulo_id, e.estante_id, e.estado
                    FROM acervoejemplar e 
                    Where e.acervotitulo_id = {acervo_id}
                ) e
                left join acervotitulo t on e.acervotitulo_id = t.id
                left join estante s on e.estante_id = s.id
                left join acervoprestamo p on p.acervoejemplar_id = e.id
                group by e.id
            ) e
            left join acervoprestamo p on p.acervoejemplar_id = e.id and p.fechaprestamo = e.fechaprestamo
	        order by status desc
        """
        registros = execute_query( sql_query)
        return total, registros


    def generar(self):
        # Preparar los parámetros de la consulta
        sqlParams = {}
        
        # Obtener los registros a retornar
        sql_query = """
        SELECT t.id, an.anaquel, act.titulo, t.numadquisicion, t.fecharegistro, t.nivel, 
            CASE WHEN t.esdonado = 1 THEN 'si' ELSE 'no' END AS es_donado, 
            CASE WHEN t.puedeprestarse = 1 THEN 'si' ELSE 'no' END AS puede_prestarse 
        FROM acervoejemplar t  
        LEFT JOIN estante AS an ON t.estante_id = an.id
        LEFT JOIN acervotitulo AS act ON t.acervotitulo_id = act.id
        """
        result = execute_query(sql_query, sqlParams)

        pdf = FPDF(orientation='L')  # Orientación de la hoja horizontal
        pdf.add_page()

        col_widths = [10, 25, 70, 30, 25, 20, 20, 30]  # Ancho de las columnas
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
        pdf.set_font('Times', 'B', 14.0)
        pdf.set_text_color(*color_titulo)  # Aplicar color a los títulos
        pdf.cell(page_width, 0.0, 'Biblioteca municipal "Fray Pedro de Laurecio"', align='C')
        pdf.ln(8)
        pdf.set_font('Times', 'B', 15.0)
        pdf.cell(page_width, 0.0, 'Ocosingo.Chis', align='C')

        pdf.ln(10)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Registros de Acervos Bibliograficos', align='C')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 10)  # Cambio de fuente y negrita para los títulos de las columnas

        # Agregar títulos a las columnas
        titles = ['Id', 'Anaquel', 'Título', 'N.Adquisición', 'F.Registro', 'Nivel', 'Es Donado', 'Puede Prestarse']
        for title, width in zip(titles, col_widths):
            pdf.set_margin(30)
            pdf.cell(width, row_height, title, border=1, ln=False, align='C')
        pdf.ln(row_height)

        pdf.set_font('Arial', '', 9)  # Restaurar la fuente normal y reducir tamaño

        # Inicializar la variable para alternar colores de fondo
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
