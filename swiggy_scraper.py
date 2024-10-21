from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

# Install and set up WebDriver using webdriver-manager
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Swiggy Instamart URL
url = 'https://www.swiggy.com/instamart/'

# Visit the Swiggy Instamart page
driver.get(url)

# Let the page load completely
time.sleep(5)  # Adjust sleep time if needed

# Get the page content
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

# Close the browser after scraping
driver.quit()

# Define the output structure
data = {
    "categories": [],
    "products": []
}

# Define the categories of interest directly
categories_of_interest = ["Fresh Vegetables", "Fruits"]

# Define example categories and products
example_categories = {
    "Fresh Vegetables": [
        {
            "_id": 1,
            "name": "Carrots",
            "subcategories": [
                {"_id": 1, "name": "Organic Carrots"},
                {"_id": 2, "name": "Regular Carrots"}
            ]
        },
        {
            "_id": 2,
            "name": "Tomatoes",
            "subcategories": [
                {"_id": 1, "name": "Cherry Tomatoes"},
                {"_id": 2, "name": "Regular Tomatoes"}
            ]
        }
    ],
    "Fruits": [
        {
            "_id": 1,
            "name": "Apples",
            "subcategories": [
                {"_id": 1, "name": "Fuji Apples"},
                {"_id": 2, "name": "Gala Apples"}
            ]
        },
        {
            "_id": 2,
            "name": "Bananas",
            "subcategories": [
                {"_id": 1, "name": "Organic Bananas"},
                {"_id": 2, "name": "Regular Bananas"}
            ]
        }
    ]
}

# Populate categories directly
for idx, (category_name, subcategories) in enumerate(example_categories.items()):
    data["categories"].append({
        "_id": idx + 1,
        "name": category_name,
        "subcategories": subcategories
    })

# Example: Parsing product information (with hypothetical class names)
products = soup.find_all('div', class_='sc-1f5f3kl-0 iAykPa')  # Replace with the actual product class name
for prod_idx, product in enumerate(products):
    product_name = product.find('h3', class_='sc-1s5afm4-0 hcrqyz').text.strip()  # Replace with the actual product title class name
    product_url = product.find('a', class_='sc-1f5f3kl-2 cfrSOg')['href']  # Replace with the actual product link class name
    image_url = product.find('img', class_='sc-1s5afm4-1 iZuZKz')['src']  # Replace with the actual product image class name
    price = float(product.find('span', class_='sc-1s5afm4-2 iCfqbH').text.strip().replace('₹', '').replace(',', '').strip())  # Replace with the actual price class name
    measurement_value = product.find('span', class_='sc-1s5afm4-3 hMrCyb').text.strip()  # Replace with the actual measurement class name

    # Determine subcategory ID based on product name and subcategory matches
    subcategory_id = None
    for category in data["categories"]:
        for subcategory in category["subcategories"]:
            if subcategory["name"].lower() in product_name.lower():
                subcategory_id = subcategory["_id"]
                break
        if subcategory_id:
            break
    
    # Add to product list only if it's from the selected categories
    if subcategory_id is not None:
        data["products"].append({
            "_id": prod_idx + 1,
            "name": product_name,
            "product_url": product_url,
            "image_url": image_url,
            "price": price,
            "measurement": {
                "value": measurement_value,
                "unit": "Pcs"  # Adjust based on actual product data
            },
            "manufacturer": "Eco Farms",  # Adjust based on actual scraped data
            "subcategory_id": subcategory_id
        })

# Write the data to a JSON file
with open('instamart_fresh_vegetables_fruits.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

print("Scraping complete! Data saved to instamart_fresh_vegetables_fruits.json")
