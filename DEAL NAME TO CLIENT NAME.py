import pandas as pd

# Load the Excel files
file1 = r"Downloads/Deal Name 1.xlsx"  # Replace with your first file name
file2 = r"Downloads/Client Name.xlsx"  # Replace with your second file name

# Read the data
df1 = pd.read_excel(file1)  # File 1 with Deal Name and Deal Owner
df2 = pd.read_excel(file2)  # File 2 with Client Name



# Ensure the column names match your file structure
deal_name_col = "Deal Name"  # Replace with actual column name in file 1
client_name_col = "Client Name"  # Replace with actual column name in file 2

# Drop rows with NaN in the relevant columns
df1 = df1.dropna(subset=[deal_name_col])
df2 = df2.dropna(subset=[client_name_col])


# Helper function to calculate match score
def get_match_score(client_phrases, deal_phrases):
    return len(client_phrases.intersection(deal_phrases))

# Define the function for matching
def find_deal_name(client_name):
    if pd.isna(client_name) or not isinstance(client_name, str):
        return None  # Skip if client_name is invalid
    
    # Step 1: Check for exact match
    for _, row in df1.iterrows():
        if client_name.strip().lower() == str(row[deal_name_col]).strip().lower():
            return row[deal_name_col]  # Return Deal Owner if exact match is found
    
    # Step 2: Check for maximum phrase match
    client_phrases = set(client_name.split())  # Split client name into unique phrases
    max_score = 0
    best_match = None
    for _, row in df1.iterrows():
        deal_name_phrases = set(str(row[deal_name_col]).split())  # Split deal name into unique phrases
        match_score = get_match_score(client_phrases, deal_name_phrases)
        if match_score > max_score:  # Update best match if a higher score is found
            max_score = match_score
            best_match = row[deal_name_col]
    print(f"Processing client: {client_name}, Max Match: {best_match}")

    return best_match  # Return the best match based on maximum phrase match


df2["Deal Name"] = df2[client_name_col].apply(find_deal_name)

# Save the updated DataFrame to a new Excel file
output_file = "output.xlsx"
df2.to_excel(output_file, index=False)

print(f"Updated file saved as {output_file}")



