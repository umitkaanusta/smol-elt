from sqlalchemy import Boolean, Column, Integer, String

from smol.database import Base


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String)
    company = Column(String)
    location = Column(String)
    date_posted = Column(String)
    category = Column(String)
