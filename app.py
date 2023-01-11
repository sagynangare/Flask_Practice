from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
posts =[{
	'author':'Robert T.qsaki',
	'title':'Rich dad',
	'content':'Financial Management',
	'date_posted':"April 20, 2015"
	},
	{
	'author':'Ankur Warikoo',
	'title':'Do epic shits',
	'content':'Financial Management',
	'date_posted':"May 20, 2018"
	}
	]

@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html", posts=posts)

@app.route('/about')
def about():
	return render_template("about.html", title="About")

@app.route('/register',methods=['GET', 'POST'])
def register():
	form = RegistrationForm()

	if form.validate_on_submit():
		flash(f"Account created for {form.username.data}!",'success')
		return redirect(url_for('home'))
	return render_template('register.html',title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
if __name__=="__main__":
	app.run(debug=True)