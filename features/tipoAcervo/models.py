from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length,Regexp, Optional
from features.core.bd import db

class TipoForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    nombre = StringField ("*Nombre del tipo", [DataRequired(), Length(max=100), Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos."),
            Regexp(r'\S', message="El nombre del tipo no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")


class Tipo (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'tipo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)


    def get_data(self):
        return {'id':self.id, 
                'nombre': self.nombre, 
                
                }
