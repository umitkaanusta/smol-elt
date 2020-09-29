from tests.test_extract import *
from tests.test_load import *
from tests.test_transform import *


def main():
    test_send_request()
    test_find_page_count()
    test_get_tables()
    test_get_li_tags()
    test_get_posting()
    test_get_all_postings()
    test_load_record()
    test_get_companies()
    test_company()
    print("Testing successful")


if __name__ == '__main__':
    main()
