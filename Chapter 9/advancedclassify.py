from pylab import *
from random import random

class matchrow(object):
	def __init__(self, row, allnum = False):
		if allnum:
			self.data = [float(row[i]) for i in range(len(row)-1)]
		else:
			self.data = row[0:len(row)-1]
		self.match = int(row[len(row) - 1])

def loadmatch(f, allnum = False):
	rows = []
	with open(f) as infile:
		for line in infile:
			rows.append(matchrow(line.split(','), allnum))
	return rows

#可视化数据
def plotagematches(rows):
	xdm, ydm = [r.data[0] for r in rows if r.match == 1], [r.data[1] for r in rows if r.match == 1]
	xdn, ydn = [r.data[0] for r in rows if r.match == 0], [r.data[1] for r in rows if r.match == 0]
	plot(xdm, ydm, 'go')
	plot(xdn, ydn, 'rx')
	show()

#线性分类
def lineartrain(rows):
	averages = {}
	counts = {}
	for row in rows:
		#得到该坐标点所属的分类
		cl = row.match
		averages.setdefault(cl, [0.0] * (len(row.data)))
		counts.setdefault(cl, 0)
		#将该坐标点加入averages
		for i in range(len(row.data)):
			averages[cl][i] += float(row.data[i])
		#记录每个分类中有多少坐标点
		counts[cl] += 1
	#将总和除以计数值得平均值
	for cl, avg in averages.items():
		for i in range(len(avg)):
			avg[i] /= counts[cl]
	return averages

#点积
def dotproduct(v1, v2):
	return sum([v1[i]*v2[i] for i in range(len(v1))])

def veclength(v):
  return sum([p**2 for p in v])

def dpclassify(point, avgs):
	b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0]))/2
	y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
	if y > 0:
		return 0
	else:
		return 1

#将数据转换成数值类型
def yesno(v):
	if v == 'yes':
		return 1
	elif v == 'no':
		return -1
	else:
		return 0

def matchcount(interest1, interest2):
	l1 = interest1.split(':')
	l2 = interest2.split(':')
	x = 0
	for v in l1:
		if v in l2:
			x += 1
	return x

#计算距离
def milesdistance(a1, a2):
	return random()
	lat1, lon1 = getlocation(a1)
	lat2, lon2 = getlocation(a2)
	latdif = 69.1*(lat1 - lat2)
	londif = 53.0*(lon1 - lon2)
	return (latdif**2 + londif**2)**0.5

yahookey = "Your Key Here"
from xml.dom.minidom import parseString
import requests

loc_cache = {}
def getlocation(address):
	if address in loc_cache:
		return loc_cache[address]
	data = requests.get('http://api.local.yahoo.com/MapsService/V1/geocode?appid=%s&location=%s' %
		(yahookey, (address))).text
	doc = parseString(data)
	lat = doc.getElementsByTagName('Latitude')[0].firstChild.nodeValue
	lon = doc.getElementsByTagName('Longitude')[0].firstChild.nodeValue
	loc_cache[address] = (float(lat), float(lon))
	return loc_cache[address]

def loadnumerical():
	oldrows = loadmatch('matchmaker.csv')
	newrows = []
	for row in oldrows:
		d = row.data
		data = [float(d[0]), yesno(d[1]), yesno(d[2]),
				float(d[5]), yesno(d[6]), yesno(d[7]),
				matchcount(d[3], d[8]),
				milesdistance(d[4], d[9]),
				row.match]
		newrows.append(matchrow(data))
	return newrows

def scaledata(rows):
	low = [999999999.0] * len(rows[0].data)
	high = [-999999999.0] * len(rows[0].data)
	#寻找最大值和最小值
	for row in rows:
		d = row.data
		for i in range(len(d)):
			if d[i] < low[i]:
				low[i] = d[i]
			if d[i] > high[i]:
				high[i] = d[i]
	#对数据进行缩放处理的函数
	def scaleinput(d):
		return [(d[i] - low[i])/(high[i]-low[i]) for i in range(len(low))]
	#对所有数据进行缩放处理
	newrows = [matchrow(scaleinput(row.data)+[row.match]) for row in rows]
	#返回新的数据和缩放处理函数
	return newrows, scaleinput

#径向基函数
def rbf(v1, v2, gamma = 20):
	dv = [v1[i] - v2[i] for i in range(len(v1))]
	l = veclength(dv)
	return math.e**(-gamma*l)

def nlclassify(point, rows, offset, gamma = 10):
	sum0 = 0.0
	sum1 = 0.0
	count0 = 0
	count1 = 0
	for row in rows:
		if row.match == 0:
			sum0 += rbf(point, row.data, gamma)
			count0 += 1
		else:
			sum1 += rbf(point, row.data, gamma)
			count1 += 1
	y = (1.0/count0)*sum0 - (1.0/count1)*sum1 + offset
	if y > 0:
		return 0
	else:
		return 1

def getoffset(rows, gamma = 10):
	l0 = []
	l1 = []
	for row in rows:
		if row.match == 0:
			l0.append(row.data)
		else:
			l1.append(row.data)
	sum0 = sum(sum([rbf(v1, v2, gamma) for v1 in l0]) for v2 in l0)
	sum1 = sum(sum([rbf(v1, v2, gamma) for v1 in l1]) for v2 in l1)
	return (1.0/(len(l1)**2))*sum1 - (1.0/(len(l0)**2))*sum0


if __name__ == '__main__':
	#agesonly = loadmatch('agesonly.csv', allnum = True)
	#matchmaker = loadmatch('matchmaker.csv')

	#plotagematches(agesonly)

	#avgs = lineartrain(agesonly)
	
	#dpclassify([48, 20], avgs))

	#numericalset = loadnumerical()
	#print(numericalset[0].data)

	#offset = getoffset(agesonly)
	#print(nlclassify([48, 20], agesonly, offset))

	#scaledset, scalef = scaledata(numericalset)
	#ssoffset = getoffset(scaledset)
	#print(numericalset[2].match)
	#newrow = [28.0, -1, -1, 26.0, -1, 1, 2, 0.8]
	#print(nlclassify(scalef(newrow), scaledset, ssoffset))