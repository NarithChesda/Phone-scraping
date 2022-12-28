import json
import constants
import re
from helpful_scripts import *
from file_handler import *

# This function clean Description and Price format remove
# \n and $,. sign from price and description.
def clean_data():

    for brand in constants.BRANDS:
        data_file = get_today_file_path(f"{brand}.json")
        with open(data_file) as f:
            items = json.load(f)

        for index, i in enumerate(items):
            new_description = i["Description"].replace("\n", " | ")
            items[index]["Description"] = new_description

            # Change price to int
            str_price = i["Price"].split(".")
            price = re.sub("\D", "", str_price[0])
            items[index]["Price"] = int(price)

            # Reformat post date
            post_date = reformat_date(i["Post Date"])
            items[index]["Post Date"] = post_date

        with open(data_file, "w", encoding="utf-8") as w:
            json.dump(items, w, indent=2)

    print("Done!")


def reformat_all_post_date():

    for brand in constants.BRANDS:
        data_paths = get_all_data_paths(brand)
        for path in data_paths:
            with open(path) as f:
                data = json.load(f)

            for post in data:
                post["Post Date"] = reformat_date(post["Post Date"])

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)


def reformat_date(str_date):
    # str_date = "21-Oct-2022"
    if str_date.find("-") != -1:
        post_date = datetime.datetime.strptime(str_date, "%d-%b-%Y")
        # return "2022-10-21"
        return post_date.strftime(constants.DATETIME_FORMAT)

    return str_date


if __name__ == "__main__":
    clean_data()
    # reformat_all_post_date()
