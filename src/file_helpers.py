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

def generate_page(from_path, template_path, dest_path):
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
    #print(f"FULL BODY: {template}")
	
	
	#Write  dest_path for the default url page
    file = open(dest_path, "w")
    file.write(template)
	