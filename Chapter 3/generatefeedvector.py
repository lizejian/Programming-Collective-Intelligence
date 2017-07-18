import feedparser
import re
def getwordcounts(url):
    #解析订阅源
    d = feedparser.parse(url)
    wc = {}
    #循环遍历所有的文章条目
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        #提取单词
        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    return d.feed.title, wc
            
def getwords(html):
    #取出所有HTML标记
    txt = re.compile(r'<[^>]+>').sub('', html)
    #利用所有非字母字符拆分出单词
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    #转换成小写形式
    return [word.lower() for word in words if word != '']

    
if __name__ == '__main__':
    apcount = {}#统计每个单词出现的条目数
    wordcounts = {}#所有的单词个数统计
    feedlist = []#所有的订阅源
    with open('feedlist.txt', errors = 'ignore') as f:
        for line in f:
            feedlist.append(line)
    for feedurl in feedlist:
        title, wc = getwordcounts(feedurl)
        wordcounts[title] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1                            
    wordlist = []
    #对单词出现率进行筛选
    for w, bc in apcount.items():
        frac = float(bc)/len(feedlist)
        if frac > 0.33 and frac < 0.35:
            wordlist.append(w)
    #输出数据
    with open('blogdata.txt', 'w') as outfile:
        outfile.write('Blog')
        for word in wordlist:
            outfile.write('\t%s' % word)
        outfile.write('\n')
        for blog, wc in wordcounts.items():
            outfile.write(blog)
            for word in wordlist:
                if word in wc:
                    outfile.write('\t%d' % wc[word])
                else:
                    outfile.write('\t0')
            outfile.write('\n')
    
    