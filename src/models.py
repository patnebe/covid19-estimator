import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()


def setup_db(app, database_path=None):
    """
    Database setup. This will use sqlite, an in-memory relational database, since the database path is set to none.
    """
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Log_entry(db.Model):
    __tablename__ = "request_response_latency_log"

    id = Column(Integer, primary_key=True)
    request_method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    latency_ms = Column(Integer)

    def __init__(self, request_method, path, status_code, latency_ms):
        self.request_method = request_method
        self.path = path
        self.status_code = status_code
        self.latency_ms = latency_ms

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return f"{self.request_method}\t\t{self.path}\t\t{self.status_code}\t\t{self.latency_ms} ms\n"
