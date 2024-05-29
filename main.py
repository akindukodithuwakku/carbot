import requests
from bs4 import BeautifulSoup

# URL to fetch the HTML content from
url = 'https://riyasewana.com/search/cars'

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
    milage_of_vehicle = []
    vehicle_location = []

    # Find all elements with class "item round"
    for elements in soup.find_all(class_="item round"):

        #  1   name of the vehicle
        name = elements.find('h2', class_='more').a.text
        name_of_vehicle.append(name)

        # 2  location of the vehicle
        location = elements.find("div" , class_="boxintxt").text.strip()
        vehicle_location.append(location)

        # 5 price for the vehicle
        price = elements.find("div" , class_="boxintxt b").text.strip()
        prices.append(price)


        # 3 milage of the vehicle
    for y in soup.findAll("div", class_="boxtext"):
            boxintxt_divs = y.find_all('div' , class_='boxintxt')
            mileage = boxintxt_divs[2].text.strip()
            milage_of_vehicle.append(mileage)

        # 4 link for the vehicle
    for x in soup.findAll("h2", class_="more"):
           links_for_vehicle.append(x.find("a")["href"])



    # Print the found elements
    for element in elements:
        print(links_for_vehicle)
        print(name_of_vehicle)
        print(milage_of_vehicle)
        print(prices)
        print(vehicle_location)






else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
