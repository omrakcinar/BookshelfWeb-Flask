from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from functools import wraps
from passlib.hash import sha256_crypt
from customforms import LoginForm, RegisterForm, NewBookForm
import json


app = Flask(__name__)
app.config.from_file("config.json", load=json.load)
mysql = MySQL(app)


# Decorators
def loginRequired(func):
        @wraps(func)
        def decoratedFunc(*args,**kwargs):
            if "isLoggedIn" in session:
                return func(*args,**kwargs)
            else:
                flash("You need to log in first.","warning")
                return redirect(url_for("loginpage"))
        return decoratedFunc



# Index
@app.route("/")
@loginRequired
def index():
    cursor = mysql.connection.cursor()
    searchQuery = "SELECT * FROM books WHERE owner = %s"
    cursor.execute(searchQuery,(session["loggedUserName"],))
    booklist = cursor.fetchall()
    return render_template("home.html", loggedUserName = session["loggedUserName"], booklist = booklist)


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
                return redirect(url_for("index"))
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
    

# Add Book Page
@app.route("/addbook", methods = ["GET","POST"])
@loginRequired
def addbook():
    form = NewBookForm(request.form)
    if request.method == "POST" and form.validate():
        booknameEntry = form.bookname.data
        authorEntry = form.author.data
        publisherEntry = form.publisher.data
        pagecountEntry = form.pagecount.data
        owner = session["loggedUserName"]

        cursor = mysql.connection.cursor()
        addBookQuery = "INSERT INTO books(bookname,author,publisher,pagecount,owner) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(addBookQuery,(booknameEntry,authorEntry,publisherEntry,pagecountEntry,owner))
        mysql.connection.commit()
        flash("New book added to your bookshelf.","info")
        return redirect(url_for("index"))
    else:
        return render_template("addbook.html", form = form)
    

# Book Details
@app.route("/book/<string:bookid>")
@loginRequired
def bookdetail(bookid):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM books WHERE id = %s AND owner = %s"
    queryResult = cursor.execute(query,(bookid,session["loggedUserName"]))
    if queryResult > 0:
        selectedBook = cursor.fetchone()
        return render_template("bookdetail.html",selectedBook = selectedBook)
    else:
        flash("This book doesn't exists","warning")
        return redirect(url_for("index"))
    

# Delete Book
@app.route("/deletebook/<string:bookid>")
@loginRequired
def deletebook(bookid):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM books WHERE id = %s AND owner = %s"
    queryResult = cursor.execute(query,(bookid,session["loggedUserName"]))
    if queryResult > 0:
        deleteQuery = "DELETE FROM books WHERE id = %s AND owner = %s"
        cursor.execute(deleteQuery,(bookid,session["loggedUserName"]))
        mysql.connection.commit()
        flash("Deleted book successfully.","info")
        return redirect(url_for("index"))
    else:
        flash("This book doesn't exists or you are unauthorized to delete it.","danger")
        return redirect(url_for("index"))



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("loginpage"))



if __name__ == "__main__":
    app.run(debug=True)