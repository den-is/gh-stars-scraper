import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

try:
    GH_USERNAME = os.environ["GH_USERNAME"]
    GH_LOGIN_PASSWORD = os.environ["GH_LOGIN_PASSWORD"]

    GH_LOGIN_URL = os.getenv("GH_LOGIN_URL", "https://github.com/login")
    GH_STARS_URL = f"https://github.com/{GH_USERNAME}?tab=stars"

    CHROME_DRIVER_PATH_ENV = os.environ["CHROME_DRIVER_PATH"]
    CHROME_DRIVER_PATH = Path(CHROME_DRIVER_PATH_ENV).expanduser().resolve()
    GH_LOGIN_WAIT = int(os.getenv("GH_LOGIN_WAIT", 60))
    OUTPUT_FILE = os.getenv("OUTPUT_FILE", "output.json")
except KeyError as e:
    print(f"Missing environment variable: {e}")
    exit(1)

OUTPUT_DICT = {}


def driver_setup():
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 1024)
    return driver


def get_stars(container):
    divs = container.find_elements(By.XPATH, ".//div/div/div")

    for d in divs:
        try:
            repo = d.find_element(By.XPATH, "./div/h3/a")

            details = d.find_element(By.XPATH, ".//details")

            summary = details.find_element(By.XPATH, ".//summary")
            summary.click()
            # wait for menu to appear and load
            time.sleep(1)

            star_menu = details.find_element(By.XPATH, ".//details-menu")
            star_menu_close = WebDriverWait(details, 5).until(
                ec.presence_of_element_located(
                    (By.XPATH, ".//button[@class='SelectMenu-closeButton']")
                )
            )

            star_menu_items = star_menu.find_elements(By.XPATH, ".//div[@role='listitem']")
            categories = []
            for cat in star_menu_items:
                input = cat.find_element(By.TAG_NAME, "input")
                if input.is_selected():
                    categories.append(cat.text)

            if len(categories) == 0:
                print(repo.text.replace(" ", ""), repo.get_attribute("href"))

            star_menu_close.click()
            OUTPUT_DICT[repo.text.replace(" ", "")] = {
                "url": repo.get_attribute("href"),
                "categories": categories,
            }

        except NoSuchElementException:
            pass


def main():

    driver = driver_setup()

    driver.get(GH_LOGIN_URL)

    wait = WebDriverWait(driver, 10)
    insert_username = wait.until(ec.presence_of_element_located((By.NAME, "login")))
    insert_username.send_keys(GH_USERNAME)

    insert_password = driver.find_element(By.NAME, "password")
    insert_password.send_keys(GH_LOGIN_PASSWORD)

    sign_in = driver.find_element(By.NAME, "commit")
    sign_in.click()

    # Input 2FA OTP code
    # Wait user for 60 seconds to finish Login procedure (enter username, password and OTP)

    start_time = time.perf_counter()

    WebDriverWait(driver, GH_LOGIN_WAIT).until(
        ec.presence_of_element_located((By.CLASS_NAME, "AppHeader-user"))
    )

    # open stars page
    driver.get(GH_STARS_URL)

    scrape = True

    while scrape:

        stars_frame = driver.find_element(By.ID, "user-starred-repos")
        get_stars(stars_frame)

        try:
            driver.find_element(By.XPATH, '//button[@disabled="disabled" and text()="Next"]')
            print("Reached the last page")
            scrape = False
        except NoSuchElementException:
            pass

        if scrape:
            next_link = driver.find_element(By.LINK_TEXT, "Next")
            next_link.click()
            # wait for the next page to load
            time.sleep(5)

    driver.quit()

    time_elapsed_str = time.strftime("%M:%S", time.gmtime(time.perf_counter() - start_time))
    print(f"Scraped in (mm:ss): {time_elapsed_str}")

    with open(OUTPUT_FILE, "w") as _out_f:
        json.dump(OUTPUT_DICT, _out_f, indent=2)


if __name__ == "__main__":
    main()
