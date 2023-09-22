from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from functools import wraps
from passlib.hash import sha256_crypt
from customforms import LoginForm, RegisterForm


app = Flask(__name__)


app.secret_key="AKC1234"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "bookshelf"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# Index
@app.route("/")
def index():
    return redirect(url_for("loginpage"))


# Login Page
@app.route("/login", methods = ["GET","POST"])
def loginpage():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        usernameInput = form.username.data
        passwordInput = form.password.data

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s"
        result = cursor.execute(query,(usernameInput,))
        if result == 0:
            flash("Username or password is wrong.","danger")
            return render_template("loginpage.html", form = form)
        else:
            userCredentials = cursor.fetchone()
            usersPassword = userCredentials["password"]
            if sha256_crypt.verify(passwordInput,usersPassword):
                session["isLoggedIn"] = True
                session["loggedUserName"] = usernameInput
                flash("Login successfull","success")
                return render_template("home.html", loggedUserName = session["loggedUserName"])
            else:
                flash("Username or password is wrong.","danger")
                return render_template("loginpage.html", form = form)
    else:
        return render_template("loginpage.html", form = form)
    

# Register Page
@app.route("/register", methods = ["GET","POST"])
def registerpage():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        fullname = form.fullname.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()
        checkUsernameQuery = "SELECT * FROM users WHERE username = %s"
        checkUsernameQueryResult = cursor.execute(checkUsernameQuery,(username,))
        if checkUsernameQueryResult == 0:
            insertQuery = "INSERT INTO users(fullname,email,username,password) VALUES (%s, %s, %s, %s)"
            cursor.execute(insertQuery,(fullname,email,username,password))
            mysql.connection.commit()
            cursor.close()
            flash("Signed up successfully. You can login now.","success")
            return redirect(url_for("loginpage"))
        else:
            flash("Username already exists.","danger")
            return render_template("registerpage.html", form = form)
    else:
        return render_template("registerpage.html", form = form)
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("loginpage"))



if __name__ == "__main__":
    app.run(debug=True)