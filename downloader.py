import os
import requests
import pandas as pd
import urllib.parse

# Function to sanitize a string to make it a valid filename
def sanitize_filename(name):
    return "".join(
        c if c.isalnum() or c in [".", "-", "_", " ", "~"] else "_" for c in name
    )

# Function to download an image from a URL and save it with a given name
def download_and_rename_image(url, new_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the file extension from the URL
            file_extension = url.split(".")[-1]
            # Create a file name by combining the new name and the file extension
            sanitized_name = sanitize_filename(new_name)
            filename = f"{sanitized_name}.{file_extension}"
            # Remove query parameters from the filename
            filename = urllib.parse.urlparse(filename).path
            file_path = os.path.join("downloaded_images", filename)
            # Write the image to a file
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded and renamed: {filename}")
        else:
            error_message = f"Failed to download image from {url}. Status code: {response.status_code}"
            print(error_message)
            # Log the error
            error_log.append({"URL": url, "Error Message": error_message})
    except Exception as e:
        error_message = f"Error downloading image from {url}: {str(e)}"
        print(error_message)
        # Log the error
        error_log.append({"URL": url, "Error Message": error_message})

# Read image data from an Excel file
df = pd.read_excel(r'D:\Target Image\Image Resizer\image_data 2.xlsx')  # Replace 'image_data.xlsx' with your Excel file name

# Create a directory to store the downloaded images if it doesn't exist
if not os.path.exists(r'C:\Users\User\Downloads\SA Image'):
    os.makedirs(r'C:\Users\User\Downloads\SA Image\New')


# Create an error log to store error data
error_log = []

# Loop through the DataFrame and download/renaming each image
for index, row in df.iterrows():
    url = row["ImageURL"]
    name = row["ImageName"]
    download_and_rename_image(url, name)

# Save the error log to an Excel file
error_df = pd.DataFrame(error_log)
error_df.to_excel("error_log.xlsx", index=False)
