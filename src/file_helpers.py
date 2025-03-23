import shutil
import os
from markdown import extract_title, markdown_to_html_node

def add_files(location_from, location_to):
	print(f"Adding files and directories from: {location_from}")
	if not os.path.exists(location_from):
		raise Exception(f"Location not found: {location_from}")
	if not os.path.exists(location_to):
		raise Exception(f"Location not found: {location_to}")

	files = os.listdir(location_from)
	for file in files:
		s_file_with_path = f"{location_from}/{file}"
		d_file_with_path = f"{location_to}/{file}"
		#Could add exception catching but not right now
		if os.path.isdir(s_file_with_path):
			print(f"copy directory: {s_file_with_path} to {d_file_with_path}")
			shutil.copytree(s_file_with_path, d_file_with_path, copy_function = shutil.copy)
		else:
			print(f"copy file: {s_file_with_path} to {d_file_with_path}")
			shutil.copy(s_file_with_path, d_file_with_path)

def remove_files(location_to_delete):
	print(f"Delete from inside: {location_to_delete}")
	
	if not os.path.exists(location_to_delete):
		raise Exception(f"Location not found: {location_to_delete}")
	
	files = os.listdir(location_to_delete)
	for file in files:
		file_with_path = f"{location_to_delete}/{file}"
		#print(f"Delete: {file_with_path}")
		if os.path.isdir(file_with_path):
			try:
				shutil.rmtree(file_with_path)
				print(f"Directory '{file_with_path}' deleted.")
			except PermissionError:
				print(f"Error: Permission denied -> '{file_with_path}'.")
			except Exception as e:
				print(f"Error: Unknown-> {e}")			
		else:
			try:
				os.remove(file_with_path)
				print(f"File '{file_with_path}' deleted.")
			except PermissionError:
				print(f"Error: Permission denied -> '{file_with_path}'.")
			except Exception as e:
				print(f"Error: Unknown -> {e}")			

def generate_page(basepath, from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"Markdown file not found: {from_path}")	
    if not os.path.exists(from_path):
        raise Exception(f"Template file not found: {template_path}")
	#File does not exist yet
    #if not os.path.exists(dest_path):
    #    raise Exception(f"Markdown file not found: {dest_path}")
	
    #Read from to get md file, get title and content
    markdown = ""
    try:
        with open(from_path, "r") as file:
            markdown = file.read()
            # content now holds the entire file content as a string
            #print(f"MARKDOWN: {markdown}")
    except IOError as e:
        raise Exception(f"An error occurred: {e}")
	
    #Read template and insert title and content	
    template = ""
    try:
        with open(template_path, "r") as file:
            template = file.read()
            # content now holds the entire file content as a string
            #print(f"TEMPLATE: {template}")
    except IOError as e:
        raise Exception(f"An error occurred: {e}")

	#Get Title and body - default to error string on failure
    title = ""
    try:	
        title = extract_title(markdown)
    except Exception as e:
        title = e

    body = ""
    try:	
        body = markdown_to_html_node(markdown).to_html()
    except Exception as e:
        body = e        

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", body)
    #Update images and links to add basepath
    template = template.replace("href=\'/", f"href='{basepath}/")
    template = template.replace("src=\'/", f"src='{basepath}/")


    #print(f"FULL BODY: {template}")
	
	
	#Write  dest_path for the default url page
    file = open(dest_path, "w")
    file.write(template)
	
def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Base Markdown directory not found: {dir_path_content}")	
    if not os.path.exists(template_path):
        raise Exception(f"Template file not found: {template_path}")	
    if not os.path.exists(dest_dir_path):
        raise Exception(f"Destination for files: {dest_dir_path}")	

    files = os.listdir(dir_path_content)
    for file in files:
        new_base = f"{dir_path_content}/{file}"
        new_dest = f"{dest_dir_path}/{file}"  

		#Could add exception catching but not right now
        if os.path.isdir(new_base):
            print(f"New directory: {new_base} to {new_dest}")
            os.mkdir(new_dest)
            generate_pages_recursive(basepath, new_base, template_path, new_dest)
        else:
            if ".md" in file:
                #Read in and write using generate_page - change .md to .html
                new_dest = new_dest.replace(".md", ".html")

                print(f"Copy file: {new_base} to {new_dest}")
                #shutil.copy(new_base, new_dest)
                generate_page(basepath, new_base, template_path, new_dest)

    return ""    