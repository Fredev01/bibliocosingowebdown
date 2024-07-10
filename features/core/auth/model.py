from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, Boolean
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import StringField, TextAreaField, SubmitField, PasswordField, HiddenField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from features.core.bd import db
from features.core.encrypt import Hash

class LoginForm(FlaskForm):
    username = StringField ("Nombre de usuario", [DataRequired(), Length(max=50)], \
                            description="Requerido, Long.Max.:50")
    password = PasswordField("Contraseña", [DataRequired()], description="Requerido")

class RegisterForm(FlaskForm):
    id = HiddenField ("Id", [], description="")
    username = StringField ("*Cuenta de usuario", [DataRequired(), Length(max=50)], description="Requerido, Long.Max.:100")
    passw = PasswordField("*Password", [], description="Requerido, se requiere almenos una minúscula, una mayúscula, un número y use símbolos: _-!#$%&()")
    confirm  = PasswordField('*Repeat Password', [EqualTo('password', message='No coinciden las contrasñas')], description="Requerido, Debe coincidir con el Password")
    email = StringField('*email', [DataRequired(), Email(message='email inválido')], description="Requerido, Especifique un correo válido")
    full_name = StringField ("*Nombre completo", [DataRequired(), Length(max=120)], description="Requerido, Long.Max.:120")
    is_active = BooleanField("Cuenta activada?", [], description="")
    public_id = StringField ("*Public id", [DataRequired(), Length(max=100)], description="Requerido, Long.Max.:100")
    # photo = HiddenField ("Foto", [Optional(), Length(max=200)], description="")
    tipo = SelectField("*Rol",validators=[DataRequired()],
            choices=[("1", "Afiliado para préstamos"), ("2", "Administrador")],
            description="Elija un rol",
            render_kw={})
    # recaptcha = RecaptchaField()

class UserLogin(UserMixin):
    def __init__(self, username, email, passwd) -> None:
        self.id = username
        self.email = email
        self.passwd = passwd
    @staticmethod
    def query(user_id):
        # user : User = con.query(User).filter_by(username=user_name).first()
        user: User = User.query.filter(User.public_id == user_id).first()
        return UserLogin(user.user_id, user.email, user.passwd)

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False)
    full_name = Column(String(120))
    passwd = Column(String(128), nullable=False)
    public_id = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    # photo = Column(String(200))
    tipo = Column(String(1), nullable=False)

    def get_id(self):
       return self.public_id
        
    def __init__(self, username, email, full_name, passwd, public_id, tipo) -> None:
        self.username = username
        self.email = email
        self.full_name = full_name
        self.passwd = passwd
        self.public_id = public_id
        self.tipo = tipo
        self.is_active = True
        
    def check_password(self, password_given:str):
        return Hash.are_equals(self.passwd, password_given)
    
    def encrypt_password(self):
        self.passwd = Hash.encrypt(self.passwd)
    
    def get_json(self):
        return {'id':self.id, 'username': self.username, 'email': self.email, \
                'full_name' : self.full_name, 'public_id': self.public_id, 'is_active': self.is_active, 'tipo': self.tipo}
