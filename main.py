import os
import shutil
import uuid
from PIL import Image
import imagehash

# Create a new folder to store the unique images
folder_name = "unique_images"
os.makedirs(folder_name, exist_ok=True)

# Recursively iterate over all the subdirectories in the current directory
for root, dirs, files in os.walk("."):
    # Iterate over all the images in the current directory
    for image_file in files:
        # Check if the file is an image
        if image_file.endswith(".jpg") or image_file.endswith(".png"):
            # Open the image and compute its pHash
            with Image.open(os.path.join(root, image_file)) as image:
                image_hash = imagehash.phash(image)

            # Check if the image hash is unique
            unique = True
            for other_image_file in os.listdir(folder_name):
                with Image.open(os.path.join(folder_name, other_image_file)) as other_image:
                    other_image_hash = imagehash.phash(other_image)
                if image_hash == other_image_hash:
                    unique = False
                    break

            # If the image is unique, copy it to the new folder and rename it with the path to the original image and a UUID
            if unique:
                shutil.copy(os.path.join(root, image_file), folder_name)
                new_image_file = os.path.join(folder_name, image_file)
                os.rename(new_image_file, new_image_file + " - " + root + " - " + str(uuid.uuid4()))
