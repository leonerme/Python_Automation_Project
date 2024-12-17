import os
import io
import requests
from PIL import Image
import openpyxl

from tqdm import tqdm  # Import tqdm for the progress bar

def download_and_process_images(file_path, save_directory):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    headers = {cell.value: idx for idx, cell in enumerate(sheet[1], 1)}
    if "ebay URL" not in headers or "SKU" not in headers:
        raise ValueError("Excel file must have 'ebay UR' and 'SKU' columns.")
    url_col = headers["ebay URL"]
    sku_col = headers["SKU"]

    rows = list(sheet.iter_rows(min_row=2, values_only=True))  # Fetch all rows

    # Wrap the loop with tqdm to display progress
    for row in tqdm(rows, desc="Processing SKUs", unit="SKU"):
        url = row[url_col - 1]
        sku = row[sku_col - 1]

        if not url or not sku:
            continue

        folder_path = os.path.join(save_directory, sku)
        os.makedirs(folder_path, exist_ok=True)

        try:
            html_content = requests.get(url).text
            images = extract_image_urls(html_content)

            if not images:
                print(f"No high-resolution images found for SKU {sku}.")
                continue

            for i, img_url in enumerate(images):
                img_response = requests.get(img_url)
                img_response.raise_for_status()

                img = Image.open(io.BytesIO(img_response.content))
                img = img.convert("RGB")

                # Naming logic
                if i == 0:
                    suffix = "_Main"  # First image as main
                else:
                    suffix = f"_{i}"  # Sequential numbering

                image_name = f"{sku}{suffix}.jpg"
                img.save(os.path.join(folder_path, image_name), "JPEG")

        except Exception as e:
            print(f"Error processing SKU {sku}: {e}")


from bs4 import BeautifulSoup

def extract_image_urls(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    image_urls = []
    for img_tag in soup.find_all("img"):
        img_src = img_tag.get("src") or img_tag.get("data-src")
        if img_src and "ebayimg.com" in img_src:
            # Prioritize high-resolution images
            if "s-l1600" in img_src:
                image_urls.append(img_src)
    # Remove duplicates
    return list(set(image_urls))


if __name__ == "__main__":
    # Path to the Excel file
    excel_file = r"C:\Users\Qbits\Downloads\ebay image url.xlsx"
    # Directory to save images
    save_dir = r"C:\Users\Qbits\Downloads\ebay images"
    download_and_process_images(excel_file, save_dir)

