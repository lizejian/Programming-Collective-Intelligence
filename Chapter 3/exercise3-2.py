import feedparser
import re
def getwordcounts(url):
    #解析订阅源
    d = feedparser.parse(url)
    wordcounts = {}
    #循环遍历所有的文章条目
    for e in d.entries:
        wc = {}
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        #提取单词
        wordlist = getwords(e.title + ' ' + summary)
        for word in wordlist:
            wc.setdefault(word, 0)
            wc[word] += 1
        wordcounts[e.title] = wc
    return wordcounts
            
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
        curwc = getwordcounts(feedurl)
        wordcounts.update(curwc)
        for wc in curwc.values():
            for word, count in wc.items():
                apcount.setdefault(word, 0)
                if count > 1:
                    apcount[word] += 1                            
    #对单词出现率进行筛选
    wordlist = [w for w, bc in apcount.items() if 0.5 > float(bc)/len(wordcounts) > 0.33]
    #输出数据
    with open('Data-exercise3-2.txt', 'w', errors = 'ignore') as outfile:
        outfile.write('Entry')
        for word in wordlist:
            outfile.write('\t%s' % word)
        outfile.write('\n')
        for entry, wc in wordcounts.items():
            outfile.write(entry)
            for word in wordlist:
                if word in wc:
                    outfile.write('\t%d' % wc[word])
                else:
                    outfile.write('\t0')
            outfile.write('\n')
    
    