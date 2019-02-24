from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models 

app = Flask(__name__)

##session secret key for our cookie
app.secret_key = 'bryantcabrera.buybyepythonflasksql'

#Set Up Login Manager
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


#Routes
##INDEX route
@app.route('/')
def index():
    # stream = models.Post.select().limit(100)
    return render_template('home.html')

#Database initialization
if __name__ == '__main__':
    ##sets up our tables
    models.initialize()

    ##create admin/default user
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