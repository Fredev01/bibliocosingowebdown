from sqlalchemy import Column, ForeignKey, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import FileField, StringField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from features.core.bd import db

class AcervotituloFileForm(FlaskForm):
    id = HiddenField("Id", [DataRequired()], description="")
    file = FileField("*Portada")

class AcervotituloForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    titulo = StringField("*Título del acervo", [DataRequired(), Length(max=100)], description="Campo obligatorio")
    autores = StringField("*Autor(es)", [DataRequired(), Length(max=130),
            Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', message="Solo se permiten letras y acentos en el nombre."),
            Regexp(r'\S', message="El nombre no puede consistir solo en espacios en blanco."),], description="Campo obligatorio")
    editorial_id = SelectField("Editorial",validators=[DataRequired()], choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    tipo_id = SelectField("Tipo",validators=[DataRequired()], choices=[("Elija una opción")],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    descripcion = TextAreaField("*Descripcion", [DataRequired(), Length(max=190)], description="Campo obligatorio")

class Acervotitulo(db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
    __tablename__ = 'acervotitulo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False, unique= True)
    autores = Column(String(130), nullable=False)
    editorial_id   = Column(Integer, index= True,  nullable=False)
    tipo_id = Column(Integer, index= True,  nullable=False)
    descripcion = Column(String(190), nullable=False)
    foto = Column(String(100), nullable=True)

    def get_data(self):
        return {'id': self.id, 
                'titulo': self.titulo, 
                'autores': self.autores,
                'editorial_id': self.editorial_id,
                'tipo_id': self.tipo_id,
                'descripcion': self.descripcion,
                'foto': self.foto,
               }
