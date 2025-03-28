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
            return LeafNode("`", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            print(f"URL AA:{text_node.url}")
            return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
        case _:
            raise Exception("invalid TextType")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            #print(f"NODE TEXT A: {node.text}")
            ind=0
            found_ind = 0
            end_ind = 0
            del_len = len(delimiter)
            #local_text = node.text
            while ind < len(node.text) and found_ind != -1:
                #print(f"ZZZZ: {node.text[ind:]}, DELIM:{delimiter}")
                #print(f"ZZZZ: {node.text[ind:].find(delimiter)}")
                found_ind = node.text[ind:].find(delimiter)
                if found_ind != -1:
                    found_ind += ind
                    found_ind = node.text[ind:].find(delimiter) + ind
                    #print(f"A node.text: |{node.text[ind:]}|, LEN A:{len(node.text)}, INDEX:{ind}, FOUND: {found_ind}, END: {end_ind}")
                    #do we need to make a default type for the missed data
                    if found_ind > 0:
                        #yes we do
                        new_nodes.append(TextNode(node.text[ind: found_ind], node.text_type))
                        #print(f"AA node.text: |{node.text[ind: found_ind+ind]}|, LEN B:{len(node.text)}, INDEX:{ind}, FOUND: {found_ind}, END: {end_ind}")
                        
                        #print(f"A: {node.text[ind: found_ind+ind]}")
                    #No more matches    

                    if found_ind >= 0:
                        #Increment the ind to the found ind to get the start, add 1 to skip the tag
                        ind = found_ind+del_len

                        #Check for a dangling delimeter
                        #if ind >= len(local_text) or local_text[ind:].find(delimiter) == -1:
                        #    raise Exception(f"Missing tag: {delimiter}")
                        
                        #Get substring for tag
                        end_ind = node.text[ind:].find(delimiter) + ind
                        print(f"B node.text: |{node.text[ind:]}|, LEN B:{len(node.text)}, INDEX:{ind}, FOUND: {found_ind}, END: {end_ind}")
                        
                        new_nodes.append(TextNode(node.text[ind:end_ind], text_type))
                        print(f"B: {node.text[ind:end_ind]}")

                        #increment the index location
                        ind = end_ind+del_len
                        print(f"LEN C:{len(node.text)}, INDEX:{ind}, FOUND: {found_ind}, END: {end_ind}")
                    #print("DONE")

            if ind < len(node.text):
                new_nodes.append(TextNode(node.text[ind:], node.text_type))
                #print(f"ZZZZ C: {node.text[ind]}")
                ind = len(node.text)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    print(f"extract_markdown_images: {text}")
    return re.findall(r'!\[(\w.*)\]\((.*)\)', text)

def extract_markdown_links(text):
    return re.findall(r'\[(\w.*)\]\((.*)\)', text)

def split_link_images(old_nodes, text_type):
    new_nodes = []
    #print(f"BB TextType:{text_type}")
    #Looks like we only support 1 item from the test scenario??
    for node in old_nodes:
        print(f"node:{node}")
        if node.text_type == TextType.TEXT:  
            #sub_node = []
            #Now build our new delimiter
            del_list=[]
            delim_formatter = lambda x,y: f"{x},{y}"
            #Support for multi entry
            multiples = node.text.split(')')
            found_opening = node.text.split('(')
            #Ignore errant )
            if (len(found_opening) > 0 and len(multiples) > 0):
                #print("AAA1")
                for multi_item in multiples:
                    #adding the divider back in
                    new_text = multi_item + ")"
                    match text_type:    
                        case TextType.LINK:
                                del_list = extract_markdown_links(new_text)
                                #print(f"Inner TextType BB:{text_type},DELIMS:{del_list}, nodetext:{new_text}")
                                delim_formatter = lambda x,y: f"[{x}]({y})"
                        case TextType.IMAGE:
                                del_list = extract_markdown_images(new_text)  
                                #print(f"Inner TextType:{text_type},DELIMS:{del_list}")
                                delim_formatter = lambda x,y: f"![{x}]({y})"    
                    #print(f"TextType:{text_type},DELIMS:{del_list}")


                    ind = 0
                    for delim in del_list:
                        #Now build new delimiter
                        new_del = delim_formatter(delim[0], delim[1])
                        partial_len = new_text.find(new_del)

                        #We need to add the previous part as text
                        if partial_len > 0:
                            #print(f" AA PARTIAL > 0: {new_text[ind:partial_len]}")
                            new_nodes.append(TextNode(multi_item[ind:partial_len], TextType.TEXT))
                        #Now add the delimeter as an entity - need to add extra stuff as needed

                        new_nodes.append(TextNode(delim[0], text_type, delim[1]))    
                        #print(f"TextTypeAA:{text_type},DELIMS:{delim[0]},{delim[1]}")
                        #update starting search position  
                        ind = partial_len+len(new_del)

                    #Now add any leftovers
                    if ind < len(new_text):
                        #print(f"Leftovers AA: {new_text[ind:]}")
                        new_nodes.append(TextNode(multi_item[ind:], TextType.TEXT)) 

                    #new_nodes.append(sub_node)      
                    #print(f"NEW NODES AA:{new_nodes}")      
        else:
            #Skip it
            new_nodes.append(node)
            #print(f"SKIPPING NODES AA:{new_nodes}") 
        #print(f"END NEW NODES AA:{new_nodes}")      
    return new_nodes

def split_nodes_image(old_nodes):
     return split_link_images(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_link_images(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    node_list = []
    #Get the images first
    print(f"ORIG text_to_textnodes:{text}")
    node_list = split_nodes_image([TextNode(text, TextType.TEXT)])

    print(f"text_to_textnodes IMAGE: {node_list}")
    #Get the Links next
    node_list = split_nodes_link(node_list)
    print(f"text_to_textnodes LINK: {node_list}")


    #Get the Code next, BOLD, ITALIC
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    print(f"text_to_textnodes CODE: {node_list}")
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    print(f"text_to_textnodes BOLD: {node_list}")
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    print(f"text_to_textnodes ITALIC: {node_list}")



    #return
    return node_list
    
