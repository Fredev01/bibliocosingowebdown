from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from features.core.bd import db

class NotificacionForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    idUser = SelectField("Clasificación del libro",validators=[DataRequired()], choices=[("-1","Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    mensaje = StringField ("*Nombre del estado", [DataRequired(), Length(max=100), Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos."),], description="Campo obligatorio")


class Notificacion (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'estado'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idUser = Column(Integer, index= True,  nullable=False)
    mensaje = Column(String(100), nullable=False)


    def get_data(self):
        return {'id':self.id, 
                'idUser':self.idUser,
                'mensaje': self.mensaje, 
                
                }
