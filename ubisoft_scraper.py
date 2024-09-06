from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException,StaleElementReferenceException
import time

def get_all_ubisoft_game_prices(game_name):
    # Setup Chrome driver with options
    driver = webdriver.Chrome()

    try:
        # Navigate to Ubisoft Store website
        driver.get('https://store.ubisoft.com/ie/home?lang=en-ZW')

        # Accept cookies
        accept_cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'privacy__modal__accept'))
        )
        accept_cookies_button.click()

        # Locate the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.ais-SearchBox-input'))
        )
        search_box.click()
        search_box.send_keys(game_name)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.card-details'))
        )

        time.sleep(5)

        # Find all game tiles on the search result page
        tiles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.grid-tile.cell.shrink.algolia-producttile-card.tag-commander-event'))
        )

        # Prepare a list to hold game price details
        game_prices = []

        for tile in tiles:
            for attempt in range(2):  # Try twice before giving up
                try:
                    # Extract game title
                    try:
                        prod_title_elem = tile.find_element(By.CLASS_NAME, 'prod-title')
                        prod_title = prod_title_elem.text.strip() if prod_title_elem else None
                    except NoSuchElementException:
                        prod_title = None

                    # Extract sale price
                    try:
                        sale_price_elem = tile.find_element(By.CLASS_NAME, 'sale_price')
                        sale_price = sale_price_elem.text.strip() if sale_price_elem else None
                    except NoSuchElementException:
                        sale_price = None

                    # Extract original price (standard price)
                    try:
                        original_price_elem = tile.find_element(By.CLASS_NAME, 'standard-price')
                        original_price = original_price_elem.text.strip() if original_price_elem else None
                    except NoSuchElementException:
                        original_price = None

                    # Print each tile's details

                    # Store the details in a dictionary
                    if original_price and prod_title:
                        purchase_details = {
                            "title": prod_title,
                            "saleprice": sale_price,
                            "originalprice": original_price
                        }

                    # Add the purchase details to the list
                        game_prices.append(purchase_details)

                    break  # If no exception, break the retry loop

                except StaleElementReferenceException:
                    if attempt == 0:  # Retry only once
                        print(f"Stale element found, retrying: {tile}")
                        # Re-find the tile element
                        tile = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.grid-tile.cell.shrink.algolia-producttile-card.tag-commander-event'))
                        )
                    else:
                        print(f"Failed to process tile due to stale element: {tile}")

        return game_prices

    except TimeoutException:
        return "Failed to retrieve the game's price or the page didn't load correctly within the timeout period."
    finally:
        driver.quit()

# Example usage:
if __name__ == "__main__":
    game_name = "Assasins Creed Mirage Deluxe"
    game_prices = get_all_ubisoft_game_prices(game_name)
    print(game_prices)
