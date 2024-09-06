from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def get_all_epic_game_prices(game_name):
    # Setup Chrome driver
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run in headless mode (without opening the browser window)
    driver = webdriver.Chrome()
    
    try:
        # Navigate to Epic Games Store website
        driver.get('https://store.epicgames.com/en-US/')

        # Locate the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Search store"]'))
        )
        search_box.click()
        search_box.send_keys(game_name)
        search_box.send_keys(Keys.ENTER)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-component="SearchResults"] a'))
        )

        # Click the first search result
        first_result = driver.find_element(By.CSS_SELECTOR, 'div[data-component="SearchResults"] a')
        first_result.click()

        # Wait for the game page to load
        game_title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.css-1whxh4i'))
        )
        game_title = game_title_element.text.strip()

        # Extract the price information
        price_element = driver.find_element(By.CSS_SELECTOR, 'div[data-component="DisplayPrice"]')
        price = price_element.text.strip() if price_element else "No price available"

        # Check for any discount information
        original_price_element = driver.find_elements(By.CSS_SELECTOR, 'div[data-component="OriginalPrice"]')
        discount_element = driver.find_elements(By.CSS_SELECTOR, 'div[data-component="DiscountedPrice"]')

        original_price = original_price_element[0].text.strip() if original_price_element else price
        discount = discount_element[0].text.strip() if discount_element else "N/A"

        # Prepare the game price details
        game_price_details = [{
            "title": game_title,
            "price": price,
            "original_price": original_price,
            "discount": discount if discount != price else "N/A"
        }]
        
        return game_price_details

    except TimeoutException:
        return "Failed to retrieve the game's price or the page didn't load correctly within the timeout period."

    finally:
        driver.quit()