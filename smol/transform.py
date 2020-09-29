from sqlalchemy.orm import Session
import pandas as pd
from typing import List

from smol.extract import find_page_count, get_tables, get_li_tags, get_all_postings
from smol.load import load_all_records
from smol.database import engine, SessionLocal
from smol import db_models

db_models.Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()


def get_companies(db_engine):
    names = pd.read_sql("SELECT DISTINCT company FROM records", db_engine)["company"].tolist()
    return [Company(n, db_engine) for n in names]


class Company:
    def __init__(self, name, db_engine):
        self.name = name
        # Separates company objects created for test and production purposes
        self.db_engine = db_engine

    @property
    def data(self):
        return pd.read_sql(f"SELECT * FROM records WHERE company = '{self.name}'", self.db_engine)

    def locations(self):
        return list(set(self.data["location"].tolist()))

    def job_titles(self):
        return list(set(self.data["job_title"].tolist()))

    def job_categories(self):
        return list(set(self.data["category"].tolist()))

    def hires_remote(self):
        titles = self.job_titles()
        locations = self.locations()
        yes_cond = (any("remote" in title.lower() for title in titles) or
                any("remote" in location.lower() for location in locations))
        return "Yes" if yes_cond else "No"

    def hires_intern(self):
        titles = self.job_titles()
        yes_cond = any("intern" in title.lower() for title in titles)
        return "Yes" if yes_cond else "No"

    def most_recent_date_posted(self):
        return self.data["date_posted"].sort_values(ascending=False)[0]

    def line(self):
        # Provides ready data to be written as a line on google spreadsheets
        return {
            "company": self.name,
            "job_titles": str(self.job_titles()),
            "job_categories": str(self.job_categories()),
            "locations": str(self.locations()),
            "hires_remote": self.hires_remote(),
            "hires_intern": self.hires_intern(),
            "latest_posting": self.most_recent_date_posted()
        }
