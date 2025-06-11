import smtplib
import random
from email.message import EmailMessage
from flask import Flask, render_template, redirect, session, request

app = Flask(__name__)
app.secret_key = 'king is great'
website_user = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    username = session.get('user')
    if username and username in website_user:
        return render_template('login.html', logged_in=True, username=username)
    return render_template('login.html', logged_in=False)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submit', methods=["POST"])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in website_user:
        user_data = website_user[username]
        if password == user_data[3]:
            session['user'] = username
            return render_template('submit.html', login_success=True, name=user_data[0])
        else:
            return render_template('submit.html', login_success=False, name=user_data[0], error="Invalid Password")
    else:
        return render_template('submit.html', login_success=False, name="", error="User not found")

@app.route('/submit1', methods=["POST"])
def submit1():
    username = request.form.get('username')
    email = request.form.get('email')
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    password = request.form.get('password')

    if username in website_user:
        return render_template('verify_otp.html', name=name)

    # Generate OTP and store info in session
    otp = str(random.randint(111111, 999999))
    session['otp'] = otp
    session['reg_data'] = {
        'username': username,
        'name': name,
        'email': email,
        'mobile': mobile,
        'password': password
    }

    # Send Email
    msg = EmailMessage()
    msg['Subject'] = 'AuthForge Registration'
    msg['From'] = 'cem.maharaja@gmail.com'
    msg['To'] = email
    msg.set_content(f'Your OTP for AuthForge registration is {otp}')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('cem.maharaja@gmail.com', 'fipq iebp vlfv kanp')  # Use App Password!
        smtp.send_message(msg)

        return render_template('verify_otp.html', name=name)

@app.route('/confirm', methods=["POST"])
def confirm():
    entered_otp = request.form.get('OTP')
    real_otp = session.get('otp')
    reg_data = session.get('reg_data')

    if not reg_data:
        return "❌ Registration data expired. Please try again."

    if entered_otp == real_otp:
        username = reg_data['username']
        website_user[username] = [
            reg_data['name'],
            reg_data['mobile'],
            reg_data['email'],
            reg_data['password']
        ]
        session['user'] = username  # auto-login
        return render_template('confirm.html', correct_pass=True, name=reg_data['name'])
    else:
        return render_template('confirm.html', correct_pass=False, name=reg_data['name'])

@app.route('/profile')
def profile():
    username = session.get('user')
    if not username or username not in website_user:
        return render_template('login.html', logged_in=False, error="Please log in to view your profile.")

    user = website_user[username]
    return render_template('profile.html', name=user[0], mobile=user[1], email=user[2], username=username, website_user=website_user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
