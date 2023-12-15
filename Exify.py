import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_html_with_crawlbase(url, token):
    api_url = f'https://api.crawlbase.com/?token=azxyXSavgH1TA3YFDTn9cg&url=https%3A%2F%2Fgithub.com%2Fcrawlbase-source%3Ftab%3Drepositories'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def parse_flight_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    flight_rows = soup.find_all('div', class_='inner-grid  keel-grid')
    prices = []
    airlines = []

    for row in flight_rows:
        # Scrape price
        t_price = row.find("div", class_="f8F1-price-text-container")
        price = t_price.find("span", class_="f8F1-price-text").text if t_price else "N/A"
        prices.append(price)
        
        # Scrape airline
        t_airline = row.find("div", class_="J0g6-labels-grp")
        airline = t_airline.find("span", class_="J0g6-operator-text").text if t_airline else "N/A"
        airlines.append(airline)

    return prices, airlines

if __name__ == '__main__':
    token = 'your_crawlbase_token_here'  # Replace with your actual token
    start_airports = ['KRK', 'WAW', 'WMI']
    destination_airport = 'CTU'
    date = '2023-12-15'
    
    all_prices = []
    all_airlines = []

    for start_airport in start_airports:
        url = f'https://www.kayak.sg/flights/{start_airport}-{destination_airport}/{date}-flexible-3days'
        html = fetch_html_with_crawlbase(url, token)
        if html:
            prices, airlines = parse_flight_data(html)
            all_prices.extend(prices)
            all_airlines.extend(airlines)

    df = pd.DataFrame({
        'Price': all_prices,
        'Airline': all_airlines
    })

    df.to_csv('flight_data.csv', index=False)
