from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired("Usuário Obrigatório")])
    password = PasswordField("password", validators=[DataRequired("Senha Obrigatória")])
    remember_me = BooleanField("remember_me")

class PostForm(FlaskForm):
    text = TextAreaField("text", validators=[DataRequired(),Length(min=1, max=140, message="Tweet não pode ter mais que 140 caractéres")])
    

class SigninForm(FlaskForm):
    username = StringField("username", validators=[DataRequired("Usuário obrigatório")])
    password = PasswordField("password", validators=[DataRequired("Senha obrigatória")])
    confirmPassword  = PasswordField('confirmPassword',validators=[DataRequired("Confirmação obrigatória"), EqualTo('password', message='Senhas não são iguais')])
    name = StringField("name", validators=[DataRequired("Nome obrigatório")])
    email = StringField("email", validators=[DataRequired("Email obrigatório"),Email("Esse campo deve conter um email válido")])
