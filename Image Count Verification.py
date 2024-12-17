import os
import pandas as pd

# Function to get count of images in a folder
def get_image_count(folder_path, image_name, valid_extensions):
    # List all files in the folder that match the image name and have valid extensions
    matched_files = [f for f in os.listdir(folder_path) 
                     if f.startswith(image_name) and os.path.splitext(f)[1].lower() in valid_extensions]
    
    print(f"Checking image: {image_name} - Found {len(matched_files)} files in folder")
    
    return len(matched_files), matched_files

# Load the Excel file and compare image counts
def check_images_in_folder(excel_file, folder_path, output_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Initialize a list to store mismatched image names
    mismatched_images = []

    # Define valid image extensions
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    # Loop through each row in the Excel file
    for index, row in df.iterrows():
        image_name = row['Image Name']
        expected_count = row['Image Count']

        # Get actual image count from the folder
        actual_count, matched_files = get_image_count(folder_path, image_name, valid_extensions)

        # Check if the counts don't match
        if actual_count != expected_count:
            print(f"Mismatch for {image_name}: Expected {expected_count}, Found {actual_count}")
            
            # Store mismatched image names and their actual count
            mismatched_images.append({
                "Image Name": image_name,
                "File in Folder": ', '.join(matched_files),  # Join all matched files into a string
                "Folder Count": actual_count,
                "Expected Count": expected_count
            })

    # Check if there are mismatches and write to Excel if there are
    if mismatched_images:
        mismatched_df = pd.DataFrame(mismatched_images)
        
        # Save the mismatched images to an Excel file
        try:
            mismatched_df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Mismatch report saved to: {output_file}")
        except Exception as e:
            print(f"Error saving Excel file: {e}")
    else:
        print("No mismatches found. All counts match.")

# Example Usage
excel_file = r'D:\COL\COL SUBMISSIONs\RTD 9-23-24\Book1.xlsx'  # Path to your Excel file
folder_path = r'D:\COL\COL SUBMISSIONs\RTD 9-23-24\Images'  # Path to your folder containing images
output_file = 'mismatched_images.xlsx'  # Output Excel file to store mismatched images

check_images_in_folder(excel_file, folder_path, output_file)
