from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired, InputRequired
from passlib.hash import sha256_crypt
import sqlite3
from flask import g
from flask_login import LoginManager, UserMixin, login_user,  login_required, logout_user, current_user
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Defining functions to add generated results to the database
@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        hisi_product = request.form['product']
        hisi_region = request.form['region']
        hisi_image_type = request.form['image_type']
        hisi_language = request.form['language']
        hisi_date = request.form['date']
        hisi_industry = request.form['industry']
        hisi_brand = request.form['brand']
        hisi_description = request.form['description']
        hisi_user = request.form['user']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO history_image(product, region, image_type, language, date, industry, brand, user, description) VALUES(?,?,?,?,?,?,?,?,?)',(hisi_product, hisi_region, hisi_image_type, hisi_language, hisi_date, hisi_industry, hisi_brand, hisi_user, hisi_description))
        conn.commit()
        conn.close()
        return render_template('image.html', genPro=hisi_product, genReg=hisi_region, genImg=hisi_image_type, genLan=hisi_language, genDat=hisi_date, genInd=hisi_industry, genBra=hisi_brand, genUse=hisi_user, genDes=hisi_description)
    else:

        return render_template('image.html')


@app.route('/source', methods=['GET','POST'])
def source():
    if request.method == 'POST':
        hiss_source = request.form['source']
        hiss_provider = request.form['provider']
        hiss_division = request.form['division']
        hiss_region = request.form['region']
        hiss_industry = request.form['industry']
        hiss_user = request.form['user']
        hiss_date = request.form['date'] 
        hiss_description = request.form['description']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO history_source(source, provider, division, region, industry, user, date, description) VALUES(?,?,?,?,?,?,?,?)',(hiss_source, hiss_provider, hiss_division, hiss_region, hiss_industry, hiss_user, hiss_date, hiss_description))
        conn.commit()
        conn.close()
        return render_template('source.html', genSou=hiss_source, genPro=hiss_provider, genDiv=hiss_division, genReg=hiss_region, genInd=hiss_industry, genUse=hiss_user, genDat=hiss_date, genDes=hiss_description)
    else:

        return render_template('source.html')



@app.route('/campaign', methods=['GET', 'POST'])
def campaign():
    if request.method == 'POST':
        hisc_date = request.form['date']
        hisc_division = request.form['division']
        hisc_camtype = request.form['camtype']
        hisc_industry = request.form['industry']
        hisc_region = request.form['region']
        hisc_product = request.form['product']
        hisc_user = request.form['user']
        hisc_description = request.form['description']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO history_campaign(date, division, camtype, industry, region, product, user, description) VALUES(?,?,?,?,?,?,?,?)',(hisc_date, hisc_division, hisc_camtype, hisc_industry, hisc_region, hisc_product, hisc_user, hisc_description))
        conn.commit()
        conn.close()
        return render_template('campaign.html', genPro=hisc_product, genReg=hisc_region, genCam=hisc_camtype, genDiv=hisc_division, genDat=hisc_date, genInd=hisc_industry, genUse=hisc_user, genDes=hisc_description)
    else:

        return render_template('campaign.html')



# Defining Registration Form Class
class RegisterForm(Form):
    fullname = StringField('fullname', [validators.length(min=5)])
    email = StringField('email', [validators.length(min=5)])
    phone = StringField('phone', [validators.length(min=5)])
    zip_code = StringField('zip_code', [validators.length(min=2)])
    street = StringField('street', [validators.length(min=5)])
    city = StringField('city', [validators.length(min=2)])
    country = StringField('country', [validators.length(min=2)])
    username = StringField('username', [validators.length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Ups... Passwords do not match')
    ])
    confirm = PasswordField('confirm')


# Defining Registration route function
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        fullname = form.fullname.data
        email = form.email.data
        phone = form.phone.data
        zip_code = form.zip_code.data
        street = form.street.data
        city = form.city.data
        country = form.country.data
        username = form.username.data
        password = form.password.data
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO admin(fullname,username,password) VALUES(?,?,?)', (fullname,username,password))
        c.execute('INSERT INTO admin_details(email,phone,zip_code) VALUES(?,?,?)', (email,phone,zip_code))
        c.execute('INSERT INTO zip_code(zip_code,street,city,country) VALUES(?,?,?,?)', (zip_code,street,city,country))
        conn.commit()
        conn.close()

        return render_template('register.html', form=form, success="New admin is registered!!")
    return render_template('register.html', form=form)


# Defining New User Form Class
class NewUser(Form):
    ID_User = StringField('ID_User', [validators.length(max=2)])
    user = StringField('user', [validators.length(min=2)])
    department = StringField('department', [validators.length(min=5)])


# Defining new user route function
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    form = NewUser(request.form)
    if request.method == 'POST' and form.validate():
        ID_User = form.ID_User.data
        user = form.user.data
        department = form.department.data
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO user(ID_User,user,department) VALUES(?,?,?)', (ID_User,user,department))
        conn.commit()
        conn.close()

        return render_template('newuser.html', form=form, success="New user is added!!")
    return render_template('newuser.html', form=form)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data.db')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def valid_login(username, password):
    user = query_db('select * from admin where username = ? and password = ?', [username, password], one=True)
    if user is None:
        return False
    else:
        return True


#def log_the_user_in(username):
#    return render_template('admin.html', username=username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return redirect(url_for('admin'))
        else:
            error = 'Invalid username/password'

    return render_template('login.html', error=error)


@app.route('/admin')
def admin():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT history_image.user, history_image.language, COUNT(user.user) FROM user INNER JOIN history_image on user.user = history_image.user group by history_image.user, history_image.language ORDER BY 3 DESC')
    data = c.fetchall()
    c.execute('SELECT history_campaign.user, history_campaign.product, COUNT(user.user) FROM user INNER JOIN history_campaign on user.user = history_campaign.user group by history_campaign.user, history_campaign.product ORDER BY 3 DESC')
    data1 = c.fetchall()
    c.execute('SELECT admin.fullname, history_image.region, COUNT(record_id) FROM admin INNER JOIN history_image on admin.fullname = history_image.user group by admin.fullname, history_image.region order by 3 desc')
    data2 = c.fetchall()
    c.execute('SELECT admin.fullname, history_campaign.region, COUNT(record_id) FROM admin INNER JOIN history_campaign on admin.fullname = history_campaign.user group by admin.fullname, history_campaign.region order by 3 desc')
    data3 = c.fetchall()
    c.execute('SELECT (SELECT COUNT(record_id) FROM history_image) AS image_count, (SELECT COUNT(record_id) FROM history_campaign) AS campaign_count, (SELECT COUNT(record_id) FROM history_source) AS source_count')
    data4 = c.fetchall()
    c.execute('SELECT (SELECT COUNT(user) FROM user) AS user_count, (SELECT COUNT(id_admin) FROM admin) AS admin_count')
    data5 = c.fetchall()
    return render_template('admin.html', data=data, data1=data1, data2=data2, data3=data3, data4=data4, data5=data5)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)