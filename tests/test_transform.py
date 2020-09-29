from sqlalchemy.orm import Session

from smol import db_models
from smol.database import SessionLocalTest, engine_test
from smol.transform import get_companies, Company


db_models.Base.metadata.create_all(bind=engine_test)

db: Session = SessionLocalTest()


def test_get_companies():
    companies = get_companies(engine_test)
    assert companies
    assert isinstance(companies[0], Company)


def test_company():
    company = get_companies(engine_test)[5]
    assert company.data["job_title"] is not None
    assert company.data["company"] is not None
    assert company.data["location"] is not None
    assert company.data["date_posted"] is not None
    assert company.data["category"] is not None
    assert company.job_titles()
    assert company.most_recent_date_posted()
    assert company.locations()
    assert company.job_categories()
    assert company.hires_remote() is not None
    assert company.hires_intern() is not None
    assert company.line()
