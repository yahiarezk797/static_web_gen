import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_link_noteq(self):
        node1 = TextNode("i am the storm", TextType.LINK, "www.i_am_the_storm.xd")
        node2 = TextNode("i am the storm", TextType.IMAGE, "www.i_am_the_storm.xd")
        self.assertNotEqual(node1, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
if __name__ == "__main__":
    unittest.main()