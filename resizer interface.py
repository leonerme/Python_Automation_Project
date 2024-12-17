import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def resize_images(input_folder, output_folder, target_size=(1000, 1000), dpi=300):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            with Image.open(input_path) as image:
                # Resize the image
                resized_image = image.resize(target_size)
                # Set the DPI
                resized_image.info["dpi"] = (dpi, dpi)
                # Save the resized image
                resized_image.save(output_path, dpi=(dpi, dpi))
                print(f"Resized {filename} successfully!")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

def select_folder():
    global path_1
    path_1 = filedialog.askdirectory()
    print(f"Selected Folder: {path_1}")

def start_resizing():
    if 'path_1' in globals():
        output_folder = os.path.join(path_1, "Resized")
        resize_images(path_1, output_folder)
        print("Resizing Completed!")
    else:
        print("Please select a folder first.")

if __name__ == "__main__":
    path_1 = None

    root = tk.Tk()
    root.title("Image Resizer")
    root.geometry("400x200")

    label = tk.Label(root, text="Select a folder to resize images:")
    label.pack(pady=10)

    select_button = tk.Button(root, text="Select Folder", command=select_folder)
    select_button.pack(pady=10)

    start_button = tk.Button(root, text="Start Resizing", command=start_resizing)
    start_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()
