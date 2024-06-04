import unittest
from inline_md import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from textnode import (
    TextNode, TextTypes
)

class TestInlineMarkdown(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextTypes.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.text_type_code)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextTypes.text_type_text), TextNode("code block", TextTypes.text_type_code), TextNode(" word", TextTypes.text_type_text)])
    def test_split_2(self):
        node = TextNode("This is text with a `code block` word and an *italic* word", TextTypes.text_type_text)
        step_1 = split_nodes_delimiter([node], "`", TextTypes.text_type_code)
        new_nodes = split_nodes_delimiter(step_1, "*", TextTypes.text_type_italic)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextTypes.text_type_text), TextNode("code block", TextTypes.text_type_code), TextNode(" word and an ", TextTypes.text_type_text), TextNode("italic", TextTypes.text_type_italic), TextNode(" word", TextTypes.text_type_text)])
    
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextTypes.text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("bolded", TextTypes.text_type_bold),
                TextNode(" word", TextTypes.text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextTypes.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("bolded", TextTypes.text_type_bold),
                TextNode(" word and ", TextTypes.text_type_text),
                TextNode("another", TextTypes.text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextTypes.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextTypes.text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("bolded word", TextTypes.text_type_bold),
                TextNode(" and ", TextTypes.text_type_text),
                TextNode("another", TextTypes.text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextTypes.text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", TextTypes.text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.text_type_text),
                TextNode("italic", TextTypes.text_type_italic),
                TextNode(" word", TextTypes.text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextTypes.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", TextTypes.text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("code block", TextTypes.text_type_code),
                TextNode(" word", TextTypes.text_type_text),
            ],
            new_nodes,
        )
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextTypes.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.text_type_text),
                TextNode("image", TextTypes.text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextTypes.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextTypes.text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextTypes.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.text_type_text),
                TextNode("image", TextTypes.text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextTypes.text_type_text),
                TextNode(
                    "second image", TextTypes.text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextTypes.text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextTypes.text_type_text),
                TextNode("link", TextTypes.text_type_link, "https://boot.dev"),
                TextNode(" and ", TextTypes.text_type_text),
                TextNode("another link", TextTypes.text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextTypes.text_type_text),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextTypes.text_type_text),
                TextNode("text", TextTypes.text_type_bold),
                TextNode(" with an ", TextTypes.text_type_text),
                TextNode("italic", TextTypes.text_type_italic),
                TextNode(" word and a ", TextTypes.text_type_text),
                TextNode("code block", TextTypes.text_type_code),
                TextNode(" and an ", TextTypes.text_type_text),
                TextNode("image", TextTypes.text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextTypes.text_type_text),
                TextNode("link", TextTypes.text_type_link, "https://boot.dev"),
            ],
            nodes,
        )
        
if __name__ == "__main__":
    unittest.main()