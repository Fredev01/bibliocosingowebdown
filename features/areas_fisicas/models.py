from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length,Regexp, Optional #Email, EqualTo
from features.core.bd import db

class AreaFisicaForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    areaFisica = StringField ("*Nombre del área", [DataRequired(), Length(max=100), Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos."),
            Regexp(r'\S', message="El nombre del área no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")
#     sexo = SelectField("Sexo",validators=[DataRequired()],
#             choices=[("H", "Hombre"), ("M", "Mujer"), ("X", "indefinido")],
#             description="Hombre o Mujer o indefinido",
#             render_kw={})
#     correo = EmailField ("*Correo", validators=[], description="Capture un correo válido. Ej: usuario@gmail.com")
#     phone = StringField('*Telefono', validators=[DataRequired()], description=('Teléfono inválido. Ej.: 9191234567'))
#     peso_actual = DecimalField ("Peso Actual", default=0, description="Ej.: 63.5")
#     peso_meta = DecimalField ("Peso Meta", default=0, description="Ej.: 54.0")

class AreaFisica (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'areaFisica'
    id = Column(Integer, primary_key=True, autoincrement=True)
    areaFisica = Column(String(100), nullable=False)

    def get_data(self):
        return {'id':self.id, 
                'areaFisica': self.areaFisica,
                }
