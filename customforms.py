from wtforms import Form, StringField, PasswordField, validators, TextAreaField, FileField
from werkzeug.utils import secure_filename

class LoginForm(Form):
    username = StringField("Username",validators=[
        validators.DataRequired()
    ])
    password = PasswordField("Password",validators=[
        validators.DataRequired(),
    ])


class RegisterForm(Form):
    fullname = StringField("Full Name",validators=[
        validators.DataRequired()
    ])
    email = StringField("E-Mail",validators=[
        validators.DataRequired(),
        validators.Email("Invalid e-mail type!")
    ])
    username = StringField("Username",validators=[
        validators.DataRequired()
    ])
    password = PasswordField("Password",validators=[
        validators.DataRequired(),
        validators.EqualTo("confirmPassword","Passwords doesn't match.")
    ])
    confirmPassword = PasswordField("Confirm Password",validators=[
        validators.DataRequired(),
    ])


class NewBookForm(Form):
    bookphoto = FileField("Book Photo")
    bookname = StringField("Book Name",validators=[
        validators.DataRequired()
    ])
    author = StringField("Author",validators=[
        validators.DataRequired()
    ])
    publisher = StringField("Publisher",validators=[
        validators.DataRequired()
    ])
    pagecount = StringField("Page Count",validators=[
        validators.DataRequired()
    ])