import unittest
from textnode import TextNode
from block_md import (markdown_to_blocks, BlockTypes, markdown_to_html_node, block_to_block_type)


class TestBlockMarkdown(unittest.TestCase):
    def test_eq(self):
        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, ['This is **bolded** paragraph', 'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line', '* This is a list\n* with items'])
        

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
        
    def test_blocks_to_block_types_headings(self):
        blocks = ["# H1", "## H2", "### H3", "#### H4", "##### H5",  "###### H6"]
        for block in blocks:
            self.assertEqual(
            block_to_block_type(block),
            BlockTypes.block_type_heading,
        )
        wrong_heading = "####### H7"
        self.assertEqual(block_to_block_type(wrong_heading), BlockTypes.block_type_paragraph)
        
    def test_blocks_to_block_types_ol(self):
        ol = """1. Hello
2. World
3. I'm
4. An ordered list"""
        self.assertEqual(block_to_block_type(ol), BlockTypes.block_type_ordered_list)
        ol = """1. Hello
3. World
2. I'm
4. An ordered list"""
        ol = """1. Hello
. World
3. I'm
4. An ordered list"""
        self.assertEqual(block_to_block_type(ol), BlockTypes.block_type_paragraph)
        self.assertEqual(block_to_block_type(ol), BlockTypes.block_type_paragraph)
        
    def test_block_to_block_other_types(self):
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockTypes.block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockTypes.block_type_unordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockTypes.block_type_paragraph)
        
    
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print("PARAGRAPHS")
        print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
        
if __name__ == "__main__":
    unittest.main()