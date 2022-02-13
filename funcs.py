import json
import re
import requests
from statistics import median
import pyotp
import csv


def get_token(secret):
    """Get current token for given secret code"""
    my_token = pyotp.TOTP(secret)
    token = my_token.now()
    return token


def get_profit_percent():
    """Get minimum profit percent from user"""
    while True:
        try:
            percent = float(input("Please input minimum profit percent from 0 to 100: "))
        except ValueError:
            print("Incorrect number inputed")
        else:
            if percent < 0 or percent > 100:
                print("Incorrect number inputed")
            print("Percent saved\n")
            return percent


def print_help():
    """Print help page to console"""
    print("Please input:\n"
          "1, to start searching of skins in given price range and profit rate on bitskins.com\n"
          "2, to get data for found items in steam(actual data and more precise than on bitskins.com)\n"
          "3, to change price range for searching\n"
          "4, to change minimum profit rate\n"
          "5, to change filename for saving results\n"
          "6, to save data into file\n"
          "8, to get this text\n"
          "0, to exit program\n")


def find_median_steam_price(url:str, headers, length=10):
    """Get median steam price using Zenscape API for last *length* deals"""
    if "StatTrak" in url:
        url = url.replace("StatTrak™ ", "StatTrak%E2%84%A2%20")
    params = (
        ("url", url),
    )
    rs = requests.get('https://app.zenscrape.com/api/v1/get', headers=headers, params=params)
    m = re.search(r'var line1=(.+);', rs.text)
    data_str = m.group(1)
    data = json.loads(data_str)
    data = data[-length:] if len(data) >= length else data
    median_price = median([float(sell[1]) for sell in data])
    return median_price


def get_command_int(prompt: str):
    """Safely get command from user"""
    while True:
        try:
            command = int(input(prompt))
        except ValueError:
            print("You did not input integer, please try again")
        else:
            break
    return command


def save_data_steam(filename: str, tech: bool, data):
    """Save data icluding steam prices to .csv file"""
    with open("results/" + filename, 'w', newline='', encoding='utf-16') as f:
        bit_writer = csv.writer(f)
        if tech:
            bit_writer.writerow([
                "item_name", "item_lowest_price", "item_base_price", "bit_based_profit_rate",
                "bit_based_discount", "item_steam_price", "real_profit_rate", "real_discount"
            ])
            bit_writer.writerows(data)
        else:
            bit_writer.writerow([
                "item_name", "item_lowest_price", "real_profit_rate"
            ])
            for item in data:
                bit_writer.writerow([item[0], item[1], item[6]])
        print("Data saved\n")


def save_data_bitskins(filename: str, tech: bool, data):
    """Save data from Bitskins only to .csv file """
    with open("results/" + filename, 'w', newline='', encoding='utf-16') as f:
        bit_writer = csv.writer(f)
        if tech:
            bit_writer.writerow([
                "item_name", "item_lowest_price", "item_base_price",
                "bit_based_profit_rate", "bit_based_discount"
            ])
            bit_writer.writerows(data)
        else:
            bit_writer.writerow([
                "item_name", "item_lowest_price", "bit_based_profit_rate"
            ])
            for item in data:
                bit_writer.writerow([item[0], item[1], item[3]])
        print("Data saved\n")


def get_price(prompt: str):
    """Safely get price range from user"""
    while True:
        try:
            min_max_price = float(input(prompt))
        except ValueError:
            print("Incorrect input, please try again")
        else:
            return min_max_price
