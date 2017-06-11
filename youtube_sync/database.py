from datetime import datetime

from . import app, db


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String, nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    completed_at = db.Column(db.DateTime)
    return_code = db.Column(db.Integer)
    output = db.Column(db.UnicodeText)


def get_jobs():
    return db.session.query(Job).order_by(Job.started_at.desc()).all()


with app.app_context():
    db.create_all()
