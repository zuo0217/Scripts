#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import sys

URL = "https://www.baidu.com/s?wd={}"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


def getInfo(ip):
    try:
        response = requests.get(url=URL.format(ip), headers=header)
        if response.status_code == 200:
            tmp = re.findall('{}</span>([\u4e00-\u9fa5]+\s?[\u4e00-\u9fa5]+)'.format(ip), str(response.text))
            if len(tmp) > 0:
                return True, ip, tmp[0]
    except Exception as e:
        pass
    return False, ip, "查询失败"


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ipAddress = sys.argv[1]
        if re.findall(r'^\d+\.\d+\.\d+.\d+$', ipAddress):
            print(getInfo(ipAddress))
