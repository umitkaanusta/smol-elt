from smol.extract import *
from lxml.html import HtmlElement


def test_send_request():
    assert send_request("https://www.google.com/")


def test_find_page_count():
    pg_count = find_page_count()
    assert send_request(url=f"https://www.python.org/jobs/?page={pg_count}")


def test_get_tables():
    page_count = 2
    tables = get_tables(page_count=page_count)
    assert tables
    assert len(tables) == 2
    for table in tables:
        assert isinstance(table, HtmlElement)
        assert table.xpath("./li")


def test_get_li_tags():
    page_count = 2
    tables = get_tables(page_count=page_count)
    li_tags = get_li_tags(tables)
    assert li_tags
    for tag in li_tags:
        assert isinstance(tag, HtmlElement)
    tag_1 = li_tags[0]
    assert tag_1.xpath("./h2[contains(@class, 'listing-company')]")
    assert tag_1.xpath("./span[contains(@class, 'listing-job-type')]")
    assert tag_1.xpath("./span[contains(@class, 'listing-posted')]")
    assert tag_1.xpath("./span[contains(@class, 'listing-company-category')]")


def test_get_posting():
    li_tags = get_li_tags(get_tables(page_count=2))
    tag = li_tags[0]
    post = get_posting(tag)
    assert post
    assert post["job_title"]
    assert post["company"]
    assert post["location"]
    assert post["date_posted"]
    assert post["category"]


def test_get_all_postings():
    li_tags = get_li_tags(get_tables(page_count=2))
    assert get_all_postings(li_tags)
