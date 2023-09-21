from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize WebDriver
driver = webdriver.Chrome()

# Navigate to the URL
SEARCH_URL = "https://www.yad2.co.il/realestate/forsale?topArea=2&area=11&city=6600&propertyGroup=apartments,houses&property=1,39,5&price=-1-2300000"  # pylint: disable=line-too-long
driver.get(SEARCH_URL)

# Wait for the page to load
# Sometimes a captcha might appear and this command will timeout
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "feed_item"))
)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all elements with class name "feed_item"
feed_items = soup.find_all(class_="feed_item feed_item-v4 accordion desktop")

for feed_item in feed_items:
    feed_item_element_id = feed_item.get("id")
    item_id = feed_item.get("id", "").split("_")[-1]  # Extract unique item ID

    driver.find_element(by=By.ID, value=feed_item_element_id).click()

    CONTACT_SELLER_CSS_SELECTOR = f"#contact_seller_{item_id} > button"

    # Wait for the button to be visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CONTACT_SELLER_CSS_SELECTOR))
    )

    # Locate and click the 'contact_seller' button
    contact_seller_button = driver.find_element(
        By.CSS_SELECTOR,
        CONTACT_SELLER_CSS_SELECTOR,
    )
    contact_seller_button.click()

    # Wait for the popup to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, f"seller_name_{item_id}"))
    )

    # Parse the popup details
    # TODO: use the already initialized soup object
    popup_soup = BeautifulSoup(driver.page_source, "html.parser")
    seller_name = popup_soup.find("div", {"id": f"seller_name_{item_id}"}).text.strip()

    phone_number_element = driver.find_element(By.ID, f"phone_number_{item_id}")
    phone_number = phone_number_element.find_element(By.TAG_NAME, "a").text

    # phone_number = popup_soup.find(
    #     "div", {"id": f"phone_number_{item_id}"}
    # ).text.strip()

    print(f"Seller Name: {seller_name}")
    print(f"Phone Number: {phone_number}")

    # This one doesn't close the feed item
    driver.find_element(by=By.ID, value=feed_item_element_id).click()


driver.quit()
