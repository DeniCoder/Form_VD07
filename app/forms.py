from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegisterForm(FlaskForm):
    name = StringField('Имя', [
        DataRequired(message="Поле обязательно для заполнения"),
        Length(min=2, max=100, message="Имя должно быть от 2 до 100 символов")
    ])
    email = StringField('Email', [
        DataRequired(message="Поле обязательно для заполнения"),
        Email(message="Некорректный email")
    ])
    password = PasswordField('Пароль', [
        DataRequired(message="Поле обязательно для заполнения"),
        Length(min=6, message="Пароль должен быть не менее 6 символов")
    ])
    confirm = PasswordField('Подтвердите пароль', [
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])

class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Пароль', [DataRequired()])

class ProfileForm(FlaskForm):
    name = StringField('Имя', [
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = StringField('Email', [
        DataRequired(),
        Email()
    ])
    password = PasswordField('Новый пароль (необязательно)', [
        Length(min=6, message="Пароль должен быть не менее 6 символов"),
        validators.Optional()
    ])