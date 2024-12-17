import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.title

        if title_tag is not None:
            return title_tag.string
        else:
            return "No title found"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching title for {url}: {e}")
        return None

def fetch_titles(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Add a new column for titles
    df['Title'] = df['URL'].apply(get_title)

    # Save the result to a new Excel file
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    input_excel_file = r"D:\COL\Versailles 1-14-24\URL Title.xlsx"  # Replace with your input file name
    output_excel_file = r"D:\COL\Versailles 1-14-24\output.xlsx"  # Replace with your desired output file name

    fetch_titles(input_excel_file, output_excel_file)
