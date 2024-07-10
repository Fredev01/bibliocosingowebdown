from sqlalchemy import Column, ForeignKey, Integer, Text, Boolean, String, Float
from sqlalchemy.sql.sqltypes import Date
from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, TextAreaField, HiddenField, SelectField, DateField, BooleanField, DecimalField, EmailField
from wtforms.validators import NumberRange, DataRequired, Length, Optional
from features.core.bd import db


class AcervoejemplarForm(FlaskForm):
    id = HiddenField("Id", [], description="")
    estante_id = SelectField("*Estante",validators=[DataRequired()],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    acervotitulo_id = SelectField("*Titulo del acervo",validators=[DataRequired()],
            validate_choice=False, description=('Seleccione una opcion'), render_kw={})
    numadquisicion = StringField("*Numero de adquisicion", [DataRequired(), Length(max=100)], description="Campo requerido tam. máx. de 100")
    fecharegistro = DateField("*Fecha de registro", [DataRequired()], description="Campo obligatorio")
    nivel = IntegerField("*# Nivel", [DataRequired(), NumberRange(min=1, max=10)], default=4, description="Campo numérico requerido entre 1 y 10")
    estado = SelectField("Estado del acervo",validators=[DataRequired()],
             choices=[("Disponible"), ("Baja")],
             description="Disponible o dado de baja",
             render_kw={})
    esdonado = BooleanField("*Es donado?", [Optional()])
    puedeprestarse = BooleanField("*Puede prestarse?", [Optional()],default=True )
    asignacion_topografica = TextAreaField("*Asignación Topográfica", [DataRequired(), Length(max=50)], description="Campo obligatorio"
                                           ,render_kw={'data-char-count-max': 50, 'rows': 4}
                                           )

class Acervoejemplar(db.Model):
    """Clase model que se mapea con la tabla de BD correspondiente"""
    __tablename__ = 'acervoejemplar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    estante_id = Column(Integer, index= True,  nullable=False)
    acervotitulo_id = Column(Integer, index= True,  nullable=False)
    numadquisicion = Column(String(100), nullable=False, unique=True)
    fecharegistro = Column(String(100), nullable=False)
    nivel = Column(String(100), nullable=False)
    estado = Column(String(50), nullable=False)
    esdonado = Column(Boolean, nullable=True)
    puedeprestarse = Column(Boolean, nullable=True)
    asignacion_topografica = Column(String(50), nullable=False)

    def get_data(self):
        return {'id': self.id, 
                'estante_id': self.estante_id,
                'acervotitulo_id': self.acervotitulo_id,
                'numadquisicion': self.numadquisicion, 
                'fecharegistro': self.fecharegistro,
                'nivel': self.nivel,
                'estado': self.estado,
                'esdonado': self.esdonado,
                'puedeprestarse': self.puedeprestarse,
                'asignacion_topografica': self.asignacion_topografica,
               }
