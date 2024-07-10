from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length,Regexp, Optional #Email, EqualTo
from features.core.bd import db

class EscuelaForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    nombre = StringField ("*Nombre de la escuela", [DataRequired(), Length(max=100), Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos."),
            Regexp(r'\S', message="El nombre de la escuela no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")
    nivel_id = SelectField("Nivel de la escuela",validators=[DataRequired()], choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})

class Escuela (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    nivel_id = Column(Integer, index=True, nullable=False)

    def get_data(self):
        return {'id':self.id, 
                'nombre': self.nombre,
                'nivel_id': self.nivel_id
                }
