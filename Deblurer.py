import os
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image

def deblur_image(blurry_image, kernel_size=(5, 5), iterations=30):
    # Determine the number of channels in the image
    num_channels = blurry_image.shape[-1] if len(blurry_image.shape) == 3 else 1

    # Create a simple uniform kernel based on the number of channels
    kernel = np.ones(kernel_size + (num_channels,)) / np.prod(kernel_size)

    # Perform Richardson-Lucy deconvolution
    deblurred_image = blurry_image.copy()
    for _ in range(iterations):
        estimated_blur = ndi.convolve(deblurred_image, kernel)
        ratio = blurry_image / (estimated_blur + 1e-8)
        deblurred_image *= ndi.convolve(ratio, kernel)

    # Normalize the image to the range [0, 255] and convert to uint8
    deblurred_image = np.clip(deblurred_image * 255, 0, 255).astype(np.uint8)

    return deblurred_image

def deblur_images_in_folder(input_folder_path, output_folder_path, kernel_size=(5, 5), iterations=30):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # List all files in the input folder
    image_files = os.listdir(input_folder_path)

    for filename in image_files:
        input_image_path = os.path.join(input_folder_path, filename)
        output_image_path = os.path.join(output_folder_path, filename)

        # Load the blurry image
        blurry_image = plt.imread(input_image_path)

        # Convert the image to a clear version
        clear_image = deblur_image(blurry_image, kernel_size, iterations)

        # Save the deblurred image in the output folder
        clear_image_pil = Image.fromarray(clear_image)
        clear_image_pil.save(output_image_path)


if __name__ == "__main__":
    input_folder_path = r"C:\Users\User\Downloads\Target Image\8-04-2023\Resized"
    output_folder_path = r"C:\Users\User\Downloads\Target Image\8-04-2023\Resized\Washed"
    kernel_size = (5, 5)
    iterations = 30

    deblur_images_in_folder(input_folder_path, output_folder_path, kernel_size, iterations)
