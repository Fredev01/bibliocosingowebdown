from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Optional #Email, EqualTo
from features.core.bd import db

class RecomendacionForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    recomendacion = StringField ("*Nombre de la recomendación", [DataRequired(), Length(max=100)], description="Campo obligatorio")
    fechaderegistro = DateField ("*Fecha de reg.", [DataRequired()], description="Fecha de registro")
    fechainicio = DateField ("*Mostrar desde", [DataRequired()], description="Fecha de inicio para publicar las recomendaciones asociadas a este registro")
    fechafin = DateField ("Mostrar hasta", validators=[Optional()], description="Fecha para terminar de publicar el listado de las recomendaciones asociadas a este periodo")
    descripcion = StringField ("Descripción", description="Long.Max.:200")
    registro_id = SelectField("Registró",validators=[DataRequired()], choices=[("-1","Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
#     sexo = SelectField("Sexo",validators=[DataRequired()],
#             choices=[("H", "Hombre"), ("M", "Mujer"), ("X", "indefinido")],
#             description="Hombre o Mujer o indefinido",
#             render_kw={})
#     correo = EmailField ("*Correo", validators=[], description="Capture un correo válido. Ej: usuario@gmail.com")
#     phone = StringField('*Telefono', validators=[DataRequired()], description=('Teléfono inválido. Ej.: 9191234567'))
#     peso_actual = DecimalField ("Peso Actual", default=0, description="Ej.: 63.5")
#     peso_meta = DecimalField ("Peso Meta", default=0, description="Ej.: 54.0")

class Recomendacion (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'recomendacion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    recomendacion = Column(String(100), nullable=False)
    fechaderegistro = Column(Date, nullable=False)
    fechainicio = Column(Date, nullable=False)
    fechafin = Column(Date, nullable=True)
    descripcion = Column(String(250), nullable=False)
    registro_id = Column(Integer, index=True, nullable=False)

    def get_data(self):
        return {'id':self.id, 
                'recomendacion': self.recomendacion, 
                'fechaderegistro': self.fechaderegistro,
                'fechainicio': self.fechainicio,
                'fechafin': self.fechafin,
                'descripcion': self.descripcion,
                'registro_id': self.registro_id 
                }
