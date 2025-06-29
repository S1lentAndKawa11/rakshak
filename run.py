from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='app/templates')
app.secret_key = 'very_secret_key_123'
bcrypt = Bcrypt(app)

# -------------------- In-Memory Storage --------------------
users_db = {}  # Stores registered users (mock DB)
admins_db = {
    'admin': bcrypt.generate_password_hash('admin123').decode('utf-8')  # Default admin login
}

# -------------------- Database Connection (not used yet) --------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rakshak"
    )

# -------------------- Forms --------------------
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    phone = StringField('Phone Number', validators=[DataRequired(), Regexp(r'^\+?\d{10,15}$')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Login As', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Login As', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign In')

# -------------------- Pages --------------------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/forum')
def forum():
    stories = [
        {"name": "Anjali Verma", "title": "Distributing Food to Homeless", "description": "I gathered leftover food..."},
        {"name": "Rahul Mehta", "title": "Flood Relief Support", "description": "During the Assam floods..."},
        {"name": "Neha Kumari", "title": "Teaching Kids", "description": "I volunteered to teach children..."}
    ]
    return render_template("forum.html", stories=stories)

@app.route('/post-story', methods=['GET', 'POST'])
def share_story():
    if request.method == 'POST':
        print("Story submitted")
        return redirect(url_for('forum'))
    return render_template("post_story.html")

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer_signup():
    if request.method == 'POST':
        print("Volunteer form submitted")
        return redirect(url_for('home'))
    return render_template("volunteer_signup.html")

@app.route('/donor', methods=['GET', 'POST'])
def donor_dashboard():
    if request.method == 'POST':
        print("Donor form submitted")
        return redirect(url_for('home'))
    return render_template("donor_dashboard.html")

# -------------------- Auth: SignUp & SignIn --------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        if username in users_db:
            flash('Username already exists.', 'danger')
        else:
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            users_db[username] = {
                'phone': form.phone.data,
                'password': hashed_pw,
                'role': form.role.data
            }
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('signin'))
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data

        if role == 'user':
            user = users_db.get(username)
            if user and bcrypt.check_password_hash(user['password'], password):
                session['user'] = username
                flash(f'Welcome, {username}!', 'success')
                return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid user credentials.', 'danger')
        else:
            admin_hash = admins_db.get(username)
            if admin_hash and bcrypt.check_password_hash(admin_hash, password):
                session['admin'] = username
                flash(f'Welcome Admin, {username}!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials.', 'danger')

    return render_template('signin.html', form=form)

@app.route('/user/dashboard')
def user_dashboard():
    if 'user' not in session:
        flash('Login required as user.', 'warning')
        return redirect(url_for('signin'))
    return render_template("user_dashboard.html", username=session['user'])

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash('Login required as admin.', 'warning')
        return redirect(url_for('signin'))
    return render_template("admin_panel.html")

# -------------------- SOS Route --------------------
@app.route('/sos')
def sos():
    return render_template("sos.html")

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('signin'))

# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)
