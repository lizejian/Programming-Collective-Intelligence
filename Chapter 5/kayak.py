import time
import requests
import xml.dom.minidom

kayakkey = ''

def getkayaksession():
    #构造url
    url = 'http://www.kayak.com/k/ident/apisession?token=%s&version=1' % kayakkey
    #解析返回的XML
    doc = xml.dom.minidom.parseString(requests.get(url).text)
    #找到<sid>XXXXXXXXXXXX</sid>标签
    sid = doc.getElementsByTagName('sid')[0].firstChild.data
    return sid
    
def flightsearch(sid, origin, destination, depart_date):
    #构造搜索用的URL
    url='http://www.kayak.com/s/apisearch?basicmode=true&oneway=y&origin=%s' % origin
    url+='&destination=%s&depart_date=%s' % (destination, depart_date)
    url+='&return_date=none&depart_time=a&return_time=a'
    url+='&travelers=1&cabin=e&action=doFlights&apimode=1'
    url+='&_sid_=%s&version=1' % (sid)
    #得到XML
    doc = xml.dom.minidom.parseString(requests.get(url).text)
    #提取搜索用的ID
    searchid = doc.getElementsByTagName('searchid')
    return searchid
    
def flightsearchresults(sid, searchid):
    #删除开头的$和逗号，并把数字转化成浮点类型
    def parseprice(p):
        return float(p[1:0].replace(',', ''))
    #遍历检测
    while 1:
        time.sleep(2)
        #构造检测所用的URL
        url = 'http://www.kayak.com/s/basic/flight?'
        url += 'searchid=%s&c=5&apimode=1&_sid_=%s&version=1' % (searchid, sid)
        doc = xml.dom.minidom.parseString(requests.get(url).text)
        #寻找morepending标签，并等待其不再为true
        morepending = doc.getElementsByTagName('morepending')[0].firstChild
        if morepending == None or morepending.data == 'flase':
            break
    #下载完整列表
    url = 'http://www.kayak.com/s/basic/flight?'
    url += 'searchid=%s&c=999&apimode=1&_sid_=%s&version=1' % (searchid, sid)
    doc = xml.dom.minidom.parseString(requests.get(url).text)
    #得到不同元素组成的列表
    prices = doc.getElementsByTagName('price')
    departures = doc.getElementsByTagName('depart')
    arrivals = doc.getElementsByTagName('arrive')
    #用zip连在一起
    return zip([p.firstChild.data.split(' ')[1] for p in departures], 
               [p.firstChild.data.split(' ')[1] for p in arrivals],
               [parseprice(p.firstChild.data) for p in prices])
    
def createschedule(people, dest, dep, ret):
    #得到搜索用的会话id
    sid = getkayaksession()
    flights = {}
    for p in people:
        name, origin = p
        #往程航班
        searchid = flightsearch(sid, origin, dest, dep)
        flights[(origin, dest)] = flightsearchresults(sid, searchid)
        #返程航班
        searchid = flightsearch(sid, origin, origin, ret)
        flights[(dest, origin)] = flightsearchresults(sid, searchid)
    return flights
    
