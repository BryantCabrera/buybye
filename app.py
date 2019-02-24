from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models
import forms

app = Flask(__name__)

##session secret key for our cookie
app.secret_key = 'bryantcabrera.buybyepythonflasksql'

#Sets Up Login Manager
##loginManager sets up our session for us, manages our session, and loads our user for us
#instantiates an instance of our loginManager
login_manager = LoginManager() 
##attaches to our app
login_manager.init_app(app)
##sets up the default login view, this will be helpful for any errors that happen, it will redirect to this view
login_manager.login_view = 'login'

@login_manager.user_loader
##when we log in a user, they get attached to userid
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

#Database Set-Up
@app.before_request
def before_request():
        """Connects to the database before each request"""
        g.db = models.DATABASE
        g.db.connect()
        g.user=current_user

@app.after_request
def after_request(response):
    """Closes the databased connection after each request"""
    g.db.close()
    return response

#Routes
##REGISTER route - combines POST & GET requests
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm() #this .RegisterForm() must match the classname from forms.py
    ##this if statement handles the post request
    if form.validate_on_submit():
        ##just returns true or false
        flash('Yay you registered', 'success')
        models.User.create_user(
            username=form.username.data, #getting from form's property called "username"
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    ##the response fo the GET request
    ##inject the form as variable form into this view
    return render_template('register.html', form=form) 

##LOGIN route
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Your email or password doesn\'t match.', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                ##login our user / create our session
                login_user(user)

                return redirect(url_for('index'))

            else:
                flash('Your email or password doesn\'t match.', 'error')

    ###GET route
    return render_template('login.html', form=form)

##LOGOUT route
@app.route('/logout')
@login_required
def logout():
    ##destroys our session
    logout_user() #given to us by Flask login manager
    flash('You\'ve been successfully logged out.', 'success')
    return redirect(url_for('index'))

##INDEX route
@app.route('/')
def index():
    # stream = models.Post.select().limit(100)
    listings = models.Post.select().limit(100)
    return render_template('listings.html', listings=listings)

#SHOW Posts/Listings route
@app.route('/listings')
@app.route('/listings/<username>')
def stream(username=None):
    template = 'listings.html'
    ##check
    if username and username != current_user.username:
        ##if the username is in the url and the user is NOT the person with the session
        ##the ** (like) means case doesn't matter
        user = models.User.select().where(models.User.username**username).get()
        ##.posts is coming from our user model
        listings = user.posts.limit(100)
    else:
        listings = current_user.get_posts().limit(100)
        user = current_user
    if username:
        template = 'user_profile.html'
    return render_template(template, listings=listings, user=user)

#Database initialization
if __name__ == '__main__':
    ##sets up our tables
    models.initialize()

    ##creates admin/default user
    try:
        ##Creates Admin User
        ##happens once when you start up your app
        ##don't have to create user by default, just nice to have when you create your app
        models.User.create_user(
            username='bryant',
            email='bryant@bryant.com',
            password='bryant',
            admin=True
        )
    except ValueError:
        pass #means just ignore all of this and keep going

    app.run(debug=True, port=8000)