from textnode import *
import re
from enum import Enum

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
             new_nodes.append(old_node)
             continue
        new = []
        num_delimiter = old_node.text.count(delimiter)
        if num_delimiter % 2 != 0:
            raise Exception(f"you didn't close {delimiter}")
        parts = old_node.text.split(delimiter)
        for i in range(len(parts)):
            if i % 2 == 0 and parts[i] != "":
                new.append(TextNode(parts[i], TextType.TEXT))
            elif parts[i] != "":
                new.append(TextNode(parts[i], text_type))
        new_nodes.extend(new)
    return new_nodes

def extract_markdown_images(text):
    results = re.findall(r"\!\[([^\]\[]*)\]\(([^\(\)]*)\)", text)
    return results

def extract_markdown_links(text):
    results = re.findall(r"(?<!!)\[([^\]\[]*)\]\(([^\(\)]*)\)", text)
    return results

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        data = extract_markdown_images(node.text)
        if len(data) == 0:
            new_nodes.append(node)
            continue
        texts = []
        tmp = node.text
        for i in range(len(data)):
            tmp = tmp.split(f"![{data[i][0]}]({data[i][1]})", 1)
            texts.append(tmp[0])
            tmp = tmp[1]
        texts.append(tmp)
        new = []
        if texts[0] != "":
            new.append(TextNode(texts[0], TextType.TEXT))
        for i in range(len(data)):
            new.append(TextNode(data[i][0], TextType.IMAGE, data[i][1]))
            if texts[i + 1] != "":
                new.append(TextNode(texts[i + 1], TextType.TEXT))
                pass
        new_nodes.extend(new)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        data = extract_markdown_links(node.text)
        if len(data) == 0:
            new_nodes.append(node)
            continue
        texts = []
        tmp = node.text
        for i in range(len(data)):
            tmp = tmp.split(f"[{data[i][0]}]({data[i][1]})", 1)
            texts.append(tmp[0])
            tmp = tmp[1]
        texts.append(tmp)
        new = []
        if texts[0] != "":
            new.append(TextNode(texts[0], TextType.TEXT))
        for i in range(len(data)):
            new.append(TextNode(data[i][0], TextType.LINK, data[i][1]))
            if texts[i + 1] != "":
                new.append(TextNode(texts[i + 1], TextType.TEXT))
        new_nodes.extend(new)
    return new_nodes
        
def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    CODE = "code"
    HEADING = "heading"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if re.match(r"^(\#{1,6} ).*", block):
        return BlockType.HEADING
    if re.match(r"^```\n.*\n\s*```$", block, re.DOTALL):
        return BlockType.CODE
    if re.match(r"^(\> ).*", block):
        return BlockType.QUOTE
    if re.match(r"^(\- ).*", block):
        return BlockType.UNORDERED_LIST
    if re.match(r"^(\d*\. ).*", block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmls = []
    for block in blocks:
        if block.strip() == "":
            continue
        type = block_to_block_type(block)
        if type == BlockType.CODE:
            block = block.split("```")
            block_lines = block[1].split("\n")
            text = ""
            for line in block_lines:
                if line.strip() != "":
                    text += line.strip() + "\n"
            htmls.append(ParentNode(tag="pre", children=[LeafNode(tag="code", value=text)]))
        elif type == BlockType.QUOTE:
            block_lines = block.split("\n")
            lines = []
            for line in block_lines:
                if line.strip("> ") != "":
                    lines.append(line.strip("> "))
            text = " ".join(lines)
            htmls.append(ParentNode(tag="blockquote", children=text_to_children(text)))
        elif type == BlockType.PARAGRAPH:
            block_lines = block.split("\n")
            text = " ".join(block_lines)
            htmls.append(ParentNode(tag="p", children=text_to_children(text)))
        elif type == BlockType.ORDERED_LIST:
            htmls.append(ParentNode(tag="ol", children=text_to_list_line_nodes(block)))
        elif type == BlockType.UNORDERED_LIST:
            htmls.append(ParentNode(tag="ul", children=text_to_list_line_nodes(block)))
        elif type == BlockType.HEADING:
            n = 0
            for i in block:
                if i == "#":
                    n += 1
                else:
                    break
            text = block[n+1:].lstrip()
            htmls.append(ParentNode(tag=f"h{n}", children=text_to_children(text)))
    return ParentNode(tag="div", children=htmls)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        if text_node.text is not None:
            html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def text_to_list_line_nodes(text):
    bad_lines = text.split("\n")
    lines = []
    for line in bad_lines:
        parts = line.split(" ", 1)
        lines.append(parts[1])
    return lines_to_nodes(lines)
    
def lines_to_nodes(lines):
    line_nodes = []
    for line in lines:
        line_nodes.append(ParentNode(tag="li", children=text_to_children(line)))
    return line_nodes

