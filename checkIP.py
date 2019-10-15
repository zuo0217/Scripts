#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import sys

URL = "https://www.baidu.com/s?wd=ip"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


def getInfo():
    try:
        response = requests.get(url=URL, headers=header)
        if response.status_code == 200:
            tmp = re.findall('(\d+\.\d+\.\d+\.\d+)</span>([\u4e00-\u9fa5]+\s?[\u4e00-\u9fa5]+)', str(response.text))
            if len(tmp) > 0:
                return tmp[0][0], tmp[0][1]
    except Exception as e:
        return False, False

def getInfoFrom(ip):
    try:
        response = requests.get(url=URL.format(ip), headers=header)
        if response.status_code == 200:
            tmp = re.findall('{}</span>([\u4e00-\u9fa5]+\s?[\u4e00-\u9fa5]+)'.format(ip), str(response.text))
            if len(tmp) > 0:
                return True, ip, tmp[0]
    except Exception as e:
        pass
    return False, ip, "查询失败"        


def getIP():
    try:
        response = requests.get(url="http://ip.360.cn/IPShare/info")
        if response.status_code == 200:
            data = response.json()
            if data.get("ip", False) is not False:
                return data["ip"]
            else:
                return "查询失败! {}".format(data)
        else:
            return "查询失败! HTTP CODE:{}".format(response.status_code)
    except Exception as e:
        return  "查询失败! {}".format(e)   

def getInfoFromIP(ip):
    try:
        response = requests.post(url="http://ip.360.cn/IPQuery/ipquery", data={"ip":ip})
        if response.status_code == 200:
            data = response.json()
            if data.get("data", False) is not False:
                return data["data"]
            else:
                return "查询失败! {}".format(data)
        else:
            return "查询失败! HTTP CODE:{}".format(response.status_code)    
    except Exception as e:
        return  "查询失败! {}".format(e)     
                         
if __name__ == "__main__":
    print(getIP())
    print(getInfoFromIP("112.80.248.75"))
