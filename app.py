from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Users data file
USERS_FILE = 'users.json'

# Admin credentials
ADMIN_USERNAME = 'Madhav'
ADMIN_PASSWORD = 'Madhav@0701'

# Function to load users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to save users
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    return '''
    <h1>Welcome to My Tool Website</h1>
    <p>Name: bøyfrîènd pîìè</p>
    <p>Contact: WhatsApp - 9674758561</p>
    <a href="/register">Register</a> | <a href="/login">Login</a> | <a href="/admin">Admin Login</a>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'Username already exists! Please choose a different username.'
        users[username] = {
            'name': name,
            'password': password,
            'approved': False
        }
        save_users(users)
        return 'Registration successful! Await admin approval.'
    return '''
    <h2>Register</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br>
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <button type="submit">Register</button>
    </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            if user['approved']:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return 'Your account is not approved yet by admin.'
        else:
            return 'Invalid credentials!'
    return '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'''
        <h2>Welcome, {session['username']}</h2>
        <p>This is your dashboard.</p>
        <a href="/logout">Logout</a>
        '''
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_user = request.form['admin_user']
        admin_pass = request.form['admin_pass']
        if admin_user == ADMIN_USERNAME and admin_pass == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            return 'Invalid admin credentials!'
    return '''
    <h2>Admin Login</h2>
    <form method="POST">
        Admin Username: <input type="text" name="admin_user" required><br>
        Admin Password: <input type="password" name="admin_pass" required><br>
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/admin_panel')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    users = load_users()
    users_html = ''
    for user, info in users.items():
        users_html += f'''
        <li>
            Name: {info['name']} | Username: {user} | Approved: {info['approved']}
            {'<a href="/approve/{}">Approve</a>'.format(user) if not info['approved'] else ''}
        </li>
        '''
    return f'''
    <h2>Admin Panel</h2>
    <h3>Users Pending Approval</h3>
    <ul>
        {users_html}
    </ul>
    <a href="/logout_admin">Logout</a>
    '''

@app.route('/approve/<username>')
def approve_user(username):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    users = load_users()
    if username in users:
        users[username]['approved'] = True
        save_users(users)
        return redirect(url_for('admin_panel'))
    return 'User not found!'

@app.route('/logout_admin')
def logout_admin():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
