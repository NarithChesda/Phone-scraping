from helpful_scripts import get_posts_from_page, get_urls
from file_handler import save_data, write_error_url, get_today_file_path
from clean_data import clean_data
from check_and_go_through_error_urls import check_and_go_through_error_urls
import constants
import time
import concurrent.futures


def main():

    for brand in constants.BRANDS:
        urls = get_urls(brand)
        posts = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_results = [executor.submit(get_posts_from_page, url) for url in urls]

            for index, future in enumerate(
                concurrent.futures.as_completed(future_results)
            ):
                if future.result() != -1:
                    posts.extend(future.result())
                else:
                    err_url = constants.BASE_URL.format(
                        brand, index * constants.PAGE_SIZE
                    )
                    write_error_url(err_url)

        data_file = get_today_file_path(f"{brand}.json")
        save_data(posts, data_file)


if __name__ == "__main__":
    start_time = time.time()
    main()
    check_and_go_through_error_urls()
    clean_data()
    print(f"This program take: {(time.time() - start_time) / 60}mn")
