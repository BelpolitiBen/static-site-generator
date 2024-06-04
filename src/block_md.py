from htmlnode import ParentNode, text_node_to_html_node
from inline_md import text_to_textnodes

class BlockTypes:    
    block_type_paragraph = "paragraph"
    block_type_quote = "quote"
    block_type_unordered_list = "unordered_list"
    block_type_code = "code"
    block_type_heading = "heading"
    block_type_ordered_list = "ordered_list"

def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        stripped_blocks.append(block.strip())
    return stripped_blocks

def block_to_block_type(block):
    if block.startswith("> "):
        return BlockTypes.block_type_quote
    if block.startswith("* ") or block.startswith("- "):
        return BlockTypes.block_type_unordered_list
    if block.startswith("```") and block.endswith("```"):
        return BlockTypes.block_type_code
    if block.startswith("#"):
        partitioned_block = block.partition(" ")
        if len(partitioned_block[0]) <= 6:
            for char in partitioned_block[0]:
                if char != "#":
                    return BlockTypes.block_type_paragraph
            return BlockTypes.block_type_heading
    if block.startswith(". ", 1):
        lines = block.split("\n")
        counter = 1
        for line in lines:
            if not line[0].isnumeric() or int(line[0]) != counter:
                return BlockTypes.block_type_paragraph
            counter += 1
        return BlockTypes.block_type_ordered_list
    return BlockTypes.block_type_paragraph

def block_to_html_leafs(block, remove_newlines=True):
    text = block.replace("\n", " ") if remove_newlines else block
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes

def line_to_li(line):
    text_nodes = text_to_textnodes(line)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return ParentNode("li", leaf_nodes)

def block_to_html_paragraph(block):
    leaf_nodes = block_to_html_leafs(block)
    return ParentNode("p", leaf_nodes)  
    
def block_to_html_quote(block):
    split_blocks = block.replace("\n", " \n").split("\n")
    li_elements = []
    for line in split_blocks:
        filtered_line = line.lstrip("> ")
        text_nodes = text_to_textnodes(filtered_line)
        leaf_nodes = []
        for node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(node))   
        li_elements.extend(leaf_nodes)
    return ParentNode("blockquote", li_elements) 
    
def block_to_html_code(block):
    filtered_block = block.strip("```").strip()
    leaf_nodes = block_to_html_leafs(filtered_block, False)
    code_tag = ParentNode("code", leaf_nodes)
    return ParentNode("pre", [code_tag])
    
def block_to_html_ordered_list(block):
    split_blocks = block.split("\n")
    li_elements = []
    for line in split_blocks:
        _, _, text = line.partition(". ")
        li_elements.append(line_to_li(text))
    return ParentNode("ol", li_elements)
    
def block_to_html_unordered_list(block):
    split_blocks = block.split("\n")
    li_elements = []
    for line in split_blocks:
        filtered_line = line.lstrip("* ").lstrip("- ")
        li_elements.append(line_to_li(filtered_line))
    return ParentNode("ul", li_elements)
    
def block_to_html_heading(block):
    partitioned_block = block.partition(" ")
    leaf_nodes = block_to_html_leafs(partitioned_block[2])
    heading = "h" + str(len(partitioned_block[0]))
    return ParentNode(heading, leaf_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    elements = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockTypes.block_type_code:
                elements.append(block_to_html_code(block))
            case BlockTypes.block_type_heading:
                elements.append(block_to_html_heading(block))
            case BlockTypes.block_type_ordered_list:
                elements.append(block_to_html_ordered_list(block))
            case BlockTypes.block_type_quote:
                elements.append(block_to_html_quote(block))
            case BlockTypes.block_type_unordered_list:
                elements.append(block_to_html_unordered_list(block))
            case _:
                elements.append(block_to_html_paragraph(block))
    return ParentNode("div", elements)