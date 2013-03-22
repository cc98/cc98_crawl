# Scrapy settings for cm project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'cm'

SPIDER_MODULES = ['cm.spiders']
NEWSPIDER_MODULE = 'cm.spiders'
ITEM_PIPELINES = [
    'cm.pipelines.MySqlPipeline'
]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cm (+http://www.yourdomain.com)'
