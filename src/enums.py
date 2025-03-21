from enum import Enum

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"

class TextType(Enum):
	TEXT="normal"
	BOLD="bold"
	ITALIC="italic"
	CODE="code"
	LINK="link"
	IMAGE="image"