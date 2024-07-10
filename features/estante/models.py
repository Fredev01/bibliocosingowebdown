from sqlalchemy import Column, ForeignKey, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from features.core.bd import db


class EstanteForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    anaquel = StringField("*Nombre del estante", [DataRequired(), Length(max=100),Regexp(r'\S', message="El nombre del estante no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")
    niveles = StringField("*# niveles", [DataRequired(), Length(max=2),Regexp(r'^[1-9]|10*$', message="Solo se permiten números mayores a 0 y menores a 13"),], description="Campo obligatorio")
    areafisica_id = SelectField("Area física",validators=[DataRequired()], choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    clasificacion_id = SelectField("Clasificación del libro",validators=[DataRequired()], choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    responsable_id = SelectField("Responsable del área",validators=[DataRequired()], choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})



class Estante(db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
    __tablename__ = 'estante'
    id = Column(Integer, primary_key=True, autoincrement=True)
    anaquel = Column(String(100), nullable=False)
    niveles = Column(String(2), nullable=False)
    areafisica_id   = Column(Integer, index= True,  nullable=False)
    clasificacion_id = Column(Integer, index= True,  nullable=False)
    responsable_id = Column(Integer, index= True,  nullable=False)


    def get_data(self):
        return {'id': self.id, 
                'anaquel': self.anaquel, 
                'niveles': self.niveles,
                'areafisica_id': self.areafisica_id,
                'clasificacion_id': self.clasificacion_id,
                'responsable_id': self.responsable_id
               }
