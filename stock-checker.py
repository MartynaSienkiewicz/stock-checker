import time
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Config
URL = '<replace with URL for the item here>'
CHROME_EXECUTABLE_PATH = r'<replace with PATH to your Chrome executable>'  # path to Chrome executable
CHROME_DRIVER_PATH = r'<replace with PATH to ChromeDriver>'                # path to ChromeDriver
CHECK_INTERVAL = 120  # 2 minutes in seconds (adjust this interval if want to check more frequently)
TELEGRAM_TOKEN = '<replace with your Telegram token>'  
TELEGRAM_CHAT_ID = '<replace with your Telegram chat ID>'  

# Set up logging
logging.basicConfig(filename='stock-checker.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.binary_location = CHROME_EXECUTABLE_PATH  # Tell Selenium to use this Chrome version
chrome_options.add_argument("--headless")                # Run in headless mode (no GUI) -- disable for debugging
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create the Selenium WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to send a Telegram notification
def send_telegram_notification(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logging.info("Notification sent successfully")
        else:
            logging.error(f"Failed to send notification: {response.text}")
    except Exception as e:
        logging.error(f"Error sending Telegram notification: {e}")

# Function to check stock availability
def check_stock():
    try:
        driver.get(URL)

        # Find the item elements that reflect the item's stock status, use a web browser and the inspector tool to find them
        # In this case, code finds a button for a specific item size and clicks it. Adjust this part of the code based on your item
        try:
            size_element = driver.find_element(By.CSS_SELECTOR, '<replace with the required CSS Selector>')
            size_element.click()  # Simulate clicking on the size button
            logging.info("Clicked <item> button")
        except Exception as e:
            logging.warning("Size <item size> button not found or could not be clicked.")

        # In this case, when the size element is pressed, out of stock text appears. Use this to determine item stock status
        try:
            logging.info("Waiting for stock status to appear...")
            stock_status = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '<replace with CSS Selector for out of stock text>'))  # Out of stock selector
            )

            # Check if the text contains "out of stock"
            if "out of stock" in stock_status.text.lower():
                logging.info(f"Checked at {time.strftime('%Y-%m-%d %H:%M:%S')}: Size 6 is out of stock")
                return False
            else:
                logging.info(f"Checked at {time.strftime('%Y-%m-%d %H:%M:%S')}: Size 6 is IN STOCK")
                send_telegram_notification(f"Size 6 jeans IN STOCK {URL}")
                return True
        except Exception as e:
            logging.error(f"Error while checking stock status: {e}")
            print(driver.page_source)
            return False

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return False

# Main loop
if __name__ == "__main__":
    try:
        while True:  # Keep running until the item is in stock
            item_in_stock = check_stock()

            # If the item is in stock, break the loop
            if item_in_stock:
                break

            # If the item is not in stock, wait for the defined interval and then check again
            time.sleep(CHECK_INTERVAL)  

    finally:
        driver.quit() 
