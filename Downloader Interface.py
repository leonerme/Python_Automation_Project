import os
import requests
import pandas as pd
import urllib.parse
import tkinter as tk
from tkinter import filedialog
#from tkinter import messagebox
from tkinter import ttk
from tqdm import tqdm
import threading
import shutil

# Function to sanitize a string to make it a valid filename
def sanitize_filename(name):
    return "".join(
        c if c.isalnum() or c in [".", "-", "_", " ", "~"] else "_"
        for c in name
    )


def download_and_rename_image(url, name, save_dir, progress_bar, error_log):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        if total_size == 0:
            raise Exception("File size is zero.")

        # Create a temporary file for downloading
        temp_file = os.path.join(save_dir, "temp_download")
        with open(temp_file, "wb") as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as t:
                for data in response.iter_content(chunk_size=1024):
                    t.update(len(data))
                    file.write(data)

        # Get the file extension from the URL
        file_extension = url.split(".")[-1]
        use_extension = ""
        if file_extension == "jpg" or file_extension == "jpeg":
            use_extension = file_extension
        else:
            use_extension = "jpg"


        # Create a file name by combining the new name and the file extension
        sanitized_name = sanitize_filename(name)
        filename = f"{sanitized_name}_1.{use_extension}"

        # Remove query parameters from the filename
        filename = urllib.parse.urlparse(filename).path

        # Replace characters that are not allowed in Windows filenames
        filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_').replace('?', '_')

        file_path = os.path.join(save_dir, filename)

        # Copy the temporary file to the final destination
        shutil.copy(temp_file, file_path)
        os.remove(temp_file)  # Remove the temporary file

        print(f"Downloaded and renamed: {filename}")
    except Exception as e:
        error_message = f"Error downloading image from {url}: {str(e)}"
        log_error(error_message)
        # Log the error
        error_log.append({"URL": url, "Error Message": error_message})

# Function to log information in the GUI
def log_info(message):
    text.config(state=tk.NORMAL)  # Allow text widget to be edited
    text.insert(tk.END, message + "\n")
    text.config(state=tk.DISABLED)  # Prevent further editing
    text.update()

# Function to log errors in the GUI
def log_error(error_message):
    log_info(error_message)  # Log the error as information
    # Show a messagebox with the error message
  #  messagebox.showerror("Error", error_message)

# Function to handle the download and logging
def download_images():
    log_info("Downloading images...")
    error_log = []

    # Read image data from an Excel file
    file_path = filedialog.askopenfilename(title="Select Excel File")
    if not file_path:
        log_error("No Excel file selected. Please choose a valid Excel file.")
        return

    df = pd.read_excel(file_path)

    # Choose the directory to save downloaded images
    save_dir = filedialog.askdirectory(title="Select Download Directory")
    if not save_dir:
        log_error("No download directory selected. Please choose a valid directory.")
        return

    # Create a directory to store the downloaded images if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    progress_bar["maximum"] = len(df)
    progress_bar["value"] = 0

    # Loop through the DataFrame and download/renaming each image
    for index, row in df.iterrows():
        url = row["ImageURL"]
        name = row["ImageName"]
        download_and_rename_image(url, name, save_dir, progress_bar, error_log)
        progress_bar.step(1)
        root.update_idletasks()

    log_info("Download completed.")

    # Save the error log to an Excel file
    error_df = pd.DataFrame(error_log)
    error_log_path = filedialog.asksaveasfilename(defaultextension=".xlsx", title="Save Error Log")
    if error_df.empty:
        log_info("No errors encountered.")
    else:
        error_df.to_excel(error_log_path, index=False)
        log_info(f"Error log saved to {error_log_path}")

# Create the main application window
root = tk.Tk()
root.title("Image Downloader")

# Create a text widget to display log messages
text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
text.pack()

# Create a progress bar to show download progress
progress_bar = ttk.Progressbar(root, mode="determinate")
progress_bar.pack()

# Create a button to start image download
download_button = tk.Button(root, text="Download Images", command=download_images)
download_button.pack()

root.mainloop()
