from file_handler import read_error_urls, save_data, get_today_file_path
from helpful_scripts import get_posts_from_page
import concurrent.futures
import constants


def check_and_go_through_error_urls():

    error_urls = read_error_urls()
    if len(error_urls) > 0:
        print("Going through error urls...")

        posts = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_results = [
                executor.submit(get_posts_from_page, url) for url in error_urls
            ]

            for future in concurrent.futures.as_completed(future_results):
                if future.result() != -1:
                    posts.extend(future.result())

        data_file = get_today_file_path(constants.ERROR_PAGE_POSTS_FILE)
        save_data(posts, data_file)
    else:
        print("No error url...")


if __name__ == "__main__":
    check_and_go_through_error_urls()
