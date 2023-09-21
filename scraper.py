from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def close_popup(driver):  # pylint: disable=redefined-outer-name
    try:
        popup_button = driver.find_element(
            by=By.CSS_SELECTOR, value="#overlay_comp > section > div > button"
        )
        if popup_button:
            popup_button.click()
    except NoSuchElementException:
        pass


# Initialize WebDriver
driver = webdriver.Chrome()

# Navigate to the URL
SEARCH_URL = "https://www.yad2.co.il/realestate/forsale?topArea=2&area=11&city=6600&propertyGroup=apartments,houses&property=1,39,5&price=-1-2300000"  # pylint: disable=line-too-long
driver.get(SEARCH_URL)

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

    driver.find_element(by=By.ID, value=feed_item_element_id).click()
    CONTACT_SELLER_CSS_SELECTOR = f"#contact_seller_{item_id} > button"

    # Wait for the button to be visible
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CONTACT_SELLER_CSS_SELECTOR))
    )

    # Locate and click the 'contact_seller' button
    contact_seller_button = driver.find_element(
        By.CSS_SELECTOR,
        CONTACT_SELLER_CSS_SELECTOR,
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

    print(f"Seller Name: {seller_name}")
    print(f"Phone Number: {phone_number}")

    # TODO: This doesn't close the feed item for some reason
    # driver.find_element(by=By.ID, value=feed_item_element_id).click()


driver.quit()
