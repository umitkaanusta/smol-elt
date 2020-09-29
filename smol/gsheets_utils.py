# This module aims to separate the operations done via the Google Sheets API from the rest of the app
import gspread
from gspread.exceptions import APIError
from typing import List

gc = gspread.service_account(filename="../credentials/gsheet_credentials.json")

sh = gc.open("Python.org Jobs")  # Change the title accordingly if you're gonna use it for smth else
ws = sh.sheet1  # Current worksheet


def clean_sheet(lines: List[dict]):
    # After each transformation, transformed versions of the records in jobs.db
    # gets uploaded to the spreadsheet. We clean the sheet and rewrite the output of transform stage
    # to avoid conflicts
    if not isinstance(lines[0], dict):
        pass  # If nothing is uploaded, don't clean the sheet
    try:
        ws.delete_rows(start_index=2, end_index=100_000)
    except APIError:
        pass


def upload_to_sheet(line: dict):
    print(line)
    values = [*line.values()]
    ws.append_row(values)


def upload_lines(lines: List[dict]):
    for line in lines:
        upload_to_sheet(line)
