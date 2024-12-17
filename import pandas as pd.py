import pandas as pd

# Specify the path to your original Excel file
input_excel_file = r"C:\Users\User\Downloads\Skype Download\Target All Collection Data - COL Final.xlsx"

# Specify the path for the new Excel file
output_excel_file = r"C:\Users\User\Downloads\Documents\Outputdata.xlsx"

# Load the original Excel file
xls = pd.ExcelFile(input_excel_file)

# Create a writer for the new Excel file
with pd.ExcelWriter(output_excel_file) as writer:
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_excel_file, sheet_name=sheet_name)
        
        # Extract the first column (assuming the first column is the index 0)
        first_column_data = df.iloc[:, 0].tolist()
        
        # Create a new DataFrame with the first column data
        new_df = pd.DataFrame({sheet_name: first_column_data})
        
        # Write the new DataFrame to the new Excel file
        new_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Data has been saved to {output_excel_file}")
