from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length,Regexp, Optional #Email, EqualTo
from features.core.bd import db

class VisitantetipoForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    visitantetipo= StringField ("*Tipo de visitante", [DataRequired(), Length(max=100), Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos."),
            Regexp(r'\S', message="El tipo de visitante no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")

class Visitantetipo (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'visitantetipo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    visitantetipo = Column(String(100), nullable=False)


    def get_data(self):
        return {'id':self.id, 
                'visitantetipo': self.visitantetipo, 
                }
