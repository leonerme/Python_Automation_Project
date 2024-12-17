import pandas as pd

# Specify the path to your original Excel file
input_excel_file = r"C:\Users\User\Downloads\Chrome Download\Target Items.xlsx"

# Specify the path for the new Excel file
output_excel_file = r"C:\Users\User\Downloads\Chrome Download\Target items all.xlsx"

# Read all sheets into a dictionary
xls = pd.ExcelFile(input_excel_file)
all_data = {}

for sheet_name in xls.sheet_names:
    df = pd.read_excel(input_excel_file, sheet_name=sheet_name)
    all_data[sheet_name] = df

# Combine data from all sheets into a single DataFrame
combined_data = pd.concat(all_data, axis=0, ignore_index=True)

# Write the combined data to a new Excel file
combined_data.to_excel(output_excel_file, index=False)

print(f"Combined data has been saved to {output_excel_file}")
