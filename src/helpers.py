from textnode import TextNode
from enums import TextType, BlockType
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href" : text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
		case _:
			raise Exception("invalid TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        ind=0
        found_ind = 0
        del_len = len(delimiter)
        local_text = node.text
        while ind < len(node.text) and len(new_nodes) < 10:
            found_ind = local_text[ind:].find(delimiter)
            #do we need to make a default type for the missed data
            if found_ind > 0:
                #yes we do
                new_nodes.append(TextNode(local_text[ind: found_ind], node.text_type))
            #No more matches    
            if found_ind == -1 and ind < len(node.text):
                new_nodes.append(TextNode(local_text[ind:], node.text_type))
                ind = len(node.text)
            else:
                #Increment the ind to the found ind to get the start, add 1 to skip the tag
                ind = found_ind+del_len

                #Check for a dangling delimeter
                if ind >= len(local_text) or local_text[ind:].find(delimiter) == -1:
                    raise Exception(f"Missing tag: {delimiter}")
                
                #Get substring for tag
                end_ind = local_text[ind:].find(delimiter) + ind
                new_nodes.append(TextNode(local_text[ind:end_ind], text_type))

                #increment the index location
                ind = end_ind+del_len

    return new_nodes

def extract_markdown_images(text):
    	return re.findall(r"(?:!\[)([\w* \w*]+)(?:\])\((https://[-%_.!~*';/?:@&=+$,A-Za-z0-9]+)\)", text)

def extract_markdown_links(text):
     return re.findall(r"(?:\[)([\w* \w*]+)(?:\])\((https://[-%_.!~*';/?:@&=+$,A-Za-z0-9]+)\)", text)

def split_link_images(old_nodes, text_type):
    new_nodes = []
    #Looks like we only support 1 item from the test scenario??
    for node in old_nodes:
        if node.text_type == TextType.TEXT:  
            #sub_node = []
            #Now build our new delimiter
            del_list=[]
            delim_formatter = lambda x,y: f"{x},{y}"
            match text_type:
                case TextType.LINK:
                        del_list = extract_markdown_links(node.text)
                        delim_formatter = lambda x,y: f"[{x}]({y})"
                case TextType.IMAGE:
                        del_list = extract_markdown_images(node.text)  
                        delim_formatter = lambda x,y: f"![{x}]({y})"    
            #print(f"DELIMS:{del_list}")
            ind = 0
            for delim in del_list:
                #Now build new delimiter
                new_del = delim_formatter(delim[0], delim[1])
                partial_len = node.text.find(new_del)

                #We need to add the previous part as text
                if partial_len > 0:
                    new_nodes.append(TextNode(node.text[ind:partial_len], TextType.TEXT))
                #Now add the delimeter as an entity - need to add extra stuff as needed

                new_nodes.append(TextNode(delim[0], text_type, delim[1]))    

                #update starting search position  
                ind = partial_len+len(new_del)

            #Now add any leftovers
            if ind < len(node.text):
                new_nodes.append(TextNode(node.text[ind:], TextType.TEXT)) 

            #new_nodes.append(sub_node)      
            #print(f"NEW NODES:{new_nodes}")      
        else:
              #Skip it
              new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
     return split_link_images(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_link_images(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    node_list = []
    #Get the images first
    node_list = split_nodes_image([TextNode(text, TextType.TEXT)])

    #print(f"IMAGE : {node_list}")
    #Get the Links next
    node_list = split_nodes_link(node_list)
    #print(f"IMAGE : {node_list}")


    #Get the Code next, BOLD, ITALIC
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)



    #return
    return node_list
    
