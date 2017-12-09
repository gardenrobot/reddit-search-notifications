import sys
import urllib
import urllib2
from lxml import etree
from dateutil import parser
import pytz
import os
import time


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

URL_TEMPLATE = 'https://www.reddit.com/r/{}/search?q={}&restrict_sr=on&include_over_18=on&sort=new&t=all'

USER_AGENT = 'Mozilla/5.0'

META_XPATH = '//div[@class="search-result-meta"]'

INTERVAL = 3600 # 1 hour

POST_DATE_XPATH = './/span[@class="search-time"]/time/@datetime'

POST_LINK_XPATH = './/a/@data-href-url'

CONFIG_FILE = 'config'

def main(subs, search, most_recent):
    subs_encode = '+'.join(subs.split(','))
    search_encode = urllib.quote_plus(search)
    url = URL_TEMPLATE.format(subs_encode, search_encode)

    res = make_request(url)

    res_tree = etree.HTML(res)
    posts = res_tree.xpath(META_XPATH)
    if len(posts) == 0:
        print 'No posts found'

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

# linux specific
def notify(link):
    os.system('notify-send -u critical {}'.format(link))

# Return html from given url
def make_request(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', USER_AGENT)]
    res = opener.open(url).read()
    return res

# For testing
def make_request_fake(url):
    with open(os.path.join(BASE_DIR, 'test.html')) as f:
        return f.read()

def mark_read(subs, search, most_recent):
    with open(os.path.join(BASE_DIR, CONFIG_FILE), 'w') as f:
        f.write(subs)
        f.write(search)
        f.write(str(pytz.utc.localize(datetime.datetime.utcnow())))

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

