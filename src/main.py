import os
import shutil

def main():
    copy_static_to_public()






def copy_static_to_public():
    public_dir = "./public"
    if not os.path.exists(public_dir):
        os.mkdir(os.path.join(public_dir))
    for item in os.listdir(public_dir):
        item_path = os.path.join(public_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    copy_directory("./static", public_dir)


def copy_directory(source, destination):
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination)
        if os.path.isdir(item_path):
            if not os.path.exists(os.path.join(destination, item)):
                os.mkdir(os.path.join(destination, item))
            copy_directory(item_path, os.path.join(destination, item))










if __name__ == "__main__":
    main()