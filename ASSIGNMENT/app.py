from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import bcrypt
import MySQLdb.cursors
import random
import re
import logging

app = Flask(__name__)
app.secret_key = '64f64cf225bc996e729c6cecdf0da10cd13d5ca20fbecb8dc7a745e6a48a67cc'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'raju143'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)
#bcrypt = Bcrypt(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.close()
        if account:
            #session['loggedin'] = True
            user = account[1]
            passw = account[2]
            try:
                if bcrypt.checkpw(password.encode('utf-8'),passw.encode('utf-8')):
                #if password == passw:
                    session['username']=username
                    return render_template('index.html')
                else:
                    return render_template('login.html',error='Invalid password')
            except Exception as e:
                return render_template('login.html',error="An error occured")
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)
 


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        cursor = mysql.connection.cursor()
        user = cursor.execute("select * from accounts where username = %s",(username,))
        if user:
            return render_template('register.html',msg="Username exists")
        cursor.close()
        if not re.match(r'^[A-Za-z0-9]{3,20}$', username):
            msg = 'Username must contain 3-20 alphanumeric characters.'
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            msg = 'Invalid email address.'
        elif not re.match(r'^\d{10}$', mobile_number):
            msg = 'Mobile number must be 10 digits.'
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            msg = 'Password must be at least 8 characters long, containing one uppercase letter, one lowercase letter, one number, and one special character.'
        elif password != confirm_password:
            msg = 'Passwords do not match.'
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            try:
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO accounts (username, password, email, mobile_number,confirm_password) VALUES (%s, %s, %s, %s,%s)", (username, hashed_password, email, mobile_number,confirm_password))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('login'))
            except MySQLdb.IntegrityError:
                msg = 'Username or email already exists!'
    return render_template('register.html', msg=msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    msg = ''
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cursor.fetchone()
        cursor.close()
        if account:
            otp = random.randint(100000, 999999)
            session['otp'] = otp
            session['reset_email'] = email
            flash(f'Your OTP is {otp}', 'info')
            return redirect(url_for('reset_password'))
        else:
            msg = 'Email not found!'
    return render_template('forgot_password.html', msg=msg)
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'otp' not in session:
        return redirect(url_for('forgot_password'))
    
    msg = ''
    
    if request.method == 'POST':
        otp = request.form['otp']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        logging.debug(f"Submitted OTP: {otp}, Session OTP: {session['otp']}")
        
        if otp.isdigit() and int(otp) == session['otp']:
            if password == confirm_password:
                email = session['reset_email']
                hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
                
                logging.debug(f"New hashed password: {hashed_password}")
                
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE accounts SET password = %s,confirm_password = %s WHERE email = %s', (hashed_password, confirm_password, email))
                mysql.connection.commit()
                cursor.close()
                
                logging.debug(f"Password updated for email: {email}")
                
                session.pop('otp', None)
                session.pop('reset_email', None)
                
                flash('Your password has been updated!', 'success')
                return redirect(url_for('login'))
            else:
                msg = 'Passwords do not match!'
                logging.debug("Passwords do not match.")
        else:
            msg = 'Invalid OTP!'
            logging.debug("Invalid OTP.")
    
    return render_template('reset_password.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True)


