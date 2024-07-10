from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField,HiddenField
from wtforms.validators import DataRequired, Length,Regexp, Optional #Email, EqualTo
from features.core.bd import db

class ClasificacionForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    nombre = StringField ("*Nombre de la clasificación", [DataRequired(), Length(max=100),
            Regexp(r'\S', message="El nombre de la clasificación no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")

class Clasificacion (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'recomdaciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    def get_data(self):
        return {'id':self.id, 
                'nombre': self.nombre, 
                }
