import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

SHEET_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe-zUw3OKXBPfJ3QaX9UVQ9lVoh4he4lYuXlHvaLEpX9Bm7Mw/viewform?usp=dialog"
ZILLOW_CLONE = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(url=ZILLOW_CLONE)
data = response.text

soup = BeautifulSoup(data, "html.parser")

links_list = []
prices_list = []
address_list = []

listings = soup.find_all("li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")

for items in listings:
    link = items.find("a").get("href")
    links_list.append(link)

    price = items.find("span", class_="PropertyCardWrapper__StyledPriceLine").text
    price = price.split("/")[0].split("+")[0]
    prices_list.append(price)

    address = items.find("address").text
    address = address.strip().replace("|", "")
    address_list.append(address)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(SHEET_URL)
wait = WebDriverWait(driver, 5)

for item in range(0, len(address_list)):
    time.sleep(3)
    address_entry = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
        )
    )
    price_entry = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
        )
    )
    link_entry = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
        )
    )

    address_entry.send_keys(address_list[item])
    price_entry.send_keys(prices_list[item])
    link_entry.send_keys(links_list[item])

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "NPEfkd.RveJvd.snByac"))
    )
    submit_button.click()
    print(
        f"(Added) at Index: {item}, Price: {prices_list[item]} \nAddress: {address_list[item]}, \nLink: {links_list[item]}\n"
    )
    refresh_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
        )
    )
    refresh_button.click()

print("--- All entries submitted successfully! ---")
driver.quit()
