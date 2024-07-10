from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, ValidationError
from wtforms.fields import  HiddenField, DateField, IntegerField
from wtforms.validators import DataRequired
from features.core.bd import db
from datetime import datetime, timedelta

def validate_custom_field(form, field):
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    
    if field.data != today and field.data != yesterday:
        raise ValidationError('La fecha debe ser de hoy o de ayer.')
    
class VisitaFileForm(FlaskForm):
    id = HiddenField("Id", [DataRequired()], description="")
    file = FileField("*Frente")


class RegistroVisitaForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    fechavisita = DateField ("Fecha de visita", validators=[DataRequired(), validate_custom_field], description="Fecha de registro")
    bibliusuario_id = SelectField("Visitante",
                                   validators=[DataRequired()],
                                   choices=[( "Elija una opción")],
                                   validate_choice=False,
                                   description="Seleccione una opción",
                                   render_kw={})
    escuela_id = SelectField("Escuela",
                             validators=[DataRequired()],
                             choices=[( "Elija una opción")],
                             validate_choice=False,
                             description="Seleccione una opción",
                             render_kw={})
    visitantetipo_id = SelectField("Tipo de visitante",
                                    validators=[DataRequired()],
                                    choices=[( "Elija una opción")],
                                    validate_choice=False,
                                    description="Seleccione una opción",
                                    render_kw={})

class RegistroVisita(db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
    # __tablename__ = 'registro_visitas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fechavisita = Column(Date, nullable=False)
    bibliusuario_id = Column(Integer, nullable=False)
    escuela_id = Column(Integer, nullable=False)  
    visitantetipo_id = Column(Integer, nullable=False)  

    def get_data(self):
        return {'id': self.id, 'fechavisita': self.fechavisita, 
                'bibliusuario_id': self.bibliusuario_id, 
                'escuela_id': self.escuela_id, 'visitantetipo_id': self.visitantetipo_id}
