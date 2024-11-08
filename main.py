# Import Libraries 
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Set up the ChromeDriver path
driver_path = "chromedriver.exe"
service = Service(driver_path)

# Configure options for Selenium WebDriver
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the Amazon page
url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
driver.get(url)
time.sleep(random.uniform(3, 6))  # Random delay to behave like  human browsing

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract product data
products = []
for product in soup.find_all("div", {"class": "s-result-item"}):
    # Print the HTML structure of each product for debugging
    print(product.prettify())
    
    # Attempt to extract product name s
    name_tag = product.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
    if not name_tag:
        name_tag = product.find("span", {"class": "a-size-base-plus"})  # Alternative selector
    name = name_tag.text.strip() if name_tag else "N/A"

    # Extract price
    price_tag = product.find("span", {"class": "a-price-whole"})
    price = price_tag.text.replace(",", "") if price_tag else "N/A"

    # Extract rating
    rating_tag = product.find("span", {"class": "a-icon-alt"})
    rating = rating_tag.text if rating_tag else "N/A"

    # Extract seller 
    seller_tag = product.find("span", {"class": "a-size-base-plus"})
    seller = seller_tag.text if seller_tag else "N/A"

    # Add extracted data in to the products list
    products.append({
        "Product Name": name,
        "Price": price,
        "Rating": rating,
        "Seller Name": seller
    })

    # Adding random delay between parsing each product
    time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds

# Save extracted data to a CSV file
df = pd.DataFrame(products)
df.to_csv("amazon_products.csv", index=False)

# Close the WebDriver
driver.quit()
