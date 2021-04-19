import scrapy
import datetime

# base url
# TODO: use list of keywords to search for instead of single one
search_phrase = 'data+science'
# use indeeds inbuilt filter function to filter job ads
filter_ads = False
# sort by date; show job ads from last 7 days
base_url = 'https://de.indeed.com/jobs?q={}&sort=date&fromage=7{}'.format(search_phrase, '' if filter_ads else '&filter=0')

def count_back_days(time, count_back_days):
    date_counted_back = time - datetime.timedelta(days=count_back_days)
    return date_counted_back.strftime('%Y-%m-%d')

def get_date(age_value):
    now = datetime.datetime.now()
    if age_value == 'Gerade veröffentlicht':
        return count_back_days(now, 0)
    elif age_value == 'Heute':
        return count_back_days(now, 0)
    elif age_value == 'vor 1 Tag':
        return count_back_days(now, 1)
    elif age_value == 'vor 2 Tagen':
        return count_back_days(now, 2)
    elif age_value == 'vor 3 Tagen':
        return count_back_days(now, 3)
    elif age_value == 'vor 4 Tagen':
        return count_back_days(now, 4)
    elif age_value == 'vor 5 Tagen':
        return count_back_days(now, 5)
    elif age_value == 'vor 6 Tagen':
        return count_back_days(now, 6)
    elif age_value == 'vor 7 Tagen':
        return count_back_days(now, 7)

class JobSpider(scrapy.Spider):

    name = 'jobs'

    # for each page append (page number - 1) * 10
    # e.g.: page 1: 0, page 2: 10, page 15: 140
    # highest possible page number: 100
    # TODO: use list of keywords to search for instead of single one
    start_urls = [base_url]
    
    def parse(self, response):
        for job in response.xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result"]'):
            yield {

                'title': job.xpath('normalize-space(.//a/@title)').get(),

                # company names are sometimes nested inside <a> tags
                # //text() gets text inside <a> tags too
                # [string-length() > 2] ignores texts only containing "\n"
                'company': job.xpath('normalize-space(.//span[@class="company"]//text()[string-length()>2])').get(),

                # <span> & <div> tags are used for location
                # * allows for both
                'location': job.xpath('.//*[@class="location accessible-contrast-color-location"]/text()').get(),

                'salary': job.xpath('normalize-space(.//span[@class="salaryText"]/text())').get(),

                # descriptions are unorderd lists
                # sometimes <b> tags are used inside the <li> tags
                # //text() gets text inside <b> tags too
                #
                # then turn list into string
                'description': ''.join(job.xpath('.//div[@class="summary"]/ul/li//text()').getall()),

                # use get_date function to turn age string into format "yyyy-mm-dd"
                'date': get_date(job.xpath('.//span[@class="date date-a11y"]/text()').get()),
            }
        next_page = response.xpath('.//nav//a[@aria-label="Weiter"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
