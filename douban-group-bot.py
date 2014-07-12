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
        # print
        # 'POST_RESPONSE:\n'+replace_all(response.read(),{'\n':'','\t':'','
        # ':'','　':''})
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
    fw = open('/Users/liam/Dropbox/Project/Douban_group/picture/' + name, 'w')
    fw.write(stream)
    fw.close()


def main():
    du = 'http://m.douban.com'
    # 设置区域
    # set Group ID
    group_id = 'haixiuzu'
    # set refresh_interval
    refresh_interval = 1
    # set sofa Content
    sofa_content = '越过山丘 才发现无人等候 喋喋不休 再也唤不回温柔'
    data = {'form_email': 'liamzhuce@gmail.com',
            'form_password': '1qaZ@wsx', 'action': '/'}
    # 到这就不要修改了，除非你知道你在干吗

    # FIXME Why need one more Login, wired?
    # if browse(du,cj)

    # login
    try:
        post(du, data, cj)
    except:
        print 'FATAL'
        exit(0)
    times = 0
    page = 2500
    for page in range(1, 1797)[::-1]:
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
            print '\n-----抢"' + group_title + '"的沙发中-----'
            times += 1
        items = re.findall(
            '<ahref="\/group\/topic\/(\d+)\/\?session=\w+">([^<]+)<\/a><span>\((\d+)\)\|', group_content)

        if not items.__len__() == 0:
            # print items
            for i in items:
                item_title = i[1]
                item_title = item_title.replace('晒','')
                item_title = item_title.replace('【】','')
                item_title = item_title.replace('/','')
                item_ID = i[0]
                item_comm = i[2]
                if int(item_comm) > 80:
                    # print item_title + '[@' + datetime.now().isoformat() + ']'
                    print item_title+' | '+item_comm
                    item_url = du + '/group/topic/' + item_ID + '/'
                    item_content = browse(item_url, cj)
                    img_content = replace_all(item_content, replace_dict)
                    # print img_content
                    # imgs = re.findall(
                    #     '<ahref="\/group\/topic\/\d+\/photo\?purl=[^<]+\&session=\w+"><imgsrc="([^<]*)"\/>', img_content)
                    imgs = re.findall(
                        '<imgsrc="([^<]*)\.jpg', img_content)
                    if not imgs.__len__() == 0:
                        num = 0
                        for img_url in imgs:
                            num = num + 1
                            img_url = img_url.replace('small', 'large')
                            filename = str(item_title) + str(num) + '.jpg'
                            try:
                                downImg(img_url+'.jpg', filename)
                            except:
                                pass
                    time.sleep(refresh_interval * random.randint(2, 5))

        #         if not re.match('captcha',item_content):
        #             item_post_session = re.findall('name="session"value="([^"]+)"',replace_all(item_content,replace_dict))
        # print item_post_session
        #             item_post_session = item_post_session[0]
        #             data = {'content':sofa_content,'action':'comments','session':item_post_session}
        #             post(item_url+'comments',data,cj)
        #         else:
        #             print '有验证码啦！\a'
        #             break
        if debug == 1:
            time.sleep(refresh_interval)
        else:
            time.sleep(refresh_interval * random.randint(3, 7))


if __name__ == '__main__':
    cj = cookielib.CookieJar()
    debug = 0
    main()
