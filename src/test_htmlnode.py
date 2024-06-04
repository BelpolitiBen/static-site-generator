import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("", "", "", {"href": "asd.com", "target": "_blank", "autoplay": True})
        props = node.props_to_html()
        self.assertEqual(props, 'href="asd.com" target="_blank" autoplay="True"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_render_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    def test_leaf_render(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_leaf_render_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_1(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode("a", "Click me!", {"href": "https://www.google.com"}), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
        self.assertEqual(node.to_html(), '<p><b>Bold text</b><a href="https://www.google.com">Click me!</a><i>italic text</i>Normal text</p>') 
    def test_2(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>") 
    def test_3(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
        node2 = ParentNode("div", [LeafNode("b", "Bold text"), node])
        self.assertEqual(node2.to_html(), "<div><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>") 
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()