from flask import request
from flask_jwt_extended import current_user
from fpdf import FPDF
from features.core.projectdefs import prepParam
from features.prestamo.models import AcervoPrestamoDevolverForm, AcervoPrestamoExtensionForm, Acervoprestamo, AcervoPrestamoForm, Notificaciones
from features.core.bd import db, execute_query


class PrestamoCU():
    def get_all(self, param_limit, search_value):
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        finicio = request.args.get("finicio")
        ffin = request.args.get("ffin")
        reporte = request.args.get("rep")
        
        condfinicio = ""
        if finicio:
            sqlParams["finicio"] = finicio
            condfinicio += " ap.fechaprestamo >= :finicio "
        condffin = ""
        if ffin:
            sqlParams["ffin"] = ffin
            condffin += " ap.fechaprestamo <= :ffin "
        if finicio and ffin:
            cond += " (" + condfinicio + " and " + condffin + ")  "
        elif finicio:
            cond += condfinicio
        elif ffin:
            cond += condffin
        if search_value:
            if cond:
                cond += " and "
            cond += prepParam(sqlParams, '( ', 'act.titulo', 'like', search_value, ' or ')
            cond += prepParam(sqlParams, ' ', 'af.username', 'like', search_value, ' ) ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f""" 
        Select count(1) 
        From acervoprestamo ap
        LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
        LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
        LEFT JOIN user af ON af.id = ap.afiliado_id
        {cond}
        """
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]
        # Obtener los registros a retornar
        sql_query = f"""
            SELECT ap.id prestamoid, af.id afiliadoid,  af.username, act.id acervoid
            , concat( act.titulo, ' #adq.:', ae.numadquisicion ) titulo
            , DATE_FORMAT(ap.fechaprestamo, '%Y/%m/%d'), DATE_FORMAT(ap.fechadevolucion, '%Y/%m/%d')
            , DATE_FORMAT(ap.fechadevolucionreal, '%Y/%m/%d'), up.id usuariopresta_id, up.username usuariopresta
            , us.id usuariorecibe_id, us.username usuariorecibe, ap.status 
            From acervoprestamo ap
            LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
            LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
            LEFT JOIN user af ON af.id = ap.afiliado_id
            LEFT JOIN user up ON up.id = ap.usuariopresta_id
            LEFT JOIN user us ON us.id  = ap.usuariorecibe_id
            {cond}
            order by ap.status desc, af.username asc, ap.fechaprestamo desc
            {param_limit}
            """
        try:
            registros = execute_query( sql_query, sqlParams)
            if reporte:
                if finicio == "" and ffin == "":
                    sql_query = f"""
                    SELECT ap.id prestamoid,  af.username,  act.titulo ,  DATE_FORMAT(ap.fechaprestamo, '%Y/%m/%d'), DATE_FORMAT(ap.fechadevolucion, '%Y/%m/%d'),
                    DATE_FORMAT(ap.fechadevolucionreal, '%Y/%m/%d'), up.username usuariopresta, us.username usuariorecibe,
                    ap.status from acervoprestamo ap
                    LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
                    LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
                    LEFT JOIN user af ON af.id = ap.afiliado_id
                    LEFT JOIN user up ON up.id = ap.usuariopresta_id
                    LEFT JOIN user us ON us.id  = ap.usuariorecibe_id
                    order by ap.fechaprestamo desc
                    """
                    registros = execute_query( sql_query, sqlParams)
                else:
                    sql_query = f"""
                    SELECT ap.id prestamoid,  af.username,  act.titulo ,  DATE_FORMAT(ap.fechaprestamo, '%Y/%m/%d'), DATE_FORMAT(ap.fechadevolucion, '%Y/%m/%d'),
                    DATE_FORMAT(ap.fechadevolucionreal, '%Y/%m/%d'), up.username usuariopresta, us.username usuariorecibe,
                    ap.status from acervoprestamo ap
                    LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
                    LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
                    LEFT JOIN user af ON af.id = ap.afiliado_id
                    LEFT JOIN user up ON up.id = ap.usuariopresta_id
                    LEFT JOIN user us ON us.id  = ap.usuariorecibe_id
                    {cond}
                    order by ap.fechaprestamo desc
                    """
                    registros = execute_query( sql_query, sqlParams)
                    
                return {'Prestamo':True , 'data':self.generar(registros)}
            # retornar el total y los registros
            return {'Prestamo':False , 'total':total, 'registros':registros}
        except Exception as e:
            print(e)
    
    def get_by_afiliado(self, param_limit, search_value):
        # prepara la condicion a filtrar
        # prepara la condicion a filtrar
        cond = ""
        sqlParams = {}
        if search_value:
            cond += prepParam(sqlParams, '( ', 'ap.afiliado_id', '=', current_user.id, ' and ')
            cond += prepParam(sqlParams, ' ', 'act.titulo', 'like', search_value, ' ) ')
        else:
            cond = f"afiliado_id={current_user.id}"
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        sql_query = f""" select count(1) From acervoprestamo ap
        LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
            LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
        LEFT JOIN user af ON af.id = ap.afiliado_id
        {cond}
        """
        registros = execute_query( sql_query, sqlParams)
        total=registros[0][0]
        # Obtener los registros a retornar
        sql_query = f"""
            SELECT ap.id prestamoid, act.id acervoid,  act.titulo ,  DATE_FORMAT(ap.fechaprestamo, '%Y/%m/%d'), DATE_FORMAT(ap.fechadevolucion, '%Y/%m/%d'),
            DATE_FORMAT(ap.fechadevolucionreal, '%Y/%m/%d'), ap.status from acervoprestamo ap
            LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
            LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
            LEFT JOIN user af ON af.id = ap.afiliado_id
            {cond} {param_limit}
            """
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return total, registros
    
    def save(self, data : AcervoPrestamoForm):
        # Verificar si el acervo ejemplar está actualmente prestado
        acervo_prestado = Acervoprestamo.query.filter_by(acervoejemplar_id=data.acervo_ejemplar_id.data, status='P').first()
        if acervo_prestado:
            return {"obj": None}
        # Resto del código para guardar el préstamo...
        obj = Acervoprestamo()
        obj_notificacion = Notificaciones()
        obj.afiliado_id = data.afiliado_id.data
        obj.fechaprestamo = data.fecha_prestamo.data
        obj.fechadevolucion = data.fecha_devolucion_plan.data
        obj.usuariopresta_id = current_user.id
        obj.acervoejemplar_id = data.acervo_ejemplar_id.data
        obj.status = "P"
        
        fecha_devolucion = data.fecha_devolucion_plan.data
        fecha_devolucion = str(fecha_devolucion)
        anio, mes, dia = map(str, fecha_devolucion.split('-'))
        fecha_devolucion = f"{dia}/{mes}/{anio}"
        titulo_acervo = self.get_titulo_acervo(data.acervo_ejemplar_id.data)
        afiliado_name = self.get_username(data.afiliado_id.data)
        obj_notificacion.username = afiliado_name
        obj_notificacion.mensaje = f"Debes devolver el acervo {titulo_acervo} en la fecha {fecha_devolucion}"
        
        db.session.add(obj)
        db.session.add(obj_notificacion)
        db.session.commit()

        return {"obj": obj.get_data()}
    
    def save_devolucion(self, data : AcervoPrestamoDevolverForm):
        # Verificar si el acervo ejemplar está actualmente prestado
        acervo_prestado = Acervoprestamo.query.filter_by(id=data.id.data).first()
        if not acervo_prestado:
            return {"obj": None}
        # Resto del código para guardar el préstamo...
        obj = acervo_prestado
        obj.fechadevolucionreal = data.fecha_devolucion_real.data
        obj.usuariorecibe_id = current_user.id
        obj.status = "D"
        db.session.add(obj)
        db.session.commit()

        return {"obj": obj.get_data()}
    
    def save_extension(self, data : AcervoPrestamoExtensionForm):
        # Verificar si el acervo ejemplar está actualmente prestado
        acervo_prestado = Acervoprestamo.query.filter_by(id=data.id.data).first()
        if not acervo_prestado:
            return {"obj": None}
        # Resto del código para guardar el préstamo...
        obj = acervo_prestado
        if obj.fechadevolucion != data.fecha_devolucion_viejo.data:
            return {"obj": None}
        obj.fechadevolucion = data.fecha_devolucion_nuevo.data
        db.session.add(obj)
        db.session.commit()
        return {"obj": obj.get_data()}

    # combo para los acervos 
    def get_combo(self, data : dict):
        cond = ""
        condId = ""
        sqlParams = {}
        if data.get('q'):
            cond += prepParam(sqlParams, '', 'act.titulo', 'like', data.get('q'), ' ')
        if data.get('id'):
            condId = prepParam(sqlParams, '', 'e.id', '=', data.get('id'), ' ')
        if cond and condId:
            cond = " where " + cond + ' and ' + condId
        elif cond or condId:
            cond = " where " + cond + condId

        # Para los combos, retornar el id y el texto a mostrar como item del select
        sql_query = f"""
            Select e.id, concat('#adq( ', e.numadquisicion, ' '
                , case when ap.status is null and e.estado = 'Disponible' then ''
					when ap.status is null and e.estado = 'Baja' then 'B' 
                    else ap.status
                    end
                , ') '
				, act.titulo
                , ', ', est.anaquel, 'N', e.nivel, ' ', c.nombre) text
                , case when ap.status = 'P' then 'PRESTADO' 
                  when e.estado = 'Baja' then 'BAJA' 
                end status
            From (
                Select act.id, act.titulo
                From acervotitulo act 
                {cond}
                limit 0, 50
            ) act 
            LEFT JOIN acervoejemplar e ON act.id = e.acervotitulo_id
            LEFT JOIN acervoprestamo ap ON e.id = ap.acervoejemplar_id and ap.status != 'D'
            LEFT JOIN estante est on e.estante_id = est.id
            LEFT JOIN clasificacion c on est.clasificacion_id = c.id
			where e.id is not null
            Order by ap.status 
            """
        # print (sql_query)
        registros = execute_query( sql_query, sqlParams)

        return registros
    
    def get_titulo_acervo(self,acervo_ejemplar_id ):
        sql_params = {}
        sql_query = f"""
        select act.titulo text from acervoejemplar ae 
        LEFT JOIN acervotitulo act ON act.id = ae.acervotitulo_id
        WHERE ae.id = {acervo_ejemplar_id}
        """
        registros = execute_query( sql_query, sql_params)

        return registros[0][0]
    
    def get_username(self, id_username):
        sql_params = {}
        sql_query = f"""
        select us.username text from user us 
        WHERE us.id = {id_username}
        """
        registros = execute_query( sql_query, sql_params)

        return registros[0][0]
    
    def get_prestamo_afiliado(self, username):
        cond = ""
        sqlParams = {}
        cond += prepParam(sqlParams, ' ', 'af.username', '=', username, ' ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        # Obtener los registros a retornar
        sql_query = f"""
            SELECT ap.id prestamoid,   DATE_FORMAT(ap.fechaprestamo, '%d/%m/%Y') fechaprestamo, 
            DATE_FORMAT(ap.fechadevolucion, '%d/%m/%Y') fechadevolucion, DATE_FORMAT(ap.fechadevolucionreal, '%d/%m/%Y') fechadevreal, 
            ap.status, act.titulo  from acervoprestamo ap
            LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
            LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
            LEFT JOIN user af ON af.id  = ap.afiliado_id
            {cond} order by ap.id DESC
            """
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return  registros
    
    def get_cantidad_prestamos_pendientes_afiliado(self, username):
        cond = ""
        sqlParams = {}
        cond += prepParam(sqlParams, '( ', 'af.username', '=', username, ' and ')
        cond += prepParam(sqlParams, ' ', 'ap.status', '=', 'P', ' ) ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        # Obtener los registros a retornar
        sql_query = f""" select count(1) From acervoprestamo ap
        LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
        LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
        LEFT JOIN user af ON af.id = ap.afiliado_id
        {cond}
        """
        total = 0
        registros = execute_query( sql_query, sqlParams)
        if registros:
            total=registros[0][0]
        # retornar el total y los registros
        return  total
    
    def get_prestamos_admim(self):
        sqlParams = {}
        # Obtener los registros a retornar
        sql_query = f"""
            SELECT ap.id prestamoid, af.username afiliado, act.titulo,  DATE_FORMAT(ap.fechaprestamo, '%d/%m/%Y') fechaprestamo, 
            DATE_FORMAT(ap.fechadevolucion, '%d/%m/%Y') fechadevolucion, DATE_FORMAT(ap.fechadevolucionreal, '%d/%m/%Y') fechadevreal, 
            ap.status,  us.username user_presta, usd.username user_recibe from acervoprestamo ap
            LEFT JOIN acervoejemplar ae ON ap.acervoejemplar_id = ae.id
            LEFT JOIN acervotitulo act ON ae.acervotitulo_id  = act.id
            LEFT JOIN user af ON af.id  = ap.afiliado_id 
            LEFT JOIN user us ON us.id  = ap.usuariopresta_id  
            LEFT JOIN user usd ON usd.id  = ap.usuariorecibe_id 
            WHERE  us.tipo  = 2 
            order by ap.id DESC
            """
        registros = execute_query( sql_query, sqlParams)
        # retornar el total y los registros
        return  registros
    
    def get_notificaciones(self, username):
        cond = ""
        sqlParams = {}
        cond += prepParam(sqlParams, ' ', 'nt.username', '=', username, ' ')
        if cond:
            cond= f"WHERE {cond}"
        # Obtener el total de registros a retornar
        # Obtener los registros a retornar
        sql_query = f"""
            select id, mensaje from notificaciones nt {cond}
            """
        registros = execute_query( sql_query, sqlParams)
        if registros:
            self.delete_notificacion_afiliado(username)
        # retornar el total y los registros
        return  registros
    
    def delete_notificacion_afiliado(self, username):
        objList = Notificaciones.query.filter(Notificaciones.username== username).all()
        if len(objList) > 0:
            for notificacion in objList:
                db.session.delete(notificacion)
                db.session.commit()
        # No necesitas retornar nada si solo estás eliminando registros


    def generar(self, data):

        pdf = FPDF(orientation='L')
        pdf.add_page()

        col_widths = [10, 30, 60, 30, 30, 30, 20, 20, 17]  # Ancho de las columnas
        row_height = 8  # Altura de las filas
        page_width = pdf.w - 2 * pdf.l_margin
        
        pdf.image("static/img/log.png", x=10, y=10, w=30)  # Ajusta las coordenadas (x, y) y el tamaño (w) según tus necesidades


        # Definir colores RGB para el diseño
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
        pdf.cell(page_width, 0.0, 'Registros de prestamo', align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 9)

        # Agregar títulos a las columnas
        titles = ['Id', 'Afiliado', 'Acervo', 'F.Préstamo', 'F.Límite', 'F.Devolución', 'U.Prestó', 'U.Recibió', 'Estado']
        for title, width in zip(titles, col_widths):
            pdf.set_margin(30)
            pdf.cell(width, row_height, title, border=3, align='C')
        pdf.ln(row_height)

        pdf.set_font('Arial', '', 10)  # Restaurar la fuente normal y reducir tamaño
        # Alternar colores de fondo de las filas
        alternating_color = False

        # Agregar datos de la tabla
        for row in data:
            if alternating_color:   # Cambiar el color de fondo para filas alternas
                pdf.set_fill_color(*color_fondo)
            else:
                pdf.set_fill_color(255, 255, 255)  
            alternating_color = not alternating_color # Color blanco para filas alternas
            for item, width in zip(row, col_widths):
                pdf.cell(width, row_height, str(item), align="C", border=1, fill=True)
            pdf.ln(row_height)
        return pdf