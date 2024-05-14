import os

def delete_images():
    folder_path = 'c:/Users/Chill/Desktop/python/Metro24/images'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)