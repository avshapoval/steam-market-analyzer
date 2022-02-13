import os
import sys

from funcs import *


my_secret = 'SECRET_CODE_BITSKINS'
api = "BITSKINS_API_KEY"
zenscrape_headers = {"apikey": "ZENSCAPE_API_KEY"}

min_price = 0
max_price = float('inf')
min_profit_percent = 0.25
filename = "bitskins.csv"

found = []
result = []
print_help()
while True:
    prompt = "Please input command(8 to get help, 0 to exit program): "
    global_command = get_command_int(prompt)
    print()
    # Search items with given price range and profit rate on bitskins
    if global_command == 1:
        found = []
        result = []
        token = get_token(my_secret)

        url = f"https://bitskins.com/api/v1/get_all_item_prices/?api_key={api}&code={get_token(my_secret)}" \
              f"&app_id=730"
        basic_prices = {
              item['market_hash_name']: float(item['price']) for item in requests.get(url).json()["prices"]
        }

        url2 = f"https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key={api}" \
               f"&code={get_token(my_secret)}&app_id=730"
        selling_prices = [
            [item['market_hash_name'], float(item['lowest_price'])] for item in requests.get(url2).json()["data"]["items"]
            if item["recent_sales_info"] is not None and float(item['lowest_price']) != 0
        ]
        

        for item in selling_prices:
            if not (min_price <= item[1] <= max_price):
                continue
            if (min_profit_percent + 1) * item[1] <= basic_prices[item[0]]:
                found.append([
                    item[0], item[1], basic_prices[item[0]],
                    (basic_prices[item[0]]/item[1] - 1)*100,
                    str(1 - (basic_prices[item[0]] - item[1])/basic_prices[item[0]]) + "%"
                ])

        found.sort(key=lambda item: item[-2], reverse=True)

    # Get info for found items on steam(sometimes, bitskins is not precise)
    elif global_command == 2:
        prompt = "Note that the process of checking prices is relatively long because every single item" \
                 "is checked directly into steam.\n" \
                 "Also note that stopping running process will lead to loss of every checked item info." \
                 "Zenscrape is used to avoid temporary IP ban.\n" \
                 "Please enter the amount of items to check price(-1 if all): "
        items_to_check = get_command_int(prompt)
        if not found:
            print("You haven't searched for any items or none of them were found.\n")
            continue

        if items_to_check == -1:
            items_to_check = len(found)
        elif items_to_check <= 0:
            continue

        result = []
        for index, item in enumerate(found[:items_to_check]):
            url = f"https://steamcommunity.com/market/listings/730/{item[0]}"
            print(f"Checking steam data of {index + 1} item of {items_to_check}, url: {url}")

            try:
                median_price = find_median_steam_price(url, zenscrape_headers)
            except AttributeError:
                print("Failed")
                continue

            print("Succesful")
            item.extend([median_price, (median_price / item[1] - 1) * 100,
                         str((1 - (median_price - item[1]) / median_price) * 100) + "%"])
            result.append(item)

    # Change price range
    elif global_command == 3:
        while True:
            prompt = "Please input minimum price on Bitskins: "
            min_price = get_price(prompt)
            break
        while True:
            prompt = "Please input maximum price on Bitskins: "
            max_price = get_price(prompt)
            if max_price < min_price or max_price < 0:
                continue
            break
        print("Price range saved\n")

    # Change minimum profit
    elif global_command == 4:
        min_profit_percent = get_profit_percent() / 100

    # Change filename for future data saving
    elif global_command == 5:
        filename = input("Please input filename without extension: ") + ".csv"

    # Save data
    elif global_command == 6:
        if not found:
            print("Saved data is empty, nothing is written")
        try:
            os.mkdir("results")
        except FileExistsError:
            pass

        prompt = "Which data to save: checked in steam or raw bitskins data?(2 - steam, 1 - bitskins): "
        user_command = get_command_int(prompt)
        if user_command == 0:
            continue

        elif user_command == 1:
            prompt = "Should technical info be saved? y/n"
            tech_save = input(prompt)
            if tech_save == "y":
                save_data_bitskins(filename, True, found)
            else:
                save_data_bitskins(filename, False, found)

        elif user_command == 2:
            prompt = "Should technical info be saved? y/n: "
            tech_save = input(prompt)
            if tech_save == "y":
                save_data_steam(filename, True, result)
            else:
                save_data_steam(filename, False, result)
        print("Data saved succesfully\n")

    # Output help "page"
    elif global_command == 8:
        print_help()
        continue

    # Exit program
    elif global_command == 0:
        sys.exit()
