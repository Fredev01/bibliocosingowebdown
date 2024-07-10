from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, FileField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, Optional #Email, EqualTo
from features.core.bd import db
from datetime import datetime, timedelta

# Función de validación personalizada
def validate_custom_field(form, field):
    today = datetime.today().date()
    min_date = today - timedelta(days=10*365)  # Restar 10 años en días
    # if field.data > today or field.data < min_date:
    if field.data > min_date:
        raise ValidationError('La fecha debe ser de por lo menos de hace 10 años.')
    # if len(field.data) < 5:
    #     raise ValidationError('El campo debe tener al menos 5 caracteres.')
class AfiliadoFileForm(FlaskForm):
    id = HiddenField("Id", [DataRequired()], description="")
    file = FileField("*Frente")

class AfiliadoForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    nombrecompleto = StringField ("*Nombre del visitante", [DataRequired(), Length(max=100),
            Regexp(r'\S', message="El nombre no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")
    fechanacimiento = DateField ("*Fecha de nacimiento.", validators=[DataRequired(), validate_custom_field], description="Fecha de nacimiento")
    sexo = SelectField("Sexo",validators=[DataRequired()],
             choices=[("Hombre"), ("Mujer"), ("indefinido")],
             description="Hombre o Mujer o indefinido",
             render_kw={})
    capacidaddiferente = SelectField("Capacidad diferente",validators=[DataRequired()],
             choices=[("No"), ("Si")], render_kw={})
    observaciones = TextAreaField ("Datos de contacto (Tel., cel., correo, domicilio, otros)", validators=[Length(max=250)], description="Long.Max.:250")
    user_id = SelectField("Cuenta de usuario solo para afiliados", choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})

class Afiliado (db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombrecompleto = Column(String(100), nullable=False)
    fechanacimiento = Column(Date, nullable=False)
    sexo = Column(String(10), nullable=False)
    capacidaddiferente = Column(String(10), nullable=True)
    observaciones = Column(String(250), nullable=True)
    credencialfrente = Column(String(100), nullable=True)
    credencialreverso = Column(String(100), nullable=True)
    user_id = Column(Integer, index=True, nullable=True)


    def get_data(self):
        return {'id':self.id, 
                'nombrecompleto': self.nombrecompleto, 
                'fechanacimiento': self.fechanacimiento,
                'sexo': self.sexo,
                'capacidaddiferente': self.capacidaddiferente,
                'observaciones': self.observaciones,
                'user_id': self.user_id,
                'credencialfrente': self.credencialfrente,
                'credencialreverso': self.credencialreverso,
                }
    