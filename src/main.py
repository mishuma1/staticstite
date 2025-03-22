import sys
from file_helpers import add_files, remove_files, generate_page
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



	if len(sys.argv) != 3:
		print("Usage: main.sh [source_path] [destination_path]")
		os._exit(1)

	if sys.argv[1] == sys.argv[2]:
		print("Source and Destination cannot be the same")
		os._exit(2)

	print(f"Start: Source:{sys.argv[1]}, Destination:{sys.argv[2]}")
	remove_files(sys.argv[2])
	add_files(sys.argv[1], sys.argv[2])

	generate_page("content/index.md", "template.html", "public/index.html")

#Only run if this file is called directly
if __name__ == "__main__":
	main()
