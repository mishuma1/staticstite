import unittest
from enums import TextType, BlockType
from textnode import TextNode
from htmlnode import HTMLNode,LeafNode,ParentNode
from helpers import (
    split_nodes_delimiter,extract_markdown_images, 
    extract_markdown_links,split_nodes_image, 
    split_nodes_link, text_node_to_html_node)
from markdown import block_to_block_type, markdown_to_blocks, markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_empty(self):
        node = TextNode()
        node2 = TextNode()
        self.assertEqual(node, node2)
	
    def test_diff(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)
	
    def test_wrong_enum(self):
        try:
                self.assertRaises(AttributeError, TextNode("This is a text node", TextType.UNKNOWN))
        except Exception as e:
                if "has no attribute".find(str(e)):
                     e="has no attribute"
                self.assertEqual("has no attribute", e)

    def test_HTMLNode_empty_match(self):
        hnode = repr(HTMLNode())
        hnode2 = repr(HTMLNode(None,None,None,None))
        self.assertEqual(hnode, hnode2)

    def test_HTMLNode_diff1(self):
        hnode = HTMLNode("tr", "Hello Test", None, {"href" : "https://www.google.com"})
        hnode2 = HTMLNode("td", "Hello Test2", None, {"href" : "https://www.google.com"})
        self.assertNotEqual(hnode, hnode2)

    def test_HTMLNode_same(self):
        hnode =  repr(HTMLNode("tr", "Hello Test", None, {"href" : "https://www.google.com"}))
        hnode2 = repr(HTMLNode("tr", "Hello Test", None, {"href" : "https://www.google.com"}))
        self.assertEqual(hnode, hnode2)  

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')        

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text_plain(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")   

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")          

    def test_split_nodes_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)  
	
    def test_split_nodes_bold_delimiter(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(repr(new_nodes[0]), 'TextNode("This is text with a ","TextType.TEXT")')

    def test_split_nodes_italic_delimiter(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[1].text_type,TextType.ITALIC)  
	
    def test_extract_links(self):
        text = "This is text with an [mylink](https://i.imgur.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("mylink", "https://i.imgur.com")], matches)  

    def test_extract_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)  

    def test_extract_images_with_multi(self):
        text = "text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches) 
   
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_endtext(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a", TextType.TEXT),
            ],
            new_nodes,
        )       

    def test_split_links_with_endtext(self):
        node = TextNode(
            "This is text with an [link1](https://i.imgur.com/zjjcJKZ.png) and another [link2](https://i.imgur.com/3elNhQu.png) and a",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a", TextType.TEXT),
            ],
            new_nodes,
        )       

    def full_test(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )       

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_detect_header_w1(self):
        md = """#Header"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.HEADING)
	
    def test_markdown_detect_header_w6(self):
        md = """######Header"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.HEADING)

    def test_markdown_detect_ordered(self):
        md = "1. Test\n2.Hello\n3.HI"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.ORDERED_LIST)

    def test_markdown_detect_paragraph(self):
        md = "1. Test\n4.Hello\n3.HI"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)

    def test_markdown_detect_unordered(self):
        md = "- Test\n- Hello\n- HI"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.UNORDERED_LIST)

    def test_markdown_detect_code(self):
        md = "```- Test\\n- Hello\\n- HI```"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.CODE)

    def test_markdown_detect_quote(self):
        md = ">HElllo\n>Test"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.QUOTE)	

    def mark_to_html_paragraph_only(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<html><div>This is <b>bolded</b> paragraph text in a p tag here </div><div>This is another paragraph with <i>italic</i> text and ```code``` here </div></html>")

    def mark_to_html_code_only(self):
        md = """
	    ```
	    This is text that _should_ remain
	    the **same** even with inline stuff
	    ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<html><div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div></html>")

    def mark_to_html_code_paragraph(self):
        md = """
	        ```
	        This is text that _should_ remain
	        the **same** even with inline stuff
	        ```

		    This is **bolded** paragraph
		    text in a p
		    tag here

		    This is another paragraph with _italic_ text and `code` here
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<html><div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div><div>This is <b>bolded</b> paragraph text in a p tag here </div><div>This is another paragraph with <i>italic</i> text and ```code``` here </div></html>")


if __name__ == "__main__":
    unittest.main()
