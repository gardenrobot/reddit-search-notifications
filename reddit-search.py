import sys
import urllib
import lxml
from lxml import etree
import datetime
from dateutil import parser
import pytz
# TODO make good readme
# TODO user agent fix

url_template = 'https://www.reddit.com/r/{}/search?q={}&restrict_sr=on&include_over_18=on&sort=new&t=all'

user_agent = 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0'

meta_xpath = '//div[@class="search-result-meta"]'

# TODO read from somewhere
most_recent = datetime.datetime(2017, 11, 1, tzinfo=pytz.utc)

def main(subs, search):
    subs_encode = '+'.join(subs.split(','))
    search_encode = urllib.quote_plus(search)
    url = url_template.format(subs_encode, search_encode)

    req = urllib.urlopen(url)
    res_tree = etree.HTML(req.read())
    posts = res_tree.xpath(meta_xpath)
    if len(posts) == 0:
        print 'No posts found'

    unread_posts = posts
    for post in posts:
        if get_date(post) > most_recent:
            print get


def get_date(post_tree):
    time = post_tree.xpath('.//span[@class="search-time"]/time/@datetime')[0]
    return parser.parse(time)


if len(sys.argv) != 3:
    print 'Usage: python reddit-search.py [subreddits] [search string]'
    sys.exit
main(sys.argv[1], sys.argv[2])

