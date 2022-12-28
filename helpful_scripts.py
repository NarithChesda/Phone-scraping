import datetime
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
import constants
import math


# In this case for Khmer24, using Web driver to automate will caught by Captcha
def start_web_driver_and_get_soup(page_url):
    options = Options()
    # Create random user_agent
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")
    # This option is to suppress this Error:
    # Bluetooth: bluetooth_adapter_winrt.cc:1074 Getting Default Adapter failed.
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # This detach option is to leave browser open after python finish running.
    # options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, executable_path=constants.WEBDRIVER_PATH)
    driver.implicitly_wait(10)
    # Getting HTML source from page_url, if return none, try it 3 times
    for _ in range(3):
        driver.get(page_url)
        # Getting this page HTML throught this method because the result of reuqests.get()
        # is not the same with element inspect in Chrome.
        html = driver.find_element(By.XPATH, "//*").get_attribute("outerHTML")
        soup = BeautifulSoup(html, "lxml")
        if soup is not None:
            break

    return soup


def read_page(soup):
    items = []

    list_unstyled = soup.find("ul", class_="list-unstyled list-items item-list")
    results = list_unstyled.find_all("div", class_="item-detail")

    # print(len(results))
    for li in results:
        item = {
            "Name": "",
            "Description": "",
            "Price": "",
            "Location": "",
            "Views": "",
            "Post Date": "",
            "User Name": "",
            "Telephone": "",
            "Post Link": "",
            "Image": "",
        }

        name = li.find("h2", class_="item-title truncate truncate-2").text
        item["Name"] = name
        description = li.find("p", class_="description truncate truncate-2")
        item["Description"] = description.text
        item["Telephone"] = description.find("i").text
        item["Price"] = li.find("span", class_="price").text

        # Get post link from parent element.
        post_links = li.find_parents("a", class_="border post")
        href = ""
        for link in post_links:
            href = link.get("href")
        item["Post Link"] = href

        # Getting Post Images
        image = li.find_previous("div", class_="item-image")
        item["Image"] = image.img["src"]

        ul = li.find("ul", class_="list-unstyled summary")
        for index, i in enumerate(ul):
            if index == 1:
                item["Location"] = i.text
            elif index == 3:
                item["Post Date"] = i.text
            elif index == 5:
                item["Views"] = i.text
            # print(f'index {index}: {i}')
        items.append(item)

    return items


# We get page number from total search result text on the webpage.
def get_total_page_number(url):
    soup = start_web_driver_and_get_soup(url)
    results_number = soup.find("h2", class_="title").text
    split_results_number = results_number.split(" ")
    str_page_number = split_results_number[0]
    page_number = int(str_page_number) / constants.PAGE_SIZE
    return math.ceil(page_number)


def get_posts_from_page(url):
    try:
        soup = start_web_driver_and_get_soup(url)
        posts = read_page(soup)
        return posts
    except AttributeError as ae:
        print(ae)
        return -1


def get_urls(brand):
    total_page_number = get_total_page_number(constants.BASE_URL.format(brand, 0))
    urls = [
        constants.BASE_URL.format(brand, page_number * constants.PAGE_SIZE)
        for page_number in range(total_page_number)
    ]
    return urls


def get_only_recent_posts(file_path):
    with open(file_path) as f:
        data = json.load(f)

    # ./data/2022-11-23/data.json
    str_date = file_path.split("/")
    file_date = datetime.datetime.strptime(str_date[2], constants.DATETIME_FORMAT)
    # 2022-11-23
    recent_posts = []
    for post in data:
        if post["Post Date"].find("-") != -1:
            post_date = datetime.datetime.strptime(
                post["Post Date"], constants.DATETIME_FORMAT
            )
            post_time = file_date - post_date
            if post_time.days <= 30:
                recent_posts.append(post)
        else:
            recent_posts.append(post)

    return recent_posts


def update_sale_date(post, file_path):
    if post["Post Date"].find("-") != -1:
        str_file_date = file_path.split("/")
        date_one = datetime.datetime.strptime(
            str_file_date[2], constants.DATETIME_FORMAT
        )
        date_two = datetime.datetime.strptime(
            post["Post Date"], constants.DATETIME_FORMAT
        )
        sale_time = date_one - date_two
        return sale_time.days
    else:
        return 1


def find_sale(file_path_one, file_path_two):

    data_one = get_only_recent_posts(file_path_one)
    data_two = get_only_recent_posts(file_path_two)
    print(f"Date one: {len(data_one)} posts")
    print(f"Date two: {len(data_two)} posts")
    sale_list = []
    for post_one in data_one:
        item_sale = True

        for post_two in data_two:
            if post_one["Name"].lower() == post_two["Name"].lower():
                item_sale = False
                break

        if item_sale:
            sale_date = update_sale_date(post_one, file_path_one)
            # Time To Sale In Days
            post_one.update({"TTSID": sale_date})
            sale_list.append(post_one)

    return sale_list
