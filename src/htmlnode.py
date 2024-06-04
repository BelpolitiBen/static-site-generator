from textnode import (
    TextNode, TextTypes
)

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        props_string = ""
        if self.props != None:
            for key, value in self.props.items():
                props_string += f'{key}="{value}" '
        return props_string.rstrip()
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode requires a value.")
        if self.tag == None:
            return self.value
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
        def __init__(self, tag, children, props=None):
            super().__init__(tag, None, children, props)
        def to_html(self):
            if self.tag == None:
                raise ValueError("ParentNode requires a tag.")
            if self.children == None:
                raise ValueError("ParentNode requires a child.")
            result = ""
            for child in self.children:
                result += child.to_html()
            if self.props == None:
                return f"<{self.tag}>{result}</{self.tag}>"
            else:
                return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
            
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextTypes.text_type_text:
            return LeafNode(None, text_node.text) 
        case TextTypes.text_type_bold:
            return LeafNode("b", text_node.text)  
        case TextTypes.text_type_italic:
            return LeafNode("i", text_node.text)   
        case TextTypes.text_type_code:
            return LeafNode("code", text_node.text)   
        case TextTypes.text_type_link:
            return LeafNode("a", text_node.text, {"href": text_node.url})   
        case TextTypes.text_type_image:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")