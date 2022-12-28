from file_handler import get_all_data_path
import os

m_brand = ["sony", "xiaomi", "oppo", "oneplus", "meizu"]

correct_names = {
    "sony": "sony-ericsson",
    "xiaomi": "Xiaomi",
    "oppo": "Oppo",
    "oneplus": "OnePlus",
    "meizu": "Meizu",
}


for brand in m_brand:
    data_paths = get_all_data_path(brand)
    for path in data_paths:
        split_path = path.split("/")
        # ./data/2022-11-20/data_file.json
        os.rename(
            path,
            f"{split_path[0]}/{split_path[1]}/{split_path[2]}/{correct_names[brand]}.json",
        )
