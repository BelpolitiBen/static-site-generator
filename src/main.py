from textnode import TextNode
from block_md import markdown_to_html_node
import os
import shutil

def main():
    generate_page("C:\\dev\\boot-dev-projects\\static-site-generator\\content\\index.md", "C:\\dev\\boot-dev-projects\\static-site-generator\\template.html", "C:\\dev\\boot-dev-projects\\static-site-generator\\public\\")

def copy_to_path(from_path, to_path):
    if not os.path.exists(from_path):
        raise Exception("Path to copy from does not exist")
    
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
        os.mkdir(to_path)
    else:
        os.mkdir(to_path)
    
    paths = os.listdir(from_path)
    for path in paths:
        curr_path = os.path.join(from_path, path)
        if os.path.isfile(curr_path):
            shutil.copy(curr_path, to_path)
        else:
            subpath = os.path.join(to_path, path)
            copy_to_path(curr_path, subpath)
            
def generate_page(from_path, template_path, to_path):
    
    print(f"Generating page from {from_path} to {to_path} using {template_path}")
    
    md_file = open(from_path)
    markdown = md_file.read()
    md_file.close()
    
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    file_name = os.path.join(to_path, "index.html")
    dest_file = open(file_name, "w")
    dest_file.write(template)
    dest_file.close()
    
    
    
    

def extract_title(markdown: str):
    filtered_md = markdown.strip()
    if not filtered_md.startswith("# "):
        raise Exception("All markdown pages need to start with a header.")
    title = filtered_md.split("\n", 1)[0].lstrip("# ")
    return title



main()