# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CommentItem(Item):
    # define the fields for your item here like:
    # name = Field()
    tid = Field()
    name = Field()
    bid = Field()
    url = Field()
    content = Field()
    pass

class WebItem(Item):
	url = Field()
	content = Field()
	pass
	
class CC98Item(Item):
	bid = Field()
	tid = Field()
	pass