import os
import requests
import pandas as pd
import urllib.parse
import tkinter as tk
from tkinter import filedialog, ttk
from concurrent.futures import ThreadPoolExecutor
import threading
import mimetypes

# Function to sanitize a string to make it a valid filename
def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in [".", "-", "_", " ", "~"] else "_" for c in name)

def get_direct_url(url):
    """Modify URLs from certain hosts to get the actual image link."""
    if "dropbox.com" in url and "dl=0" in url:
        return url.replace("dl=0", "dl=1")  # Convert Dropbox links to direct download
    return url

#Function to Download Image
def download_image(url, name, save_dir, error_log):
    try:
        url = get_direct_url(url)  # Convert Dropbox URLs if needed
        response = requests.get(url, stream=True, timeout=10, allow_redirects=True)
        response.raise_for_status()

        # Extract content type to determine the file extension
        content_type = response.headers.get("Content-Type", "")
        file_extension = mimetypes.guess_extension(content_type.split(";")[0]) or ".jpg"

        # Ensure the file extension is valid
        if file_extension not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            file_extension = ".jpg"  # Default to JPG if unknown

        # Use the filename from the URL if available
        """filename = os.path.basename(url.split("?")[0])  # Remove query params
        if "." not in filename:  # If no valid extension, use the sanitized name
            filename = f"{sanitize_filename(name)}{file_extension}"""
        filename = f"{sanitize_filename(name)}{file_extension}"
        file_path = os.path.join(save_dir, filename)

        #file_path = os.path.join(save_dir, filename)

        # Save image directly to file
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        log_info(f"Downloaded: {filename}")
    except Exception as e:
        error_log.append({"SKU": filename, "URL": url, "Error": str(e)})
        log_info(f"Error downloading: {filename} URL: {url}: {e}")

# Function to log messages safely
def log_info(message):
    text.after(0, lambda: text.insert(tk.END, message + "\n"))
    text.after(0, text.yview_moveto, 1)

# Function to handle batch downloading
def start_download():
    log_info("Starting downloads...")
    file_path = filedialog.askopenfilename(title="Select Excel File")
    if not file_path:
        log_info("No Excel file selected.")
        return

    df = pd.read_excel(file_path)
    save_dir = filedialog.askdirectory(title="Select Download Directory")
    if not save_dir:
        log_info("No save directory selected.")
        return

    os.makedirs(save_dir, exist_ok=True)
    progress_bar["maximum"] = len(df)
    progress_bar["value"] = 0

    error_log = []

    def run_downloads():
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for _, row in df.iterrows():
                futures.append(executor.submit(download_image, row["ImageURL"], row["ImageName"], save_dir, error_log))
            for _ in futures:
                progress_bar.step(1)
                root.update_idletasks()

        log_info("Download complete.")
        if error_log:
            error_df = pd.DataFrame(error_log)
            error_path = filedialog.asksaveasfilename(defaultextension=".xlsx", title="Save Error Log")
            if error_path:
                error_df.to_excel(error_path, index=False)
                log_info(f"Error log saved to {error_path}")

    threading.Thread(target=run_downloads, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("Image Downloader")
text = tk.Text(root, wrap=tk.WORD, state=tk.NORMAL, height=10)
text.pack()
progress_bar = ttk.Progressbar(root, mode="determinate")
progress_bar.pack()
download_button = tk.Button(root, text="Download Images", command=start_download)
download_button.pack()
root.mainloop()
