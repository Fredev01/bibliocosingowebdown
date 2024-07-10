from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Regexp, Optional #Email, EqualTo
from features.core.bd import db

class EditorialForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    editorial = StringField ("*Nombre de la editorial", [DataRequired(), Length(max=100), Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos."),
            Regexp(r'\S', message="El nombre de la editorial no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")

class Editorial (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'recomendacion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    editorial = Column(String(100), nullable=False)

    def get_data(self):
        return {'id':self.id, 
                'editorial': self.editorial, 
                }
