import flask
from flask_login import login_required

from . import app, database, tasks


@app.route('/')
@login_required
def index():
    return flask.render_template('index.html')


@app.route('/jobs')
@login_required
def jobs():
    return flask.render_template('jobs.html', jobs=database.get_jobs())


@app.route('/make_audio')
@login_required
def make_audio():
    youtube_id = flask.request.args.get('youtube_id')
    tasks.make_audio.delay(youtube_id)
    flask.flash('Processing YouTube ID: %s' % youtube_id)
    return flask.redirect('/')
