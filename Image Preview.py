import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv(r'D:\COL\Target Image\Autamation Scripts\Image_Url_preview.csv')

# Define the number of images to display per page
images_per_page = 10

# Generate an HTML file
html_content = '<!DOCTYPE html><html><head><title>Image URL Previews</title></head><body><h1>Image URL Previews</h1><table><thead><tr><th>SKU ID</th>'

# Generate table headers for image URLs
for i in range(1, min(12, len(df.columns))):
    html_content += f'<th>Image URL {i}</th>'

html_content += '</tr></thead><tbody>'

# Create rows for each SKU
for _, row in df.iterrows():
    html_content += '<tr>'
    html_content += f'<td>{row["SKU ID"]}</td>'
    
    # Display up to 11 image URLs per SKU (columns 2 to 12 in the CSV)
    for i in range(1, min(12, len(df.columns))):
        image_url = row[i]
        html_content += f'<td><img src="{image_url}" style="max-width: 120px; max-height: 120px;"></td>'
    
    html_content += '</tr>'

html_content += '</tbody></table></body></html>'

# Save the HTML content to a file
with open('image_previews.html', 'w') as f:
    f.write(html_content)
