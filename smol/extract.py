import requests
from lxml import html
from itertools import chain


def send_request(url):
    return requests.get(
        url=url,
        headers={
            "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit 537.36 "
                           "(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")
        }
    )


def find_page_count():
    c = 0
    while send_request(url=f"https://www.python.org/jobs/?page={c+1}"):
        c += 1
    return c


def get_tables(page_count):
    tables = []
    for i in range(page_count):
        resp = send_request(url=f"https://www.python.org/jobs/?page={i+1}")
        tables.append(html.fromstring(resp.text).xpath("/html/body/div/div[3]/div/section/div/ol")[0])
    return tables


def get_li_tags(table_list):
    li_tags = [table.xpath("./li") for table in table_list]
    return list(chain.from_iterable(li_tags))


def get_posting(li_tag):
    return {
        "job_title": li_tag.xpath("./h2/span[1]/a/text()")[0],
        "company": " ".join(li_tag.xpath("./h2/span[1]/text()")).strip(),
        "location": li_tag.xpath("./h2/span[2]/a/text()")[0],
        "date_posted": li_tag.xpath("./span[2]/time/@datetime")[0],
        "category": li_tag.xpath("./span[3]/a/text()")[0]
    }


def get_all_postings(tag_list):
    return [get_posting(tag) for tag in tag_list]
