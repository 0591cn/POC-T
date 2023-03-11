#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = bit4

import sys

import requests
from lib.core.data import paths, logger
from lib.utils.config import ConfigFileParser
from lib.utils.http import GET_and_parse_json
from lib.core.common import getSafeExString
import getpass
import urllib
import base64
import json




def check(email, key):
    if email and key:
        auth_url = "https://fofa.info/api/v1/info/my?email={0}&key={1}".format(email, key)
        try:
            r_dict = GET_and_parse_json(auth_url, verify=False)
            if r_dict.error:
                return False
            else:
                return True
        except Exception as e:
            logger.error(e)
            return False
    return False


def FofaSearch(query, limit=100, offset=0):  # DONE 付费获取结果的功能实现
    page = offset + 1
    try:
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        logger.info(msg)
        email = ConfigFileParser().FofaEmail()
        key = ConfigFileParser().FofaKey()
        if check(email, key):
            pass
        else:
            raise  # will go to except block
    except:
        msg = 'Automatic authorization failed.'
        logger.warning(msg)
        msg = 'Please input your FoFa Email and API Key below.'
        logger.info(msg)
        email = input("Fofa Email: ").strip()
        key = getpass.getpass(prompt='Fofa API Key: ').strip()
        if not check(email, key):
            msg = 'Fofa API authorization failed, Please re-run it and enter a valid key.'
            sys.exit(logger.error(msg))

    query = base64.b64encode(query)

    url = "https://fofa.info/api/v1/search/all?email={0}&key={1}&qbase64={2}&size={3}&page={4}".format(email, key, query, limit, page)
    #print(request)#
    result = []
    try:
        resp = GET_and_parse_json(url, verify=False)

        if resp.error:
            logger.error(resp.text)
        else: # /opt/POC-T/lib/api/fofa/pack.py:59turn none to false, fix no result to return!
            for item in resp.get('results'):
                #print(item)
                result.append(item[0])
            if resp.get('size') >= 100 and resp.get('size') > limit : # real< limit
                logger.info("{0} items found! {1} returned....".format(resp.get('size'), limit))
            else:# real < 100 or limit > real
                logger.info("{0} items found!".format(resp.get('size')))
    except Exception as e:
        sys.exit(logger.error(getSafeExString(e)))
    finally:
        return result