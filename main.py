import os
import shutil
import uuid
from PIL import Image
import imagehash
import hashlib

folder_name = "unique_files"
unique_file_hashes = {}

def HashImage(folder_name, file):
    with Image.open(os.path.join(folder_name, file)) as image:
        return imagehash.phash(image)

def HashVideo(folder_name, file):
    with open(os.path.join(folder_name, file), "rb") as video:
        return hashlib.sha256(video.read()).hexdigest()

def InitializeUniqueHashesDict():
    for file in os.listdir(folder_name):
        print(file)
        file_hash = False

        if file.endswith(".jpg") or file.endswith(".png"):
            file_hash = HashImage(folder_name, file)
        elif file.endswith(".mp4") or file.endswith(".avi"):
            file_hash = HashVideo(folder_name, file)

        if file_hash:
            unique_file_hashes[file_hash] = True

def IsFileUnique(root, file_path, file_type = 'image'):
    file_hash = False

    if file_type == 'image':
        file_hash = HashImage(root, file_path)
    elif file_type == 'video': 
        file_hash = HashVideo(root, file_path)

    if file_hash in unique_file_hashes:
        return False
    else: 
        unique_file_hashes[file_hash] = True
        return True            
           
def SaveUniqueFileToFolder(root, folder_name, file_path):
    new_file_path = os.path.join(folder_name, file_path)
    shutil.copy(os.path.join(root, file_path), new_file_path)
    file_name = file_path.rsplit('.', 1)[0]
    file_ext = file_path.rsplit('.', 1)[1]
    os.rename(new_file_path, os.path.join(folder_name, (((root + "-" + file_name + str(uuid.uuid4())).replace(os.sep,'-')).replace('.','')) + '.' + file_ext))


def GenerateAllUniqueImages():
    os.makedirs(folder_name, exist_ok=True)
    InitializeUniqueHashesDict()
    for root, dirs, files in os.walk("."):
        if root == "./" + folder_name:
            continue
        for file in files:
            unique = False

            if file.endswith(".jpg") or file.endswith(".png"):
                unique = IsFileUnique(root, file, 'image')

            elif file.endswith(".mp4") or file.endswith(".avi"):
                unique = IsFileUnique(root, file, 'video')

            if unique:
                SaveUniqueFileToFolder(root, folder_name, file)

GenerateAllUniqueImages()