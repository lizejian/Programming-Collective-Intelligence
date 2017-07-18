from bs4 import BeautifulSoup
import requests
import re

chare = re.compile(r'[!-\.&]')
itemowners = {}
#要去除的单词
dropwords = ['a', 'new', 'some', 'more', 'own', 'the', 'many', 'other', 'another']
currentuser = 0
for i in range(1, 51):
    #搜索'用户希望拥有的物品'所对应的URL
    c = requests.get('http://member.zebo.com/Main?event_key = USERSEARCH&wiowiw=wiw&keyword=car&page=%d' % (i))
    soup = BeautifulSoup(c.text)
    for td in soup('td'):
        #寻找带有bgverdanasmall类的表格单元格
        if 'class' in dict(td.attrs) and td['class'] == 'bgverdanasmall':
            items = [re.sub(chare, '', a.contents[0].lower()).strip() for a in td('a')]
            for item in items:
                txt = ' '.join([t for t in item.split(' ') if t not in dropwords])
                if len(txt) < 2:
                    continue
                itemowners.setdefault(txt, {})
                itemowners[txt][currentuser] = 1
            currentuser += 1
            
with open('zebo.txt', 'w') as outfile:
    outfile.write('Item')
    for user in range(0, currentuser):
        outfile.write('\tU%d' % user)
        outfile.write('\n')
        for item, owners in itemowners.items():
            if len(owners) > 10:
                out.write(item)
            for user in range(0, currentuser):
                if user in owners:
                    outfile.write('\t0')
            out.write('\n')
   