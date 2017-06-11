from datetime import datetime
import os
import re
import subprocess

from . import app, celery, db
from .database import Job


@celery.task()
def make_audio(youtube_id):
    worker_path = os.path.join(app.root_path, 'worker.sh')
    env = {
        'DYNAMIC_AUDIO_NORMALIZER_BIN': app.config['DYNAMIC_AUDIO_NORMALIZER_BIN'],
        'DESTINATION_SERVER_PATH': app.config['DESTINATION_SERVER_PATH'],
    }
    job([worker_path, youtube_id], env=env)


def job(cmd, env={}):
    job_env = os.environ.copy()
    job_env.update(env)
    job = Job(command=repr(cmd))
    db.session.add(job)
    db.session.commit()
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, env=job_env)
        return_code = 0
    except subprocess.CalledProcessError as e:
        output = e.output
        return_code = e.returncode
    job.complete = True
    job.return_code = return_code
    job.output = output.decode('utf-8')
    job.completed_at = datetime.now()
    db.session.commit()
    return return_code == 0
