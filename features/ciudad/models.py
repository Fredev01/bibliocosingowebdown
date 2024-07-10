from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from features.core.bd import db

class CiudadForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    nombre = StringField ("*Nombre del ciudad", [DataRequired(), Length(max=100) , Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos."),], description="Campo obligatorio")


class Ciudad (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'ciudad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)


    def get_data(self):
        return {'id':self.id, 
                'nombre': self.nombre, 
                
                }
