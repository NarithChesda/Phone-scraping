import os
import json
import constants
from datetime import date


def get_today_file_path(file_name):
    today = str(date.today())
    directory = f"../data/{today}"
    # Check if the folder of today isn't exist, then create one.
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Construct file path
    today_file = f"{directory}/{file_name}"
    if not os.path.exists(today_file):
        f = open(today_file, "a")
        json.dump([], f)
        f.close()

    return today_file


def write_error_url(url):
    error_url_file = get_today_file_path(constants.ERROR_PAGE_URL)

    with open(error_url_file) as f:
        error_page_url = json.load(f)

    error_page_url.append(url)

    with open(error_url_file, "w") as w:
        json.dump(error_page_url, w, indent=2)


def read_error_urls():
    error_url_file = get_today_file_path(constants.ERROR_PAGE_URL)
    with open(error_url_file) as f:
        error_urls = json.load(f)
    return error_urls


def save_data(posts, data_file):
    try:
        with open(data_file) as f:
            data = json.load(f)
    except ValueError as err:
        print(err)
        data = []

    data.extend(posts)
    with open(data_file, "w", encoding="utf-8") as w:
        json.dump(data, w, indent=4)


# This function is use to save page number while we're looping through
# all the pages, we save the page number in case something happen.
# We can continue without having to go through it again.
def write_saved_page_memory(brand, page_number):
    with open(constants.SAVED_PAGE_MEMORY, "w") as f:
        saved = f"{brand}: {str(page_number)}"
        f.write(saved)


def read_saved_page_memory():
    with open(constants.SAVED_PAGE_MEMORY, "r") as f:
        read_memory = f.read().split(": ")
        brand = read_memory[0]
        page_number = int(read_memory[1])
    return brand, page_number


def get_all_data_paths(brand):
    root_dir = "./data"
    data_paths = []
    for it in os.scandir(root_dir):
        if it.is_dir():
            date = it.path.split("\\")
            data_path = f"{root_dir}/{date[1]}/{brand}.json"
            if os.path.exists(data_path):
                data_paths.append(data_path)

    return data_paths
