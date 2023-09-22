from wtforms import Form, StringField, PasswordField, validators, TextAreaField

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