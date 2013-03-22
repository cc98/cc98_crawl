# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
import datetime
from cm.items import CC98Item

class CmPipeline(object):
    def process_item(self, item, spider):
        return item

class MySqlPipeline(object):
	def __init__(self):
		self.db = MySQLdb.connect(
			host="127.0.0.1", 
			user="root", 
			db="cc98",
			passwd = '123',
			charset = 'utf8',
			use_unicode = True
		)
		self.cursor = self.db.cursor()

	def process_item(self, item, spider):
		#print item['tid'], item['bid']
		print self.cursor.execute("INSERT INTO comm(un, url, content) VALUES (%s, %s, %s);", (item['name'], item['url'],item['content']))
		self.db.commit()
		return item

	def close_spider(self, spider):
		self.db.commit()
		self.cursor.close()
		self.db.close()
