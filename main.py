import requests
from bs4 import BeautifulSoup

# URL to fetch the HTML content from
url = 'https://riyasewana.com/search/cars/toyota/axio'

# Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Make an HTTP GET request to fetch the HTML content
response = requests.get(url , headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content , 'html.parser')

    links_for_vehicle = []
    name_of_vehicle = []
    prices = []
    mileage_of_vehicle = []
    vehicle_location = []

    # Find all elements with class "item round"
    for elements in soup.find_all(class_="item round"):
        # 1. Name of the vehicle
        name = elements.find('h2' , class_='more').a.text
        name_of_vehicle.append(name)

        # 2. Location of the vehicle
        location = elements.find("div" , class_="boxintxt").text.strip()
        vehicle_location.append(location)

        # 3. Price for the vehicle
        price_text = elements.find("div" , class_="boxintxt b").text.strip()
        if "negotiable" in price_text.lower():
            price = 0
        else:
            try:
                price = float(price_text.replace('Rs.' , '').replace(',' , '').strip())
            except ValueError:
                price = 0
        prices.append(price)

        # 4. Mileage of the vehicle
        boxintxt_divs = elements.find_all('div' , class_='boxintxt')
        mileage_text = boxintxt_divs[2].text.strip() if len(boxintxt_divs) > 2 else '0 km'
        if '(km)' in mileage_text:
            mileage = int(mileage_text.replace('(km)' , '').strip())
        else:
            mileage = 0  # Default to 0 if no mileage is found
        mileage_of_vehicle.append(mileage)

        # 5. Link for the vehicle
        link = elements.find('h2' , class_='more').a['href']
        links_for_vehicle.append(link)

    # Find the index of the maximum mileage
    max_prices = prices.index(max(prices))

    # Print the details of the vehicle with the maximum mileage
    print(f"{name_of_vehicle[max_prices]}, price: {prices[max_prices]}, "
          f"location: {vehicle_location[max_prices]}, link: {links_for_vehicle[max_prices]}, "
          f"mileage: {mileage_of_vehicle[max_prices]} km")


    print(links_for_vehicle)
    print(name_of_vehicle)
    print(mileage_of_vehicle)
    print(prices)
    print(vehicle_location)



else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")





