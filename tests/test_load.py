from sqlalchemy.orm import Session

from smol import db_models, load
from smol.database import SessionLocalTest, engine_test


db_models.Base.metadata.create_all(bind=engine_test)

db: Session = SessionLocalTest()

test_posting = {
    "job_title": "Test",
    "company": "Test Inc.",
    "location": "Neverland",
    "date_posted": "Now",
    "category": "Testing"
}


def test_load_record():
    load.load_record(db, test_posting)
    assert db.query(db_models.Record).filter_by(date_posted=test_posting["date_posted"]).first()
    # Testing whether the function returns None if we add duplicate lines
    assert load.load_record(db, test_posting) is None
    db.rollback()
    db.close()

# load_all_records won't be tested
