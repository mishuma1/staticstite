from enums import BlockType, TextType
from helpers import text_to_textnodes,text_node_to_html_node,split_nodes_delimiter
from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import TextNode
import re

def markdown_to_blocks(markdown):
    new_markdown = []
    block_groups = markdown.split('\n\n')
    for blocks in block_groups:  
            sub_blocks = list(map(lambda x: x.strip(), blocks.strip().split('\n')))
            if len(sub_blocks) > 0:
                new_markdown.append("\n".join(sub_blocks))
    return new_markdown            

def block_to_block_type(markdown_text):
    #Determine type - reg types
    heading_regex = "^(#{1,6})"
    #First try
    #code_regex = "^(`{3}).*(`{3})"
    code_regex="(`{3})(.*\n?)+(`{3})"
    code_reg_comp = re.compile(code_regex, re.MULTILINE)
    quotes = "^>.*"
    unordered_list = "^-.*"
    ordered_list = lambda x: f"^{x}\\.(?:.*)"
    if re.match(heading_regex, markdown_text):
        return BlockType.HEADING
    elif code_reg_comp.match(markdown_text):
        return BlockType.CODE
    else:
        text_lines = markdown_text.split("\n")
        quote_match = True
        unordered_match = True
        ordered_match = True
        for ind in range(0, len(text_lines)):
            if not re.match(quotes, text_lines[ind]):
                 quote_match = False
            if not re.match(unordered_list, text_lines[ind]):
                 unordered_match = False
            if not re.match(ordered_list(ind+1), text_lines[ind]):
                 ordered_match = False                                  
              
        if quote_match:
            return BlockType.QUOTE
        if unordered_match:
            return BlockType.UNORDERED_LIST 
        if ordered_match:
            return BlockType.ORDERED_LIST 
        
        #Default
        return BlockType.PARAGRAPH

def sub_search(this_block):
    html_str = "" 
    for items in this_block.split('\n'):
        if len(items) > 0:                                  
            text_nodes = text_to_textnodes(items)
            print(f"NODES AA:{text_nodes}") 
            for text_item in text_nodes:
                match text_item.text_type:
                    case TextType.BOLD:
                        html_str += f"<b>{text_item.text}</b>"
                    case TextType.ITALIC:
                        html_str += f"<i>{text_item.text}</i>"
                    case TextType.CODE:
                        html_str += f"<pre><code>{text_item.text}</code></pre>"
                    case TextType.LINK:
                        print("LINK")
                        html_str += f"<a href='{text_item.url}'>{text_item.text}</a>"
                    case TextType.IMAGE:
                        print(f"IMAGE AA:{text_item}")
                        html_str += f"<img src='{text_item.url}' alt='{text_item.text}'>"
                    case TextType.TEXT:
                        html_str += f"{text_item.text}"   
    return html_str

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_line = []
    print(f"main markdown:{markdown_blocks}")
    for this_block in markdown_blocks:
          print(f"this block:|{this_block},:{len(this_block)}|")
          if len(this_block) > 0:
            print(f"markdown blocks:{markdown_blocks}")
            print(f"block_to_block_type:{block_to_block_type(this_block)}")
            match block_to_block_type(this_block):
                case BlockType.PARAGRAPH:
                    html_str = sub_search(this_block) + " "
                    """                 html_str = ""
                    #print(f"block:{this_block}")
                    for items in this_block.split('\n'):
                        if len(items) > 0:              
                            print(f"ITEM AA:{items}")                       
                            text_nodes = text_to_textnodes(items)
                            print(f"NODES AA:{text_nodes}") 
                            for text_item in text_nodes:
                                match text_item.text_type:
                                    case TextType.BOLD:
                                        html_str += f"<b>{text_item.text}</b>"
                                    case TextType.ITALIC:
                                        html_str += f"<i>{text_item.text}</i>"
                                    case TextType.CODE:
                                        html_str += f"```{text_item.text}```"
                                    case TextType.LINK:
                                        print("LINK")
                                        html_str += f"[{text_item.text}]({text_item.url})"
                                    case TextType.IMAGE:
                                        print(f"IMAGE AA:{text_item}")
                                        html_str += f"<img src='{text_item.url}' alt='{text_item.text}'>"
                                        #html_str += f"<a ![{text_item.text}]({text_item.url})"
                                    case TextType.TEXT:
                                        html_str += f"{text_item.text}" """
                            #html_str += " "
                            #html_str += text_node_to_html_node(items).to_html
                            #print(f"html_str:{html_str}")
                    html_line.append(LeafNode("div", html_str))
                    #print(f"HTML line:{html_line}")
                case BlockType.HEADING:
                    tmp_remove = this_block.strip('#')
                    tmp_remove = tmp_remove.strip()
                    html_line.append(LeafNode("div", f"<h1>{tmp_remove}</h1>"))
                case BlockType.CODE:
                    tmp_remove = this_block.replace("```", "")
                    html_line.append(LeafNode("div", f"<pre><code>{tmp_remove}</code></pre>"))
                case BlockType.QUOTE:
                    #tag "blockquote"
                    quote = ""
                    for quoteline in this_block.split('>'):
                        quote += quoteline.strip()
                        quote = sub_search(quote)

                    html_line.append(LeafNode("blockquote", f"{quote}"))    
                    #print(f"MARK 2: {this_block}")
                case BlockType.UNORDERED_LIST:
                    unorder = ""
                    for unorder_line in this_block.split('\n'):
                        unorder_line = unorder_line.replace("-", "", 1).strip()
                        unorder_line = sub_search(unorder_line)
                        unorder += f"<li>{unorder_line}</li>"
                    html_line.append(LeafNode("ul", f"{unorder}"))    
                    print(f"UNORDER:{unorder}")
                case BlockType.ORDERED_LIST:
                    order = ""
                    for order_line in this_block.split('\n'):
                        #find the first dot and return the right side
                        ind = order_line.index(".")
                        order_line = order_line[ind+1:]
                        order_line = sub_search(order_line.strip())
                        order += f"<li>{order_line}</li>"
                    html_line.append(LeafNode("ol", f"{order}"))                   
                    print(f"ORDER:{order}")
        
    print(f"LEAVNING MTHN")
    return ParentNode("html", html_line)
    #tag=None,value=None,children=None,props=None

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    for this_block in markdown_blocks:
          match block_to_block_type(this_block):
            case BlockType.HEADING:
                return this_block.strip('#').strip()

    raise Exception("Missing Title")
