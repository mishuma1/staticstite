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
    #print(f"{markdown_text}")
    #Determine type - reg types
    heading_regex = "^(#{1,6})"
    #First try
    #code_regex = "^(`{3}).*(`{3})"
    code_regex="(`{3})(.*\n?)+(`{3})"
    code_reg_comp = re.compile(code_regex, re.MULTILINE)
    quotes = "^>.*"
    unordered_list = "^-.*"
    ordered_list = lambda x: f"^{x}\\.(?:.*)"
    #print(f"MARKDOWN:|{markdown_text}|")
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
            #print(f"{quote_match},{unordered_match},{ordered_match}")
            #print(f"{text_lines[ind]}")
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

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_line = []
    print(f"main markdown:{markdown_blocks}")
    for this_block in markdown_blocks:
          #print(f"match blocks:{block_to_block_type(this_block)}")
          match block_to_block_type(this_block):
            case BlockType.PARAGRAPH:
                html_str = ""
                #print(f"block:{this_block}")
                for items in this_block.split('\n'):
                    if len(items) > 0:              
                        #print(f"ITEM:{items}")                       
                        text_nodes = text_to_textnodes(items)
                        for text_item in text_nodes:
                            match text_item.text_type:
                                case TextType.BOLD:
                                    html_str += f"<b>{text_item.text}</b>"
                                case TextType.ITALIC:
                                    html_str += f"<i>{text_item.text}</i>"
                                case TextType.CODE:
                                    html_str += f"```{text_item.text}```"
                                case TextType.LINK:
                                    html_str += f"[{text_item.text}]({text_item.url})"
                                case TextType.IMAGE:
                                    html_str += f"![{text_item.text}]({text_item.url})"
                                case TextType.TEXT:
                                    html_str += f"{text_item.text}"
                        html_str += " "
                        #html_str += text_node_to_html_node(items).to_html
                        #print(f"html_str:{html_str}")
                html_line.append(LeafNode("div", html_str))
                #print(f"HTML line:{html_line}")
            case BlockType.HEADING:
                tmp_remove = this_block.strip('#"')
                html_line.append(LeafNode("div", f"<h1>{tmp_remove}</h1>"))
            case BlockType.CODE:
                tmp_remove = this_block.replace("```", "")
                html_line.append(LeafNode("div", f"<pre><code>{tmp_remove}</code></pre>"))
            case BlockType.QUOTE:
                #tag "blockquote"
                quote = ""
                for quoteline in this_block.split('>'):
                    quote += quoteline

                html_line.append(LeafNode("blockquote", f"{quote}"))    
                #print(f"MARK 2: {this_block}")
            case BlockType.UNORDERED_LIST:
                test=1
            case BlockType.ORDERED_LIST:
                test=1
    
    #print(f"TYPE html_line:{html_line}")
    return ParentNode("html", html_line)
    #tag=None,value=None,children=None,props=None

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    for this_block in markdown_blocks:
          match block_to_block_type(this_block):
            case BlockType.HEADING:
                return this_block.strip('#"')

    raise Exception("Missing Title")
