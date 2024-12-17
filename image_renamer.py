import os
import openpyxl
import shutil

def find_and_copy_files(input_excel_path, input_folder_path, output_folder_path):
    # Load the Excel workbook
    workbook = openpyxl.load_workbook(input_excel_path)
    sheet = workbook.active

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder_path, exist_ok=True)

    for row in sheet.iter_rows(min_row=2, values_only=True):
        sku, search_value, rename_with = row

        # Find files in the input folder matching the search_value
        found_files = [f for f in os.listdir(input_folder_path) if search_value in f]

        # If files are found, copy and rename them
        if found_files:
            for i, file in enumerate(found_files, 1):
                new_filename = f"{rename_with}_{i}" if len(found_files) > 1 else rename_with

                # Copy the file to the output folder and rename it
                shutil.copy(os.path.join(input_folder_path, file), os.path.join(output_folder_path, new_filename))

if __name__ == "__main__":
    input_excel_path = r"C:\Users\User\Downloads\Target Image\Image Resizer\Rename.xlsx"
    input_folder_path = r"C:\Users\User\Downloads\Target Image\Image Resizer\Images"
    output_folder_path = r"C:\Users\User\Downloads\Target Image\Image Resizer\Renamd"

    find_and_copy_files(input_excel_path, input_folder_path, output_folder_path)
