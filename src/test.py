import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import time
import json
from pyquery import PyQuery as pq
from lxml import etree

page = 1
baseUrl = 'http://www.qiushibaike.com'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}


def urlFormat(url):
    if str(url).startswith('//'):
        return 'http:' + url
    elif str(url).startswith('/'):
        return baseUrl + url
    elif str(url).startswith('http://') or str(url).startswith('https://'):
        return url
    return baseUrl


for index in range(10):
    page = index + 1
    url = baseUrl + '/hot/page/' + str(page)
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    print('pulling page ' + str(page))
    doc = pq(response.read())
    articleList = []
    content = doc('#content-left')
    content.children('contentForAll').clear()
    articles = content.children().filter('.article')
    for i in range(articles.size()):
        content = articles.eq(i).children('.contentHerf')
        a = {
            'text': content.text(),
            'url': urlFormat(content.attr('href')),
            'image': []
        }
        imgTags = articles.eq(i).children('.thumb a img')
        for j in range(imgTags.size()):
            imaTag = imgTags.eq(j)
            img = {'url': urlFormat(imaTag.attr('src')), 'alt': imaTag.attr('alt')}
            a['image'].append(img)
        articleList.append(a)

    fhandle = open("./" + str(index) + ".json", "w")
    fhandle.write(json.dumps(articleList))
    fhandle.close()
    time.sleep(1)
