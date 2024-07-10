from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms import IntegerField, ValidationError
from wtforms.fields import StringField, PasswordField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, Regexp
from features.core.bd import db
from sqlalchemy import Column, Integer, String, Boolean

from features.core.encrypt import Hash

def validate_passwd_field(form, field):
    if len(field.data) == 0 and len(form.id.data) == 0:
        raise ValidationError('La contraseña es obligatoria para nuevos registros')
    elif form.passwd.data != form.confirm.data:
        raise ValidationError('La contraseñas deben coincidir')

class UserForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    username = StringField("*Nombre de usuario", [DataRequired(), Length(max=45)], description="Campo obligatorio")
    email = StringField("*Correo electrónico", [DataRequired(), Email(message='email inválido'), Length(max=100)], description="Campo obligatorio, especifique un correo válido")
    full_name = StringField ("*Nombre completo", [DataRequired(), Length(max=120),
            Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ.\s]+$', message="Solo se permiten letras y acentos en el nombre."),
            Regexp(r'\S', message="El nombre no puede consistir solo en espacios en blanco."),], description="Requerido, Long.Max.:120")
    passwd = PasswordField("Contraseña", [ Length(max=45), validate_passwd_field], description="Campo obligatorio")
    confirm  = PasswordField('Repetir Contraseña', [validate_passwd_field], description="Requerido, Debe coincidir con la Contraseña")
    is_active = BooleanField("¿Está activo?")
    public_id = StringField ("*Public id", description="Requerido, Long.Max.:100")
    # photo = HiddenField ("Foto", [Optional(), Length(max=200)], description="")
    tipo = SelectField("Tipo de usuario", validators=[DataRequired()], 
                       choices=[("1", "Afiliado para préstamos"), ("2", "Administrador")],
                       validate_choice=False, description=('Seleccione una opcion'), render_kw={})


class User(db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
    __table_args__ = {'extend_existing': True}  # Agregar esta línea
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique= True)
    email = Column(String(100), nullable=False)
    full_name = Column(String(120))
    passwd = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=False)
    tipo = Column(String(20), nullable=False)
    # photo = Column(String(200),  nullable=True)
    public_id = Column(String(100), nullable= False)
    def check_password(self, password_given:str):
        return Hash.are_equals(self.passwd, password_given)
    
    def encrypt_password(self):
        self.passwd = Hash.encrypt(self.passwd)
    def get_data(self):
        return {'id': self.id, 
                'username': self.username, 
                'email': self.email,
                'passwd': self.passwd,
                'is_active': self.is_active,
                'tipo': self.tipo
                }
