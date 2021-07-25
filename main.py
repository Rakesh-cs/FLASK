from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import mysql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rakeshcs '
app.config['MYSQL_DB'] = 'jshareweb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=8, max=25)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords Do Not Match')])
    confirm = PasswordField('ConfirmPassword')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))



    cur = mysql.connection.cursor()
    cur = cur.excecute("INSERT INTO users(name,email,username,password,) VALUES(%s,%s,%s,%s) ",
                       (name, email, username, password))

    mysql.connection.commit()
    cur.close()

    flash("you are now registered and can login ", 'Sucess')
    redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ != '__main__':
    app.run(debug=True)
