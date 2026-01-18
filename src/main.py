import os
import shutil
from helping_func import *

def main():
    copy_static_to_public()
    generate_pages_recursive("./content", "./template.html", "./public")






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

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        parts = line.split(" ", 1)
        if parts[0] == "#":
            titles = parts[1]
    try:
        return titles.strip()
    except Exception:
        raise Exception("there is no title (<h1>)")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f1:
        markdown = f1.read()
    with open(template_path, "r") as f2:
        template = f2.read()
    html_text = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    new_file = template.replace("{{ Title }}", title).replace("{{ Content }}", html_text)
    dirpath = os.path.dirname(dest_path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(dest_path, "w") as f3:
        f3.write(new_file)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    names = os.listdir(dir_path_content)
    for name in names:
        src_path = os.path.join(dir_path_content, name)
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                generate_page(src_path, template_path, os.path.join(dest_dir_path, name.replace(".md", ".html") ))
        if os.path.isdir(src_path):
            new_dest_dir = os.path.join(dest_dir_path, name)
            if not os.path.exists(new_dest_dir):
                os.makedirs(new_dest_dir)
            generate_pages_recursive(src_path, template_path, new_dest_dir)
        










if __name__ == "__main__":
    main()