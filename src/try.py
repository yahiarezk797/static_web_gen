from helping_func import *

node = TextNode(
    "a ![x](1) b ![y](2) c",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node])
print(new_nodes)
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]