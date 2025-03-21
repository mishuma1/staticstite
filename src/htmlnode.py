
class HTMLNode:
	def __init__(self, tag=None,value=None,children=None,props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("not implemented")
	def props_to_html(self):
		ret_str = ""
		if self.props != None:
			for i in self.props:
				ret_str += f" {i}=\"{self.props[i]}\""

		return ret_str
	
	def __repr__(self):
		return f"HTMLNode(\"{self.tag}\",\"{self.value}\",\"{self.children}\",\"{self.props}\")"
		
class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		#print("LEAF TO_HTML")
		if self.value == None:
			raise ValueError("All leaf nodes must have a value.")
		if self.tag == None:
			return self.value
		#self.props_to_html(props)
		#print(f"FF:{self.props}")
		return f"<{self.tag + self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		#print("PARENT TO_HTML")
		if self.tag == "":
			raise ValueError("All Parent nodes must have a tag.")
		if self.children == None:
			raise ValueError("All Parent nodes must have a child.")
		
		ret_str = f"<{self.tag}{self.props_to_html()}>"
		for child in self.children:
			ret_str += child.to_html()
		return ret_str	+ f"</{self.tag}>"
	