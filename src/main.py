import sys
from file_helpers import add_files, remove_files, generate_page, generate_pages_recursive
import os
from markdown import markdown_to_html_node, extract_title

def main():
#	md = """
#		#THIS IS THE TITLE
#
#		```
#		This is text that _should_ remain
#		the **same** even with inline stuff
#		```
#
#		This is **bolded** paragraph
#		text in a p
#		tag here
#
#		This is another paragraph with _italic_ text and `code` here
#	"""
#	node = markdown_to_html_node(md)
#	html = node.to_html()
#	print(f"HTML->{html}")

#	print(f"TITLE:{extract_title(md)}")



	if len(sys.argv) != 4:
		print("Usage: main.sh [image_source_path] [destination_path] [content_source_path]")
		os._exit(1)

	if sys.argv[1] == sys.argv[2] or sys.argv[3] == sys.argv[2]:
		print("Source and Destination cannot be the same")
		os._exit(2)

	print(f"Start: Image Source:{sys.argv[1]}, Destination:{sys.argv[2]}, Content Source:{sys.argv[3]} ")
	remove_files(sys.argv[2])
	add_files(sys.argv[1], sys.argv[2])

	generate_pages_recursive(sys.argv[3], "template.html", sys.argv[2])
	#generate_page("content/index.md", "template.html", "public/index.html")

#Only run if this file is called directly
if __name__ == "__main__":
	main()
