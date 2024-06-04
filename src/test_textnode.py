import unittest

from textnode import TextNode
from htmlnode import text_node_to_html_node
from inline_md import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node ", "bold")
        self.assertNotEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bald")
        self.assertNotEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bald", "brih.com")
        self.assertNotEqual(node, node2)

class TestSplitter(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(new_nodes, [TextNode("This is text with a ", "text"), TextNode("code block", "code"), TextNode(" word", "text")])
    def test_split_2(self):
        node = TextNode("This is text with a `code block` word and a *bold* word", "text")
        step_1 = split_nodes_delimiter([node], "`", "code")
        new_nodes = split_nodes_delimiter(step_1, "*", "bold")
        self.assertEqual(new_nodes, [TextNode("This is text with a ", "text"), TextNode("code block", "code"), TextNode(" word and a ", "text"), TextNode("bold", "bold"), TextNode(" word", "text")])



if __name__ == "__main__":
    unittest.main()
