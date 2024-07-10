from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length,Regexp, Optional #Email, EqualTo
from features.core.bd import db

class PersonalForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    nombre = StringField(
        "*Nombre",
        [
            DataRequired(message="Este campo es obligatorio."),
            Length(max=50, message="El nombre no puede tener más de 50 caracteres."),
            Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos en el nombre."),
            Regexp(r'\S', message="El nombre no puede consistir solo en espacios en blanco."),
        ],
        description="Campo obligatorio",
    )
    
    apellidos = StringField(
        "*Apellidos",
        [
            DataRequired(message="Este campo es obligatorio."),
            Length(max=50, message="Los apellidos no pueden tener más de 50 caracteres."),
            Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos en los apellidos."),
            Regexp(r'\S', message="Los apellidos no pueden consistir solo en espacios en blanco."),

        ],
        description="Campo obligatorio",
    )
    
    correo = EmailField(
        "*Correo",
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(max=100, message="El correo no puede tener más de 100 caracteres."),
        ],
        description="Capture un correo válido. Ej: usuario@gmail.com",
    )
    
    phone = StringField(
        '*Telefono',
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(min=10, max=10, message="El teléfono debe tener 10 dígitos."),
            Regexp(r'^\d+$', message="Solo se permiten números en el teléfono."),
        ],
        description=('Teléfono inválido. Ej.: 9191234567'),
    )
    user_id = SelectField("Nombre de usuario",validators=[DataRequired()], choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})

class Personal (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
#     __tablename__ = 'recomendacion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    phone = Column(String(10), nullable=False, unique=True)
    user_id = Column(Integer, index=True, nullable=False)
    
    def get_data(self):
        return {'id':self.id, 
                'nombre': self.nombre, 
                'apellidos': self.apellidos,
                'correo': self.correo,
                'phone': self.phone,
                'user_id': self.user_id
                }
