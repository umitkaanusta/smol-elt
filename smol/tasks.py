from sqlalchemy.orm import Session
from prefect import task, Flow
from prefect.schedules import IntervalSchedule
from prefect.triggers import all_successful
from datetime import datetime, timedelta

from smol import db_models
from smol.database import engine, SessionLocal
from smol.extract import find_page_count, get_tables, get_li_tags, get_all_postings
from smol.load import load_all_records
from smol.transform import get_companies
from smol.gsheets_utils import clean_sheet, upload_lines
from smol.sns_utils import send_success_message, send_failure_message

db_models.Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()


schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1),
    interval=timedelta(hours=24)
)


@task(
    name="extract",
    max_retries=3,
    retry_delay=timedelta(seconds=10),
    on_failure=send_failure_message
)
def extract():
    pg_count = find_page_count()
    tables = get_tables(pg_count)
    li_tags = get_li_tags(tables)
    return get_all_postings(li_tags)


@task(
    name="load",
    max_retries=3,
    retry_delay=timedelta(seconds=10),
    on_failure=send_failure_message
)
def load(postings_):
    load_all_records(db, postings_)
    return True


@task(
    name="transform",
    max_retries=3,
    retry_delay=timedelta(seconds=10),
    on_failure=send_failure_message
)
def transform(loaded):
    # Execute T and Write to sheet of the pipeline
    if not loaded:
        return False
    companies = get_companies(engine)
    return [company.line() for company in companies]


@task(
    name="write_to_sheet",
    max_retries=3,
    retry_delay=timedelta(seconds=10),
    on_failure=send_failure_message
)
def write_to_sheet(lines):
    clean_sheet(lines)
    upload_lines(lines)
    return True


@task(
    name="send_message",
    max_retries=3,
    retry_delay=timedelta(seconds=10),
    on_failure=send_failure_message
)
def send_message(written_):
    if written_:
        send_success_message()


with Flow("ELT-Pipeline", schedule=schedule, on_failure=send_failure_message) as flow:
    # ELT, not ETL
    E = extract()
    L = load(E)
    T = transform(L)
    written = write_to_sheet(T)
    send_message(written)
