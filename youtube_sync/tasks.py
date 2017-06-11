from datetime import datetime
import os
import re
import subprocess

from . import app, celery, db
from .database import Job


@celery.task()
def make_audio(youtube_id):
    worker_path = os.path.join(app.root_path, 'worker.sh')
    cmd = [worker_path, youtube_id]
    job = Job(command=repr(cmd))
    db.session.add(job)
    db.session.commit()
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
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
