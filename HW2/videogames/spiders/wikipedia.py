import scrapy


class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Category:Video_games_by_year']

    def parse(self, response):
        CATEGORY_LINK_SELECTOR = '.CategoryTreeItem a ::attr(href)'
        for link in response.css(CATEGORY_LINK_SELECTOR).getall():
            if not link.split('/')[2].startswith('Category:V'):
                yield scrapy.Request(
                    response.urljoin(link),
                    callback=self.parse_page
                )
        # yield from response.follow_all(response.css(CATEGORY_LINK_SELECTOR), callback=self.parse_page)

    def parse_page(self, response):
        CATEGORY_GROUP_SELECTOR = '.mw-category-group'
        for category_group in response.css(CATEGORY_GROUP_SELECTOR):
            TITLE_SELECTOR = './/ul/li/a/@title'
            for title in category_group.xpath(TITLE_SELECTOR).getall():
                yield {
                    'name': title
                }

