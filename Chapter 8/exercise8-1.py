from random import random, randint
import math
from pylab import *


def wineprice(rating, age):
	peak_age = rating - 50
	#根据等级来计算价格
	price = rating/2
	if age > peak_age:
		#经过‘峰值年’，后继5年里品质将会变差
		price *= (5 - (age - peak_age))
	else:
		#价格在接近‘峰值年’时，会增加到原值的5倍
		price *= (5 * (age + 1)/peak_age)
	if price < 0:
		price = 0
	return price

def wineset1():
	rows = []
	for i in range(300):
		#随机生成年代和等级
		rating = random() * 50 + 50
		age = random() * 50
		#得到一个参考价格
		price = wineprice(rating, age)
		#增加噪声
		price *= (random() * 0.4 + 0.8)
		#加入数据集
		rows.append({'input': (rating, age), 'result': price})
	return rows


def euclidean(v1, v2):
	d = 0.0
	for i in range(len(v1)):
		d += (v1[i] - v2[i]) ** 2
	return math.sqrt(d)

def getdistances(data, vec1):
	distancelist = []
	for i in range(len(data)):
		vec2 = data[i]['input']
		distancelist.append((euclidean(vec1, vec2), i))
	distancelist.sort()
	return distancelist

def knnestimate(data, vec1, k = 5):
	#得到经过排序的距离值
	dlist = getdistances(data, vec1)
	avg = 0.0
	#对前k项结果求平均
	for i in range(k):
		idx = dlist[i][1]
		avg += data[idx]['result']
	avg /= k
	return avg

#高斯函数
def gaussian(dist, sigma = 10.0):
	return math.e**(-dist**2/(2*sigma**2))

#加权knn
def weightedknn(data, vec1, k = 5, weightf = gaussian):
	#得到距离值
	dlist = getdistances(data, vec1)
	avg = 0.0
	totalweight = 0.0
	#得到加权平均值
	for i in range(k):
		dist = dlist[i][0]
		idx = dlist[i][1]
		weight = weightf(dist)
		avg += weight * data[idx]['result']
		totalweight += weight
	avg /= totalweight
	return avg

#拆分数据
def dividedata(data, test = 0.05):
	trainset = []
	testset = []
	for row in data:
		if random() < test:
			testset.append(row)
		else:
			trainset.append(row)
	return trainset, testset

#评估算法
def testalgorithm(algf, k, trainset, testset):
	error = 0.0
	for row in testset:
		guess = algf(trainset, row['input'], k)
		error += (row['result'] - guess)**2
	return error/len(testset)

#交叉验证//成本函数
def crossvalidate(algf, data, k, trials = 100, test = 0.05):
	error = 0.0
	for i in range(trials):
		trainset, testset = dividedata(data, test)
		error += testalgorithm(algf, k, trainset, testset)
	return error/trials


if __name__ == '__main__':
	data = wineset1()
	
	K = 10
	best_perf = 100000
	best_k = 1
	for k in range(1, K):
		cur_perf = crossvalidate(weightedknn, data, k)
		if best_perf > cur_perf:
			best_perf = cur_perf
			best_k = k
	print(best_k)


