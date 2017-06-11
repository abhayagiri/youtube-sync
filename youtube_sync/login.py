import flask
import flask_login

from . import app


class User(flask_login.UserMixin):
    def __init__(self):
        self.id = 'admin'


login_manager = flask_login.LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User()


@app.route('/login', methods=('GET', 'POST'))
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        password = flask.request.form['password']
        if password == app.config['ADMIN_PASSWORD']:
            user = User()
            flask_login.login_user(user)
            flask.flash('Logged in successfully.')
            return flask.redirect(flask.url_for('index'))
        else:
            flask.flash('Invalid Password.')
            return flask.render_template('login.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))
