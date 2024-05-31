import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"

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
                price = int(price_text.replace('Rs.', '').replace(',', '').strip())
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


#price calculations

price_list = []
def highest():
    pass
    # maxPrice = max(price)
    # new_window = Canvas(window, width=200, height=200)
    # results = Label(new_window, text="", font=(16))
    # results.grid(column=0, row=1, pady=10)
    #
    # results.config(text=f"{maxPrice}")
    #
    # exit_button = Button(window , text="Back" , font=("Helvetica" , 14) , bg="#f44336" , fg="white" ,
    #                      command=window.quit)
    # exit_button.grid(column=0 , row=2 , columnspan=3 , pady=10)


def lowest():
   pass



# ui creation
from tkinter import Tk, Label, Canvas, Entry, Button, Frame

# Define background color
BACKGROUND_COLOR = "#f0f0f0"

# Initialize the main window
window = Tk()
window.title("Car Price Analyzer")
window.config(pady=20, padx=20, bg=BACKGROUND_COLOR)

# Title label
title = Label(window, text="Find Your Dream Vehicle", font=("Helvetica", 24, "bold"), bg=BACKGROUND_COLOR)
title.grid(column=0, row=0, columnspan=3, pady=10)

# Create a frame for the car name entry
entry_frame = Frame(window, bg=BACKGROUND_COLOR)
entry_frame.grid(column=0, row=1, columnspan=3, pady=10)

car_name_label = Label(entry_frame, text="Enter Car Name:", font=("Helvetica", 14), bg=BACKGROUND_COLOR)
car_name_label.pack(side="left", padx=5)

car_name_entry = Entry(entry_frame, font=("Helvetica", 14), width=20)
car_name_entry.pack(side="left", padx=5)

# Canvas for image or other content
canvas = Canvas(window, height=300, width=300, bg="white")
canvas.grid(column=0, row=2, columnspan=3, pady=10)

# Create a frame for price information
price_frame = Frame(window, bg=BACKGROUND_COLOR)
price_frame.grid(column=0, row=3, columnspan=3, pady=10)

price_label = Label(price_frame, text="Price: ", font=("Helvetica", 14), bg=BACKGROUND_COLOR)
price_label.grid(column=0, row=0, padx=10)

Checkbutton(price_frame, text='Lowest', variable=lowest()).grid( column=1,row=0, padx=10)
Checkbutton(price_frame, text='Highest', variable=highest()).grid(column=2, row=0, padx=10)


# Search button
search_button = Button(window, text="Search", width=20, height=2, font=("Helvetica", 14), bg="#4CAF50", fg="white")
search_button.grid(column=0, row=4, columnspan=3, pady=10)

# Price plot section
price_plot_label = Label(window, text="Price vs Kms' Graphs", font=("Helvetica", 14, "bold"), bg=BACKGROUND_COLOR)
price_plot_label.grid(column=0, row=5, columnspan=3, pady=10)

price_plot_btn = Button(window, text="See Plot", font=("Helvetica", 14), bg="#2196F3", fg="white")
price_plot_btn.grid(column=0, row=6, columnspan=3, pady=10)

# Exit button
exit_button = Button(window, text="Exit", font=("Helvetica", 14), bg="#f44336", fg="white", command=window.quit)
exit_button.grid(column=0, row=7, columnspan=3, pady=10)

# Run the application
window.mainloop()


