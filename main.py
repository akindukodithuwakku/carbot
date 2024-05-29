import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to fetch the HTML content from
url = 'https://riyasewana.com/search/cars/toyota/axio'

# Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Make an HTTP GET request to fetch the HTML content
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    data = {
        'Name': [],
        'Location': [],
        'Price': [],
        'Mileage': [],
        'Link': []
    }

    # Find all elements with class "item round"
    for elements in soup.find_all(class_="item round"):
        # Name of the vehicle
        name = elements.find('h2', class_='more').a.text
        data['Name'].append(name)

        # Location of the vehicle
        location = elements.find("div", class_="boxintxt").text.strip()
        data['Location'].append(location)

        # Price for the vehicle
        price_text = elements.find("div", class_="boxintxt b").text.strip()
        if "negotiable" in price_text.lower():
            price = None
        else:
            try:
                price = float(price_text.replace('Rs.', '').replace(',', '').strip())
            except ValueError:
                price = None
        data['Price'].append(price)

        # Mileage of the vehicle
        boxintxt_divs = elements.find_all('div', class_='boxintxt')
        mileage_text = boxintxt_divs[2].text.strip() if len(boxintxt_divs) > 2 else '0 km'
        if '(km)' in mileage_text:
            mileage = int(mileage_text.replace('(km)', '').replace(',', '').strip())
        else:
            mileage = 0  # Default to 0 if no mileage is found
        data['Mileage'].append(mileage)

        # Link for the vehicle
        link = elements.find('h2', class_='more').a['href']
        data['Link'].append(link)

    # Create DataFrame
    df = pd.DataFrame(data)
    print(df)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def plot_data():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Mileage'], df['Price'])
    ax.set_xlabel('Mileage (km)')
    ax.set_ylabel('Price (Rs.)')
    ax.set_title('Price vs Mileage for Vehicles')

    # Integrate plot with Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Tkinter setup
root = tk.Tk()
root.title('Vehicle Data Plot')

# Plot Button
plot_button = tk.Button(root, text='Plot Data', command=plot_data)
plot_button.pack()

# Start Tkinter main loop
root.mainloop()
