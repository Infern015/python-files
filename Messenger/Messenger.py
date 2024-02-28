from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

# Dummy database for users
users = {
    'user1@example.com': {'name': 'User 1', 'password': 'password1', 'messages': []},
    'user2@example.com': {'name': 'User 2', 'password': 'password2', 'messages': []}
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            return redirect(url_for('dashboard', email=email))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash('Email already exists', 'error')
        else:
            users[email] = {'name': request.form['name'], 'password': password, 'messages': []}
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard/<email>', methods=['GET', 'POST'])
def dashboard(email):
    if request.method == 'POST':
        recipient = request.form['recipient']
        message = request.form['message']
        if recipient in users:
            users[recipient]['messages'].append({'from': email, 'message': message})
            flash('Message sent successfully', 'success')
        else:
            flash('Recipient not found', 'error')
    return render_template('dashboard.html', user=users[email])

@app.route('/inbox/<email>')
def inbox(email):
    return render_template('inbox.html', user=users[email])

if __name__ == '__main__':
    app.run(debug=True)
