from scrapy.spider import BaseSpider
from scrapy.http import *
from scrapy.selector import HtmlXPathSelector
from cm.items import CC98Item
from cm.items import WebItem
from cm.items import CommentItem
import math

class Cc98Spider(BaseSpider):
    name = 'cc98'
    start_urls = ['http://www.cc98.org/login.asp']
    list_url = 'http://www.cc98.org/customboard.asp'
    id_list = [
        #144, 152, 537, 135, 100, 306, 357, 275, 262, 477, 
        146, 
        241, 68, 562, 15, 182, 141, 114, 198, 247, 
        234, 376, 197, 186, 86, 179, 126, 294, 487, 239, 147, 285, 295, 353, 422, 563, 81, 158, 189, 
        314, 148, 164, 352, 490, 497, 258, 232, 155, 421, 474, 484, 80, 226, 122, 504, 16, 248, 296, 217, 
        180, 329, 60, 320, 142, 480, 229, 235, 192, 173, 459, 246, 471, 30, 214, 328, 284, 316, 479, 
        496, 91, 193, 557, 58, 399, 170, 319, 500, 506, 341, 290, 116, 472, 347, 119, 25, 266, 269, 252, 
        488, 417, 28, 489, 476, 572, 481, 344, 263, 401, 345, 377, 212, 181, 255, 351, 334, 330, 374, 157, 
        233, 77, 465, 139, 403, 371, 505, 482, 507, 509, 467, 102, 593, 478, 583, 312, 310, 101, 462, 
        560, 282, 115, 391, 405, 437, 176, 236, 191, 283, 318, 188, 74, 231, 169, 493, 104, 221, 431, 580, 
        486, 39, 475, 315, 222, 40, 203, 278, 145, 515, 57, 67, 128, 276, 261, 468, 502, 483, 361, 567, 549, 
        430, 596, 165, 321, 495, 270, 406, 136, 251, 447, 464, 469, 200, 99, 274, 569, 288, 75, 499, 438, 
        166, 273, 118, 271, 355, 26, 326, 498, 129, 267, 545, 17, 592, 627, 249, 491, 196, 88, 492, 327, 
        594, 584, 331, 570, 190, 630, 358, 206, 550, 435, 587, 308, 585, 508, 518, 194, 216, 286, 256, 503, 
        339, 230, 324, 393, 277, 178, 449, 272, 202, 598, 313, 473, 551, 211, 519, 304, 281, 244, 105, 566, 
        323, 184, 187, 254, 443, 260, 402, 455, 571, 392, 576, 573, 264, 209, 538, 520, 268, 433, 85, 297, 
        564, 250, 333, 362, 48, 547, 622, 369, 385, 713, 621, 372, 628, 616, 404, 195, 618, 19, 511, 223, 
        245, 354, 436, 625, 642, 460, 558, 394, 379, 9, 591, 72, 434, 546, 599, 617, 586, 605, 84, 536, 595, 
        253, 375, 103, 154, 561, 335, 383, 711, 623, 336, 340, 303, 257, 350, 337, 322, 552, 446, 411, 20, 
        225, 450, 47, 346, 601, 382, 287, 535, 210, 606, 50, 614, 448, 445, 624, 7, 213, 305, 227, 373, 279, 
        589, 215, 183, 311, 207, 41, 414, 444, 636, 124, 219, 208, 615, 588, 349, 453, 620, 21, 395, 397, 
        710, 539, 717, 415, 540, 140, 626, 610, 325, 578, 574, 634, 413, 721, 555, 451, 597, 722, 611, 425, 
        579, 470, 426, 719, 83, 292, 716, 224, 204, 553, 637, 42, 300, 666, 602, 675, 151, 613, 452, 514, 
        454, 698, 720, 359, 714, 548, 696, 149, 655, 640, 52, 440, 718, 416, 510, 697, 631, 603, 544, 668, 
        656, 662, 501, 410, 661, 657, 680, 424, 633, 654, 678, 674, 348, 673, 632, 665, 692, 658, 23, 36, 
        667, 664, 663, 516, 38, 695, 701, 689, 568, 672, 671, 669, 679, 150, 708, 660, 629, 429, 457, 517, 
        332, 612, 681, 693, 694, 699, 494, 513, 559, 428, 702, 712, 677, 659, 670, 707, 700, 709, 691, 687, 
        688, 676, 607, 565, 432, 600, 703, 49, 51, 31, 32, 34, 22, 132, 133, 134, 127, 364, 386, 396, 407, 
        409, 293, 704, 705, 706, 690, 590, 608, 418, 419, 441, 439, 466, 577, 556, 512, 554]
    new_list = {581:100, 485:5, 135:350, 152:110, 307:15}

    def __init__(self, username = None, password = None):
        self.username = username
        self.password = password
        pass

    def parse(self, response):
        return [FormRequest.from_response(response,
                    formdata={'username': self.username, 'password': self.password},
                    cookies={'cc98Simple':1},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        filename = response.url.split("/")[-1]
        open(filename, 'wb').write(response.body)
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        for i in self.id_list:
            board_url = 'http://www.cc98.org/list.asp?boardid=%s' % i
            request = Request(url = board_url, callback = self.parse_board)
            request.meta['bid'] = i
            yield request
    
    def parse_boardid(self, response):
        filename = response.url.split("/")[-1]
        open(filename, 'wb').write(response.body)
        x = HtmlXPathSelector(response)
        for link in x.select('//a[contains(@href, "list.asp")]/@href'):
            #board_url = 'http://www.cc98.org/%s' % link.select('@href').extract_unquoted()[0]
            print link.re(r'boardid=(\d+)')
            #yield Request(url = board_url, callback = self.parse_board)

    def parse_board(self, response):
        #if "topic_" in response.body:
        x = HtmlXPathSelector(response)
        bid = response.meta['bid']
        page_count = min(int(x.re(r'<\/b>\/<b>(\d+)')[0]), 30)
        for page_index in range(1,page_count):
            yield Request(url = response.url + '&page=%i' % page_index, callback = self.parse_board_page)
            
    def parse_board_page(self, response):
        x = HtmlXPathSelector(response)
        bid = x.re(r'var currentBoardID = (\d+)')[0]
        for tid in x.re(r'topic_(\d+)'):
        	url = 'http://www.cc98.org/dispbbs.asp?boardid=%s&id=%s' % (bid, tid)
        	yield Request(url = url, callback = self.parse_thread)
        	
    def parse_thread(self, response):
        x = HtmlXPathSelector(response)
        topic_num = int(x.select("//span[@id='topicPagesNavigation']/b/text()").extract()[0])
        star_num = int(math.ceil(topic_num / 10.))
        for i in range(1,star_num + 1):
            url = response.url + '&star=%s' % i
            yield Request(url = url, callback = self.parse_thread_page)
        

    def parse_thread_page(self, response):
        items = []
        x = HtmlXPathSelector(response)
        topics = x.select("//table[@cellpadding=5]")
        for t in topics:
            item = CommentItem()
            #item['name'] = t.select(".//a[@name]/font/b/text()").extract()[0]
            item['name'] = t.select(".//blockquote//div[@class='usernamedisp']/b/a/text()").extract()[0]
            item['url'] = response.url
            item['content'] = t.select(".//blockquote//span[contains(@id, 'ubbcode')]").extract()[0]
            items.append(item)
            pass
        return items

