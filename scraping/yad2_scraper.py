from typing import Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraping.yad2_feed_item import Address, FeedItem


def close_popup(driver):  # pylint: disable=redefined-outer-name
    try:
        popup_button = driver.find_element(
            by=By.CSS_SELECTOR, value="#overlay_comp > section > div > button"
        )
        if popup_button:
            popup_button.click()
    except NoSuchElementException:
        pass


def scrape_address(soup, item_id) -> Address:
    street_and_number = (
        soup.find("span", {"id": f"feed_item_{item_id}_title"})
        .find("span", class_="title")
        .text.strip()
    )
    floor = soup.find("span", {"id": f"data_floor_{item_id}"}).text.strip()

    subtitle = soup.find("span", {"class": "subtitle"}).text.strip()
    neighborhood, city = [p.strip() for p in subtitle.split(",")[-2:]]
    return Address(
        city=city,
        street_and_number=street_and_number,
        neighborhood=neighborhood,
        floor=floor,
    )


def scrape_seller_details(
    driver, item_id  # pylint: disable=redefined-outer-name
) -> Tuple[str, str]:
    contact_seller_css_selector = f"#contact_seller_{item_id} > button"

    # Wait for the button to be visible
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, contact_seller_css_selector))
    )

    # Locate and click the 'contact_seller' button
    contact_seller_button = driver.find_element(
        By.CSS_SELECTOR,
        contact_seller_css_selector,
    )

    close_popup(driver)
    contact_seller_button.click()
    close_popup(driver)

    # Wait for the details to appear
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, f"seller_name_{item_id}"))
    )

    # Parse the popup details
    seller_name = driver.find_element(By.ID, f"seller_name_{item_id}").text.strip()
    phone_number = driver.find_element(By.ID, f"phone_number_{item_id}").text.strip()

    return seller_name, phone_number


# pylint: disable=too-many-locals
def scrape_data(driver):  # pylint: disable=redefined-outer-name
    scrape_result: list[FeedItem] = []
    # Wait for the page to load
    # Sometimes a captcha might appear and this command will timeout
    WebDriverWait(driver, 45).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "feed_item"))
    )

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all elements with class name "feed_item"
    # TODO: also feed_item_platinum
    # TODO: use Selenium instead of BS?
    feed_items = soup.find_all(class_="feed_item feed_item-v4 accordion desktop")

    for feed_item in feed_items:
        feed_item_element_id = feed_item.get("id")
        item_id = feed_item.get("id", "").split("_")[-1]  # Extract unique item ID

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, feed_item_element_id))
        )
        close_popup(driver)
        driver.find_element(by=By.ID, value=feed_item_element_id).click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, f"feed_item_{item_id}_title"))
        )

        address = scrape_address(feed_item, item_id)

        subtitle = feed_item.find("span", {"class": "subtitle"}).text.strip()
        estate_type = subtitle.split(",")[0]
        rooms = soup.find("span", {"id": f"data_rooms_{item_id}"}).text.strip()
        square_meter = soup.find(
            "span", {"id": f"data_SquareMeter_{item_id}"}
        ).text.strip()
        price = soup.find("div", {"id": f"feed_item_{item_id}_price"}).text.strip()
        updated_date = soup.find(
            "span", {"id": f"feed_item_{item_id}_date"}
        ).text.strip()

        seller_name, phone_number = scrape_seller_details(driver, item_id)

        # description = feed_item.find(
        #     "div", {"class": "show-more-contents"}
        # ).text.strip()

        feed_item_result = FeedItem(
            seller_name=seller_name,
            seller_phone_number=phone_number,
            address=address,
            estate_type=estate_type,
            rooms=rooms,
            square_meter=square_meter,
            price=price,
            updated_date=updated_date,
            # description=description,
        )

        print(feed_item_result)

        scrape_result.append(feed_item_result)

        # TODO: This doesn't close the feed item for some reason
        # driver.find_element(by=By.ID, value=feed_item_element_id).click()

    driver.quit()
    return scrape_result


if __name__ == "__main__":
    # Initialize WebDriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    SEARCH_URL = "https://www.yad2.co.il/realestate/forsale?topArea=2&area=11&city=6600&propertyGroup=apartments,houses&property=1,39,5&price=-1-2300000"  # pylint: disable=line-too-long
    driver.get(SEARCH_URL)

    res = scrape_data(driver)

    print(res)
