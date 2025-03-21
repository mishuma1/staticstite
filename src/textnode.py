from enums import TextType

class TextNode():
	def __init__(self, text="", text_type=TextType.TEXT, url=""):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__(self):
		if self.url == None or self.url == "":
			return f"TextNode(\"{self.text}\",\"{self.text_type}\")"
		return f"TextNode(\"{self.text}\",\"{self.text_type}\",\"{self.url}\")"


