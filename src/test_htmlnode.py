import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        n1 = HTMLNode("a", "i am the storm")
        n2 = HTMLNode("a", "i am the storm", None, {"href":"www.xd.com"})
        self.assertEqual(n1.props_to_html(), "")
        self.assertEqual(n2.props_to_html(), ' href="www.xd.com"')

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
    

if __name__ == "__main__":
    unittest.main()