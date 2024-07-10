from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Optional #Email, EqualTo
from features.core.bd import db
from datetime import datetime, timedelta

# Función de validación personalizada
def validate_custom_field(form, field):
    today = datetime.today().date()

    if field.name == "fecha_prestamo":
        if field.data != today:
            raise ValidationError('La fecha de préstamo debe ser la fecha actual.')
    if field.name == "fecha_devolucion_real":
        if field.data != today:
            raise ValidationError('La fecha de devolución debe ser la fecha actual.')

    elif field.name == "fecha_devolucion_plan":
        if field.data != today + timedelta(days=7):
            raise ValidationError('La fecha de devolución plan debe ser 7 días después de la fecha de préstamo.')

class AcervoPrestamoForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    afiliado_id = SelectField("Usuario visitante", validators=[DataRequired()], validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    fecha_prestamo = DateField("*Fecha de préstamo.", [DataRequired(), validate_custom_field],
        description="Fecha de préstamo")
    fecha_devolucion_plan = DateField("*Fecha devolución plan", [DataRequired(), validate_custom_field],
        description="Fecha de devolución plan")
    fecha_devolucion_real = DateField("Fecha devolución real", validators=[Optional()],
        description="Fecha devolución real")
    usuario_presta_id = SelectField("Registró préstamo ", validators=[DataRequired()],
        validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    usuario_recibe_id = SelectField("Registró devolución ", validators=[Optional()],
        validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    acervo_ejemplar_id = SelectField("Acervo ejemplar", validators=[DataRequired()],
        validate_choice=False, description=('Seleccione una opcion'), render_kw={})


class AcervoPrestamoDevolverForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    fecha_devolucion_real = DateField("Fecha devolución real", validators=[DataRequired(), validate_custom_field],
        description="Fecha devolución real")
    usuario_recibe_id = SelectField("Registró devolución ", validators=[DataRequired()],
        choices=[("-1", "Elija una opción")],
        validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    
class AcervoPrestamoExtensionForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    fecha_devolucion_viejo = DateField("*Fecha devolución plan", [DataRequired(), validate_custom_field],
                                      description="Fecha de devolución plan")
    fecha_devolucion_nuevo = DateField("*Nueva fecha devolución plan", [DataRequired(), validate_custom_field],
                                        description="Nueva fecha de devolución plan")
    def validate_fecha_devolucion_nuevo(self, field):
        fecha_devolucion_viejo = self.fecha_devolucion_viejo.data
        fecha_devolucion_nuevo = field.data
        # Validar que la fecha de devolución nuevo sea 7 días después de la fecha de devolución viejo
        if fecha_devolucion_viejo + timedelta(days=7) != fecha_devolucion_nuevo:
            raise ValidationError('La nueva fecha de devolución debe ser 7 días después de la fecha de devolución plan original.')

class Acervoprestamo (db.Model):
        """Clase model que se mapea con la tabla de BD correspondiente"""
        id = Column(Integer, primary_key=True, autoincrement=True)
        afiliado_id = Column(Integer, index=True, nullable=False)
        fechaprestamo = Column(Date, nullable=False)
        fechadevolucion = Column(Date, nullable=False)
        fechadevolucionreal = Column(Date, nullable=True)
        usuariopresta_id = Column(Integer, index=True, nullable=False)
        usuariorecibe_id = Column(Integer, index=True, nullable=True)
        acervoejemplar_id = Column(Integer, index=True, nullable=True)
        status = Column(String(10), default=True)

        def get_data(self):
                return {'id':self.id, 
                        'afiliado_id': self.afiliado_id,
                        'fechaprestamo': self.fechaprestamo,
                        'fechadevolucion' : self.fechadevolucion,
                        'fechadevolucionreal': self.fechadevolucionreal,
                        'usuariopresta_id': self.usuariopresta_id,
                        'usuariorecibe_id': self.usuariorecibe_id,
                        'acervoejemplar_id': self.acervoejemplar_id,
                        'status': self.status
                        }

# class Acervotitulo(db.Model):
#         id = Column(Integer, primary_key=True, autoincrement=True)
#         titulo = Column(String(100), nullable=False)
#         autores =Column(String(150), nullable=False)
#         editorial_id = Column(Integer, index=True, nullable=False)
#         tipo_id = Column(Integer, index=True, nullable=False)
#         descripcion = Column(String(250), nullable=False)
#         foto = Column(String(250), nullable=False)


# class Estanteclasificacion(db.Model):
#         id = Column(Integer, primary_key=True, autoincrement=True)
#         estante = Column(String(20), nullable=False)
#         niveles = Column(String(20), nullable=False)
#         areafisica_id = Column(Integer, index=True, nullable=False)
#         clasificacion_id = Column(Integer, index=True, nullable=False)
#         responsable_id= Column(Integer, index=True, nullable=False)
        

# class Acervoejemplar(db.Model):
#         id = Column(Integer, primary_key=True, autoincrement=True)
#         estante_id = Column(Integer, index=True, nullable=False)
#         acervotitulo_id = Column(Integer, index=True, nullable=False)
#         numadquisicion = Column(String(50), nullable=False)
#         fecharegistro = Column(Date, nullable=False)
#         esdonado = Column(Boolean, default=False)
#         nivel = Column(String(10), nullable=False)
#         puedeprestarse = Column(Boolean, default=True)
        
class Notificaciones(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), index=True, nullable=False)
    mensaje = Column(String(250), nullable=False)