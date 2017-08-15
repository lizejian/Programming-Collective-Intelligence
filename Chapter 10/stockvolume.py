import nmf
import requests
from numpy import *

tickets = ['YHOO', 'AVP', 'BIIB', 'BP', 'CL', 'CVX',
			'DNA', 'EXPE', 'GOOG', 'PG', 'XOM', 'AMGN']

shortest = 30
prices = {}
dates = None

for t in tickets:
	#打开url
	rows = requests.get('http://ichart.finance.yahoo.com/table.csv?' + 
						's=%s&d=11&e=26&f=2006&g=d&a=3&b=12&c=1996'%t + 
						'&ignore=.csv').readlines()
	#从每一行中提取成交量
	prices[t] = [float(r.split(',')[5]) for r in rows[1:] if r.strip() != '']
	if len(prices[t]) < shortest:
		shortest = len(prices[t])
	if not dates:
		dates = [r.split(',')[0] for r in rows[1:] if r.strip() != '']

l1 = [[prices[tickets[i][j]] for i in range(len(tickets))] for j in range(shortest)]

w, h = nmf.factorize(matrix(l1), pc = 5)

print(h)
print(w)

for i in range(shape(h)[0]):
	print('Feature %d' % i)
	#得到最符合当前特征的股票
	ol = [(h[i, j], tickets[j]) for j in range(shape(h)[1])]
	ol.sort(reverse = True)
	for j in range(12):
		print(ol[j], '\n')
	#显示最符合当前特征的交易日期
	porder = [(w[d, i], d) for d in range(300)]
	porder.sort(reverse = True)
	print([(p[0], dates[p[1]]) for p in porder[0:3]], '\n')

