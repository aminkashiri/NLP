from gc import callbacks
import scrapy


class GamefaSpider(scrapy.Spider):
    name = "gamefa_spider"
    start_urls = ['https://gamefa.com']

    # COUNT_MAX = 2
    # custom_settings = {
    #         'CLOSESPIDER_PAGECOUNT': COUNT_MAX,
    # }

    # CONCURRENT_REQUEST = 1
    # CLOSESPIDER_PAGECOUNT = 2
    # count = 0

    def parse(self, response):
        # print('-----------------------------------------------------------------')
        # print(response.url)
        # print('self.count ', self.count)
        # if self.count >= self.COUNT_MAX:
        #     return 
        # self.count += 1

        # print('-----------------------------------------------------------------')

        POST_LINK_SELECTOR = '.d-block.px-2 ::attr(href)'
        # for post_link in response.css(POST_LINK_SELECTOR).getall():
        #     print('---------- 1', post_link)

        #     yield scrapy.Request(
        #         response.urljoin(post_link),
        #         callback=self.parse_page
        #     )
        yield from response.follow_all(response.css(POST_LINK_SELECTOR), callback=self.parse_page)
        

        NEXT_PAGE_SELECTOR = '.next.page-numbers ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        
    def parse_page(self, response):
        # print('---------------------------------------- 10')
        CONTENT_SELECTOR = '.content'
        content = response.css(CONTENT_SELECTOR)
        P_SELECTOR = 'p'
        content_string = ''
        for p in content.css(P_SELECTOR):
            TEXT_SELECTOR = '::text'
            content_string += ''.join(p.css(TEXT_SELECTOR).extract()) + ' '
        
        TITLE_SELECTOR = '.py-3.border-bottom.mb-0.px-2::text'
        title = response.css(TITLE_SELECTOR).get()

        TIME_SELECTOR = '.d-block.d-sm-inline-block::text'
        time = response.css(TIME_SELECTOR).get()

        yield {
            'title': title,
            'time':time,
            'content': content_string[:-1]

        }


        


