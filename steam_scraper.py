from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_all_steam_game_prices(game_name):
    driver = webdriver.Chrome()

    try:
        driver.get('https://store.steampowered.com/')

        # Locate the search box
        search_box = driver.find_element(By.ID, 'store_nav_search_term')
        search_box.send_keys(game_name)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.search_result_row'))
        )

        # Click the first result (most relevant)
        first_result = driver.find_element(By.CSS_SELECTOR, '.search_result_row')
        first_result.click()

        # Check if the Age-Check page appears
        try:
            age_check_header = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.agegate_birthday_desc'))
            )
            # Age-check page detected, set the birthdate
            day_select = Select(driver.find_element(By.ID, 'ageDay'))
            month_select = Select(driver.find_element(By.ID, 'ageMonth'))
            year_select = Select(driver.find_element(By.ID, 'ageYear'))

            day_select.select_by_value('21')
            month_select.select_by_value('December')
            year_select.select_by_value('2002')

            # Submit the form
            view_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#view_product_page_btn'))
            )
            view_page_button.click()

        except TimeoutException:
            # If no age-check page, continue to the price extraction
            pass

        # Ensure we're on the correct game page by waiting for a specific game page element
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.game_area_purchase_game'))
            )

            # Find all purchase options
            purchase_options = driver.find_elements(By.CSS_SELECTOR, '.game_area_purchase_game')
            # Prepare a list to hold all the purchase details
            game_prices = []

            for option in purchase_options:
                try:
                    # Get the title of the purchase option
                    option_title_element = option.find_element(By.CSS_SELECTOR, 'h1, h2, .package_title')
                    option_title = option_title_element.text.strip() if option_title_element else None

                    # Find the price elements within this option
                    try:
                        price_element = option.find_element(By.CSS_SELECTOR, '.game_purchase_price, .discount_final_price')
                        price = price_element.text.strip() if price_element else None
                    except NoSuchElementException:
                        price = None

                    try:
                        original_price_element = option.find_element(By.CSS_SELECTOR, '.discount_original_price')
                        original_price = original_price_element.text.strip() if original_price_element else price
                    except NoSuchElementException:
                        original_price = price

                    # Store the details in a dictionary
                    if original_price and option_title:
                        purchase_details = {
                            "title": option_title,
                            "saleprice": price,
                            "originalprice": original_price,
                        }

                    # Add this purchase option's details to the list
                        game_prices.append(purchase_details)

                except Exception as e:
                    print(f"Error extracting details for an option: {e}")
                    continue

            return game_prices

        except TimeoutException:
            return "No purchase options found or the page didn't load correctly within the timeout period."

    finally:
        driver.quit()

# Example usage:
if __name__ == "__main__":
    game_name = "Cyberpunk"
    game_prices = get_all_steam_game_prices(game_name)
    print(game_prices)