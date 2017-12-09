import sys
import urllib
import urllib2
from lxml import etree
from dateutil import parser
import pytz
import os
import time
import datetime


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

URL_TEMPLATE = 'https://www.reddit.com/r/{}/search?q={}&restrict_sr=on&include_over_18=on&sort=new&t=all'

# User Agent for http calls
USER_AGENT = 'Mozilla/5.0'

# 1 hour, sleep timer
INTERVAL = 3600

# extract all search results
META_XPATH = '//div[@class="search-result-meta"]'

# extract data from single search result
POST_DATE_XPATH = './/span[@class="search-time"]/time/@datetime'
POST_LINK_XPATH = './/a/@data-href-url'

# name of config file
CONFIG_FILE = 'config'

def main(subs, search, most_recent):
    # Create url
    subs_encode = '+'.join(subs.split(','))
    search_encode = urllib.quote_plus(search)
    url = URL_TEMPLATE.format(subs_encode, search_encode)

    # Get html
    res = make_request(url)
    res_tree = etree.HTML(res)
    posts = res_tree.xpath(META_XPATH)

    if len(posts) == 0:
        print 'No posts found'

    # Posts made after most_recent
    new_posts = [post for post in posts if get_date(post) > most_recent]

    if len(new_posts) == 0:
        print 'No new posts found'
    else:
        print 'New posts'
        for post in new_posts:
            notify(get_link(post))


# Return post date
def get_date(post_tree):
    time = post_tree.xpath(POST_DATE_XPATH)[0]
    return parser.parse(time)

# Return link to post
def get_link(post_tree):
    link = post_tree.xpath(POST_LINK_XPATH)[0]
    return link

# Display notification. Linux specific.
def notify(link):
    os.system('notify-send -u critical {}'.format(link))

# Return html from given url
def make_request(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', USER_AGENT)]
    res = opener.open(url).read()
    return res

# Rewrite config but with most_recent set to now.
def mark_read(subs, search, most_recent):
    with open(os.path.join(BASE_DIR, CONFIG_FILE), 'w') as f:
        f.write(subs + os.linesep)
        f.write(search + os.linesep)
        f.write(str(pytz.utc.localize(datetime.datetime.utcnow())))

# Return values from config
def read_config():
    with open(os.path.join(BASE_DIR, CONFIG_FILE)) as f:
        subs = f.readline().strip()
        search = f.readline().strip()
        most_recent = parser.parse(f.readline())
    return (subs, search, most_recent)

if len(sys.argv) == 2 and sys.argv[1] == '-r':
    subs, search, most_recent = read_config()
    mark_read(subs, search, most_recent)
elif len(sys.argv) == 1:
    while True:
        subs, search, most_recent = read_config()
        main(subs, search, most_recent)
        time.sleep(INTERVAL)
else:
    print 'Usage: python reddit-search.py [-r]'
    sys.exit()

