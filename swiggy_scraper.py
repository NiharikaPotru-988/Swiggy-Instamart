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

# Swiggy Instamart URL (replace with actual category URLs if needed)
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

# Example: Parsing categories and subcategories (adjust based on actual page structure)
categories = soup.find_all('div', class_='category-class')  # Adjust the selector for categories
for idx, category in enumerate(categories):
    category_name = category.find('h2').text.strip()  # Adjust to get category name
    subcategories = category.find_all('div', class_='subcategory-class')  # Adjust selector for subcategories
    
    subcat_data = []
    for sub_idx, subcategory in enumerate(subcategories):
        subcat_name = subcategory.text.strip()
        subcat_data.append({
            "_id": sub_idx + 1,
            "name": subcat_name
        })
    
    data["categories"].append({
        "_id": idx + 1,
        "name": category_name,
        "subcategories": subcat_data
    })

# Example: Parsing product information (adjust selectors based on actual structure)
products = soup.find_all('div', class_='product-class')  # Adjust selector for products
for prod_idx, product in enumerate(products):
    product_name = product.find('h3', class_='product-title-class').text.strip()  # Adjust selector
    product_url = product.find('a', class_='product-link-class')['href']  # Adjust selector
    image_url = product.find('img', class_='product-image-class')['src']  # Adjust selector
    price = float(product.find('span', class_='price-class').text.strip())  # Adjust selector
    measurement_value = product.find('span', class_='measurement-class').text.strip()  # Adjust selector
    
    # Example subcategory ID (you'll need to adjust this based on actual data structure)
    subcategory_id = 6  # Adjust as necessary
    
    # Add to product list
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
with open('instamart_products.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

print("Scraping complete! Data saved to instamart_products.json")
