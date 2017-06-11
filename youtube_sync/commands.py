import os

from . import app, tasks


@app.cli.command()
def worker():
    """Run celery worker."""
    os.execvp('celery', ['celery', '--app=youtube_sync.celery', '--loglevel=info', 'worker'])


@app.cli.command()
def add_test_job():
    """Add a test job to the worker queue."""
    youtube_id='pn7w-6leiJA'
    click.echo('Adding job with youtube_id = %s' % youtube_id)
    result = tasks.make_audio.delay(youtube_id)
    click.echo('Added task: %s' % result)
