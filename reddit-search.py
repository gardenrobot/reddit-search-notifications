import sys
import urllib
import lxml
from lxml import etree
import datetime
from dateutil import parser
import pytz
# TODO fix bug where there is one subreddit
# TODO display links as notifications
# TODO run in background

# TODO use base dir
# TODO user agent fix
# TODO make good readme

url_template = 'https://www.reddit.com/r/{}/search?q={}&restrict_sr=on&include_over_18=on&sort=new&t=all'

user_agent = 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0'

meta_xpath = '//div[@class="search-result-meta"]'

def main(subs, search, most_recent):
    subs_encode = '+'.join(subs.split(','))
    search_encode = urllib.quote_plus(search)
    url = url_template.format(subs_encode, search_encode)

    res = make_request_fake(url)

    res_tree = etree.HTML(res)
    posts = res_tree.xpath(meta_xpath)
    if len(posts) == 0:
        print 'No posts found'

    new_posts = []
    for post in posts:
        if get_date(post) > most_recent:
            link = get_link(post)
            new_posts.append(link)
    if len(new_posts) > 0:
        print 'New posts'
        for post in new_posts:
            print post


# Return post date
def get_date(post_tree):
    time = post_tree.xpath('.//span[@class="search-time"]/time/@datetime')[0]
    return parser.parse(time)

# Return link to post
def get_link(post_tree):
    link = post_tree.xpath('.//a/@data-href-url')[0]
    return link

# Return html from given url
def make_request(url):
    req = urllib.urlopen(url)
    res = req.read()
    return res

# For testing
def make_request_fake(url):
    with open('test.html') as f:
        return f.read()

def mark_read(subs, search, most_recent):
    with open('data', 'w') as f:
        f.write(subs)
        f.write(search)
        f.write(str(pytz.utc.localize(datetime.datetime.utcnow())))

with open('data') as f:
    subs = f.readline()
    search = f.readline()
    most_recent = parser.parse(f.readline())

if len(sys.argv) == 2 and sys.argv[1] == '-r':
    mark_read(subs, search, most_recent)
elif len(sys.argv) == 1:
    main(subs, search, most_recent)
else:
    print 'Usage: python reddit-search.py [-r]'
    sys.exit

