import requests
import re
from bs4 import *
from urllib.parse import urljoin
from sqlite3 import *
#构造一个单词列表，这些单词将被忽略
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler(object):
    #初始化crawler类并传输数据库名称
    def __init__(self, dbname):
        self.con = connect(dbname)
    
    def __del__(self):
        self.con.close()
    
    def dbcommit(self):
        self.con.commit()
        
    #辅助函数，用于获取条目的id，并且如果条目不存在，就将其加入数据库中
    def getentryid(self, table, field, value, createnew = True):
        cur = self.con.execute("select rowid from {} where ? = ?".format(table), (field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute("insert into {} values (?)".format(table, field), (value,))
            return cur.lastrowid
        else:
            return res[0]
    
    #为每个网页建立索引
    def addtoindex(self, url, soup):
        if self.isindexed(url):
            return
        print('Indexing %s' % url)
        #获取每个单词
        text = self.gettextonly(soup)
        words = self.separatewords(text)
        #得到URL的id
        urlid = self.getentryid('urllist', 'url', url)
        #将每个单词与该url关联
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords:
                continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute('insert into wordlocation(urlid, wordid, location) values(%d, %d, %d)' % (urlid, wordid, i))          
    
    #从一个HTML网页中提取文字（不带标签）
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()         
    
    #根据任何非空白字符进行分词处理
    def separatewords(self, text):
        splitter = re.compile(r'\w*')
        return [s.lower() for s in splitter.split(text) if s != '']
    
    #如果url已经建立过索引，则返回true
    def isindexed(self, url):
        u = self.con.execute("select rowid from urllist where url = '%s'" % url).fetchone()
        if u != None:
            #检查它是否已经被检索过了
            v = self.con.execute('select * from wordlocation where urlid = ?',(u[0], )).fetchone()
            if v!= None:
                return True
        return False
     
    #添加一个挂链两个网页的链接
    def addlinkref(self, urlFrom, urlTo, linkText):
        pass
    
    #从一小组网页开始进行广度优先搜索，直至某一给定深度,期间为网页建立索引
    def crawl(self, pages, depth = 2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = requests.get(page)
                except:
                    print('Could not open %s' % page)
                    continue
                soup = BeautifulSoup(c.text, 'html.parser')
                self.addtoindex(page, soup)
                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]#去掉位置部分
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                self.dbcommit()
            pages = newpages
                        
        
    #创建数据库表
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()
        
                
    
if __name__ == '__main__':
    pages = [r'http://www.runoob.com/python/python-tutorial.html']
    crawler = crawler('searchindex.db')
    crawler.crawl(pages)
    
    