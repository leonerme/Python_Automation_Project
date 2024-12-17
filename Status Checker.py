import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Initialize a web driver (you need to download and configure the appropriate driver for your browser)
driver = webdriver.Chrome(executable_path= r"C:\Users\User\Downloads\Compressed\chromedriver-win64\chrome.exe")

# Load the Excel file
excel_file_path = "product_ids.xlsx"  # Replace with the path to your Excel file
df = pd.read_excel(excel_file_path)

# Define the function to fetch the product status
def fetch_product_status(product_id):
    driver.get(url)
    
    # Find the search input field and enter the product ID
    search_input = driver.find_element_by_name("search")  # Replace with the actual name of the search input field
    search_input.clear()
    search_input.send_keys(product_id)
    search_input.send_keys(Keys.RETURN)
    
    # Wait for the search results to load (you may need to adjust the sleep time)
    time.sleep(2)
    
    # Parse the HTML of the search results page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract the product status from the parsed HTML
    # You'll need to inspect the website's HTML structure to locate the relevant element
    status_element = soup.find("div", class_="product-status")  # Replace with the actual element that contains the status
    
    if status_element:
        product_status = status_element.text.strip()
    else:
        product_status = "Status not found"
    
    return product_status

# Website URL to scrape
url = "https://example.com"  # Replace with the actual website URL

# Create a new column to store the product statuses
df['Product Status'] = df['Product ID'].apply(fetch_product_status)

# Save the updated Excel file
output_file_path = "product_ids_with_status.xlsx"  # Replace with the desired output file path
df.to_excel(output_file_path, index=False)

# Close the web driver
driver.quit()

print(f"Product statuses have been written to {output_file_path}")
