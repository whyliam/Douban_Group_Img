#!/usr/bin/python
# coding=utf-8
import urllib
import urllib2
import cookielib
import re
import time
import random
from datetime import datetime


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


def post(url, data, cj):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    response = opener.open(req, data)
    # DEBUG AREA
    if debug >= 1:
        print 'POST_REQUEST:\n' + url
        print 'POST_CONTENT:\n' + data
    return response.read()


def browse(url, cj):
    try:
        req = urllib2.Request(url)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        if debug > 4:
            print 'BROSWE_REQUEST:\n' + url
            print 'BROSWE_RESPONSE:\n' + response.read()
        return response.read()
    except:
        return ''


def downImg(url, name):
    fr = urllib.urlopen(url)
    stream = fr.read(-1)
    fr.close()
    fw = open('picture/' + name, 'w')
    fw.write(stream)
    fw.close()


def main():
    du = 'http://m.douban.com'

    # set Group ID
    group_id = 'haixiuzu'
    # set refresh_interval
    refresh_interval = 1
    # set form_email, and form_password
    data = {'form_email': 'liamzhuce@gmail.com',
            'form_password': '********', 'action': '/'}
    # set group all_pages
    all_pages = 2000

    # login
    try:
        post(du, data, cj)
    except:
        print 'FATAL'
        exit(0)
    times = 0
    
    for page in range(1, all_pages)[::-1]:
        # Get Groups
        group_content = browse(
            du + '/group/' + group_id + '/topics?page=' + str(page), cj)
        print page
        replace_dict = {'\n': '', '\t': '', ' ': '', '　': ''}
        group_content = replace_all(group_content, replace_dict)
        if debug >= 1:
            print group_content
        if times == 0:
            group_title = re.findall('<title>(.*)<\/title>', group_content)[0]
            print '\n-----download "' + group_title + '"ing-----'
            times += 1
        items = re.findall(
            '<ahref="\/group\/topic\/(\d+)\/\?session=\w+">([^<]+)<\/a><span>\((\d+)\)\|', group_content)

        if not items.__len__() == 0:
            # print items
            for i in items:
                item_title = i[1]
                item_title = item_title.replace('/', '')
                item_ID = i[0]
                item_comm = i[2]
                if int(item_comm) > 80:
                    print item_title + ' | ' + item_comm
                    item_url = du + '/group/topic/' + item_ID + '/'
                    item_content = browse(item_url, cj)
                    img_content = replace_all(item_content, replace_dict)
                    imgs = re.findall(
                        '<imgsrc="([^<]*)\.jpg', img_content)
                    if not imgs.__len__() == 0:
                        num = 0
                        for img_url in imgs:
                            num = num + 1
                            img_url = img_url.replace('small', 'large')
                            filename = str(item_title) + str(num) + '.jpg'
                            try:
                                downImg(img_url + '.jpg', filename)
                            except:
                                pass
                    time.sleep(refresh_interval * random.randint(2, 5))

        if debug == 1:
            time.sleep(refresh_interval)
        else:
            time.sleep(refresh_interval * random.randint(3, 7))


if __name__ == '__main__':
    cj = cookielib.CookieJar()
    debug = 0
    main()
