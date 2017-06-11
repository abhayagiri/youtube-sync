import flask
from flask_login import login_required
import re

from . import app, database, tasks


@app.route('/')
@login_required
def index():
    return flask.render_template('index.html')


@app.route('/jobs')
@login_required
def jobs():
    return flask.render_template('jobs.html', jobs=database.get_jobs())


@app.route('/make_audio', methods=('POST', ))
@login_required
def make_audio():
    raw = flask.request.form['youtube_id']
    matches = re.match(r'(?:(?:http(?:s)??\:\/\/)?(?:www\.)?(?:(?:youtube\.com\/watch\?v=)|(?:youtu.be\/)))?([a-zA-Z0-9\-_]{11})', raw)
    if matches:
        youtube_id = matches.group(1)
        tasks.make_audio.delay(youtube_id)
        flask.flash('Processing YouTube ID: %s' % youtube_id)
        return flask.redirect('/')
    else:
        flask.flash('Invalid YouTube ID: %s' % raw)
        return flask.render_template('index.html')
