import binascii
import click
import jinja2
import os
import shutil

from . import app, tasks


instance_path = os.path.join(os.path.dirname(app.root_path), 'instance')
local_cfg_path = os.path.join(instance_path, 'local.cfg')
local_cfg_template_path = os.path.join(instance_path, 'local.cfg.tmpl')


def secret(length):
    return binascii.hexlify(os.urandom(length)).decode('utf-8')[:length]


@app.cli.command()
def worker():
    """Run celery worker."""
    os.execvp('celery', ['celery', '--app=youtube_sync.celery', '--loglevel=info', 'worker'])


@app.cli.command()
@click.option('--force', is_flag=True)
@click.option('--dan-bin', type=click.Path(exists=True), help='Path to Dynamic Audio Normalizer bin')
@click.option('--remote-host', type=click.STRING, help='Destination server host')
@click.option('--remote-user', type=click.STRING, help='Destination server user')
@click.option('--remote-path', type=click.Path(), help='Destination server path')
def setup_local_cfg(force, dan_bin, remote_host, remote_user, remote_path):
    """Setup instance/local.cfg."""
    if os.path.exists(local_cfg_path):
        click.echo('Already exists: %s' % local_cfg_path)
        if not force:
            click.echo('Exiting...')
            return
    if remote_host and remote_user and remote_path:
        remote = '%s@%s:%s' % (remote_user, remote_host, remote_path)
    else:
        remote = None
    vars = {
        'CSRF_SESSION_KEY': secret(64),
        'SECRET_KEY': secret(64),
        'ADMIN_PASSWORD': secret(8),
        'DESTINATION_SERVER_PATH': remote,
        'DYNAMIC_AUDIO_NORMALIZER_BIN': dan_bin,
    }
    template = jinja2.Template(open(local_cfg_template_path).read())
    click.echo('Updating/creating: %s' % local_cfg_path)
    open(local_cfg_path, 'w').write(template.render(vars) + '\n')


@app.cli.command()
def add_test_job():
    """Add a test job to the worker queue."""
    youtube_id='pn7w-6leiJA'
    click.echo('Adding job with youtube_id = %s' % youtube_id)
    result = tasks.make_audio.delay(youtube_id)
    click.echo('Added task: %s' % result)
