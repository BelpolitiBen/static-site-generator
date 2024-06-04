import re
from textnode import (
    TextNode, TextTypes
)

delimiters = {TextTypes.text_type_code: "`", TextTypes.text_type_bold: "**", TextTypes.text_type_italic: "*"}



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextTypes.text_type_text:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        l = len(split_node)
        for i in range(l):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextTypes.text_type_text))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    regexd_text = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return regexd_text


def extract_markdown_links(text):
    regexd_text = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return regexd_text


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        listas = []
        for image in images:
            lista = node.text.split(f"![{image[0]}]({image[1]})", 1)
            if lista[0]:
                new_node = TextNode(lista[0], TextTypes.text_type_text)
                listas.append(new_node)
            new_image_node = TextNode(image[0], TextTypes.text_type_image, image[1])
            listas.append(new_image_node)
            if lista[1] and not extract_markdown_images(lista[1]):
                listas.append(TextNode(lista[1], TextTypes.text_type_text))
            node.text = node.text.replace(f"{lista[0]}![{image[0]}]({image[1]})", "")
        new_nodes.extend(listas)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        listas = []
        for link in links:
            lista = node.text.split(f"[{link[0]}]({link[1]})", 1)
            new_node = TextNode(lista[0], TextTypes.text_type_text)
            new_image_node = TextNode(link[0], TextTypes.text_type_link, link[1])
            listas.append(new_node)
            listas.append(new_image_node)
            if lista[1] and not extract_markdown_links(lista[1]):
                listas.append(TextNode(lista[1], TextTypes.text_type_text))
            node.text = node.text.replace(f"{lista[0]}[{link[0]}]({link[1]})", "")
        new_nodes.extend(listas)
    return new_nodes


def text_to_textnodes(text):
    first_node = TextNode(text, TextTypes.text_type_text)
    nodes = [first_node]
    for text_type, delimiter in delimiters.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes