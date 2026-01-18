from helping_func import *

with open("../content/index.md", "r") as f:
    markdown = f.read()

node = markdown_to_html_node(markdown)
print (node.to_html())