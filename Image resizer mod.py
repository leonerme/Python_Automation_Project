import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageOps
from threading import Thread

def make_square(image):
    width, height = image.size
    if width == height:
        return image  # Already square
    
    # Determine padding
    size = max(width, height)
    new_image = Image.new("RGB", (size, size), (255, 255, 255))  # White background
    paste_x = (size - width) // 2
    paste_y = (size - height) // 2
    new_image.paste(image, (paste_x, paste_y))
    return new_image

def resize_images(input_folder, output_folder, target_size=(1000, 1000), dpi=300):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith((
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'))]
    total_images = len(image_files)
    
    for i, filename in enumerate(image_files):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            with Image.open(input_path) as image:
                image = make_square(image)  # Ensure the image is square
                resized_image = image.resize(target_size)
                resized_image.save(output_path, dpi=(dpi, dpi))
                print(f"Resized {filename} successfully!")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
        
        progress_var.set((i + 1) / total_images * 100)
        root.update_idletasks()

def select_folder():
    global path_1
    path_1 = filedialog.askdirectory()
    print(f"Selected Folder: {path_1}")

def start_resizing():
    if 'path_1' in globals():
        output_folder = os.path.join(path_1, "Resized")
        target_size_str = size_entry.get()
        try:
            width, height = map(int, target_size_str.split("x"))
            target_size = (width, height)
            resizing_thread = Thread(target=resize_images, args=(path_1, output_folder, target_size))
            resizing_thread.start()
        except ValueError:
            print("Invalid size format. Please enter width and height in the format 'width x height'.")
    else:
        print("Please select a folder first.")

if __name__ == "__main__":
    path_1 = None

    root = tk.Tk()
    root.title("Image Resizer")
    root.geometry("400x300")

    label = tk.Label(root, text="Select a folder to resize images:")
    label.pack(pady=10)

    select_button = tk.Button(root, text="Select Folder", command=select_folder)
    select_button.pack(pady=10)

    size_label = tk.Label(root, text="Enter target size (e.g., 1000x1000):")
    size_label.pack()

    size_entry = tk.Entry(root)
    size_entry.pack()

    start_button = tk.Button(root, text="Start Resizing", command=start_resizing)
    start_button.pack(pady=10)

    progress_var = tk.DoubleVar()
    progress = ttk.Progressbar(root, variable=progress_var)
    progress.pack(pady=10)

    root.mainloop()