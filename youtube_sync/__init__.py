from celery import Celery
import click
import flask
import flask_bootstrap
import flask_sqlalchemy

from . import celeryconfig
from . import flaskconfig


def make_app():

    # Flask
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(flaskconfig)
    app.config.from_pyfile('local.cfg', silent=True)

    # Bootstrap
    flask_bootstrap.Bootstrap(app)

    # Celery
    # See http://flask.pocoo.org/docs/0.12/patterns/celery/
    celery = Celery(app.import_name)
    celery.config_from_object(celeryconfig)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    # Click
    @click.group(cls=flask.cli.FlaskGroup, create_app=lambda info: app)
    def cli():
        pass

    # SQLAlchemy
    db = flask_sqlalchemy.SQLAlchemy()
    db.init_app(app)

    return app, celery, cli, db


app, celery, cli, db = make_app()


from . import commands
from . import database
from . import login
from . import routes
from . import tasks
