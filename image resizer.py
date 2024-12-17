import os
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

if __name__ == "__main__":
    input_folder = r"C:\Users\User\Downloads\Target Image\Image Resizer\Images"  # Replace with the full path of "New Images" folder
    output_folder = r"C:\Users\User\Downloads\Target Image\Image Resizer\Resized Images"    # Replace with the full path of "Resized" folder
    resize_images(input_folder, output_folder)
