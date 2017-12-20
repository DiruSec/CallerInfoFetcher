#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json, urllib, urllib.request, cgi, re, sys
from bs4 import BeautifulSoup
def replaceAddr(query):
    regString = re.compile(r"(?:\r|\n|\t){1,}")
    try:
        return " ".join(list(filter(lambda x: len(x)>0, regString.split(query))))
    except:
        return "未知地址"
def replaceDesc(query):
    regString = re.compile(r"(?:\r|\n|\t){1,}")
    try:
        return regString.sub("",query)
    except:
        return ""
def replaceCount(query):
    regString = re.compile(r"被(.*)位")
    try:
        return regString.findall(query)[0]
    except:
        return "未知人数"

def returnJSON(jsonObject):
    print ("Content-Type: application/json")
    print ("\n")
    print ("\n")
    print (json.dumps(jsonObject,indent=1))
    sys.exit(0)

def error(errorInfo):
    jsonProto["reason"] = errorInfo
    jsonProto["error_code"] = 1
    returnJSON(jsonProto)

def request360(query):
    searchOrg = urllib.request.urlopen(url='https://m.so.com/index.php?q=' + query)
    searchParsed = BeautifulSoup(searchOrg, "html.parser")
    try:
        jsonProto["result"]["phone"] = searchParsed.find("div", class_="mohe-cont").find("div", class_="mh-tel-num").span.text
        jsonProto["result"]["city"] = replaceAddr(searchParsed.find("div", class_="mohe-cont").find("div", class_="mh-tel-adr").p.text)
    except:
        error("查询失败")
    try:
        jsonProto["result"]["name"] = replaceAddr(searchParsed.find("div", class_="mohe-cont").find("div", class_="mh-tel-mark").text)
        jsonProto["result"]["rpt_type"] = replaceAddr(searchParsed.find("div", class_="mohe-cont").find("div", class_="mh-tel-mark").text)
        jsonProto["result"]["rpt_cnt"] = replaceCount(searchParsed.find("div", class_="mohe-cont").find("div", class_="mh-tel-desc").text)
        jsonProto["result"]["countDesc"] = replaceDesc("".join(list(map(lambda x:str(x), searchParsed.find("div", class_="mohe-cont").find("div", class_="mh-tel-desc").contents))))
    except:
        pass
    regString = re.compile(r"(诈骗|骚扰|广告|推销)")
    if (re.match(regString, jsonProto["result"]["rpt_type"]) != None):
        jsonProto["result"]["iszhapian"] = 1

# 获取 CGI 参数
params = cgi.FieldStorage()
jsonProto = {
    "reason": "查询成功",
    "result": {
        "iszhapian": 0,
        "province": "",
        "city": "",
        "provider": "",
        "phone": "",
        "name": "",
        "company": "",
        "info": "",
        "rpt_type": "",
        "rpt_cnt": "",
        "countDesc": ""
    },
    "error_code": 0 
}
# if params['key'] == "baidu":
#     # requestBaidu(params['tel'])
#     error()
# elif params['key'] == '360':
#     request360(params['tel'])
#     returnJSON(jsonProto)
# else:
#     error()

if params.getlist("key")[0] == '360':
    request360(urllib.parse.quote(params.getlist("tel")[0]))
    returnJSON(jsonProto)
else:
    error("invaild key.")