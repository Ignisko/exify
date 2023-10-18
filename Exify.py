from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def start_web_driver():
    driver = webdriver.Chrome()
    print("WebDriver started.")
    return driver

def navigate_to_url(driver, start_airport, destination_airport='SIN', date='2023-12-15'):
    url = f'https://www.kayak.sg/flights/{start_airport}-{destination_airport}/{date}-flexible-3days'
    driver.get(url)
    sleep(5)

def scrape_data(driver):
    flight_rows = driver.find_elements_by_xpath('//div[@class="inner-grid  keel-grid"]')
    prices = []
    airlines = []

    for row in flight_rows:
        elementHTML = row.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        
        # Scrape price
        t_price = elementSoup.find("div", {"class": "f8F1-price-text-container"})
        if t_price:
            price = t_price.find("span", {"class": "f8F1-price-text"})
            if price:
                prices.append(price.text)
        
        # Scrape airline
        t_airline = elementSoup.find("div", {"class": "J0g6-labels-grp"})
        if t_airline:
            airline = t_airline.find("span", {"class": "J0g6-operator-text"})
            if airline:
                airlines.append(airline.text)

    return prices, airlines

if __name__ == '__main__':
    print("Starting script...")
    driver = start_web_driver()

    start_airports = ['KRK', 'WAW', 'WMI']
    destination_airport = 'CTU'
    
    # Initialize these lists to store all scraped data
    all_prices = []
    all_airlines = []

    for start_airport in start_airports:
        print(f"Trying for airport {start_airport}")
        navigate_to_url(driver, start_airport, destination_airport)
        
        # Scrape data for each airport
        prices, airlines = scrape_data(driver)
        print(f"Prices: {prices}")
        print(f"Airlines: {airlines}")

        # Extend the all_prices and all_airlines lists with newly scraped data
        all_prices.extend(prices)
        all_airlines.extend(airlines)

    # Create a DataFrame and save to CSV
    df = pd.DataFrame({
        'Price': all_prices,
        'Airline': all_airlines
    })

    df.to_csv('flight_data.csv', index=False)
    
    print("Exiting...")
    driver.quit()
