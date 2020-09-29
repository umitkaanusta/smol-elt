from sqlalchemy.orm import Session
from typing import List

from smol import db_models


def load_record(db: Session, posting: dict):
    record = db_models.Record(**posting)
    # If the record already exists, just pass
    # Each job posting's timestamp is unique
    if db.query(db_models.Record).filter_by(date_posted=record.date_posted).first():
        return None
    db.add(record)
    db.commit()


def load_all_records(db: Session, postings: List[dict]):
    for p in postings:
        load_record(db, posting=p)
