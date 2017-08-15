import time
import random
import math

people = [('Seymour', 'BOS'), ('Franny', 'DAL'), 
         ('Zooey', 'CAK'), ('Walt', 'MIA'),
         ('Buddy', 'ORD'), ('Les', 'OMA')]
            
destination = 'LGA'

flights = {}
with open('schedule.txt') as infile:
    for line in infile:
        origin, dest, depart, arrive, price = line.strip().split(',')
        flights.setdefault((origin, dest), [])
        #将航班详情添加到航班列表中 
        flights[(origin, dest)].append((depart, arrive, int(price)))

#给定时间在一天中的分钟数        
def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3]*60 + x[4]
    
def printschedule(r):
    for d in range(len(r)//2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[2*d]]
        ret = flights[(destination, origin)][r[2*d + 1]]
        print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin, 
        out[0], out[1], out[2], ret[0], ret[1], ret[2]))

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60
    for d in range(len(sol)//2):
        #得到往返航班和返程航班
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d +1])]
        #总价格等于所有往返航班价格之和
        totalprice += outbound[2] + returnf[2]
        #将飞行时间计入成本之中
        totalprice += (getminutes(outbound[1]) - getminutes(outbound[0])) * 0.5
        totalprice += (getminutes(returnf[1]) - getminutes(returnf[0])) * 0.5
        #记录最晚到达时间和最早离开时间
        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])
    #每个人必须在机场等待直到最后一个人到达为止
    #他们也必须在相同时间到达机场，并等候他们的返程航班
    totalwait = 0
    for d in range(len(sol)//2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d + 1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep
    #如果最晚到达的时间小于最早离开的时间，那么就需要多付一天车费
    if latestarrival > earliestdep:
        totalprice += 50
    #如果有人8点之后达到则，追加20罚款
    if latestarrival > getminutes('08:00'):
        totalprice += 20
    return totalprice + totalwait

#模拟退火算法-用多个初始值来模拟退火    
def newannealingoptimize(domain, costf, N = 5, T = 10000.0, cool = 0.95, step = 3):
    #随机初始化值
    vecs = [[random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))] for _ in range(N)]
    while T > 0.1:
        #生成一系列索引值
        idxs = [random.randint(0, len(domain) - 1) for _ in range(N)]
        #选择一个改变索引值的方向
        dirs = [random.randint(-step, step) for _ in range(N)]
        for i in range(N):
            #当前的索引值
            idx = idxs[i]
            #创建一个代表题解的新列表，改变其中一个值
            vecb = vecs[i][:]
            vecb[idx] += dirs[i]
            #判断是否超出边界
            if vecb[idx] < domain[idx][0]:
                vecb[idx] = domain[idx][0]
            elif vecb[idx] > domain[idx][1]:
                vecb[idx] = domain[idx][1]
            #计算当前成本和新的成本
            ea = costf(vecs[i])
            eb = costf(vecb)
            #判断是否是更好的解
            if (eb < ea or random.random() < pow(math.e, -(eb-ea)/T)):
                vecs[i] = vecb[:]            
        #降低温度
        T = T * cool
    #找出最优的方案
    bestsol = vecs[0]
    for i in range(1, N):
        if costf(bestsol) > costf(vecs[i]):
            bestsol = vecs[i]
    return bestsol

#模拟退火算法    
def annealingoptimize(domain, costf, T = 10000.0, cool = 0.95, step = 3):
    #随机初始化值
    vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    while T > 0.1:
        #选择一个索引值
        i = random.randint(0, len(domain) - 1)
        #选择一个改变索引值得方向
        dir = random.randint(-step, step)
        #创建一个代表题解的新列表，改变其中一个值
        vecb = vec[:]
        vecb[i] += dir
        #判断是否超出边界
        if vecb[i] < domain[i][0]:
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]:
            vecb[i] = domain[i][1]
        #计算当前成本和新的成本
        ea = costf(vec)
        eb = costf(vecb)
        #判断是否是更好的解
        if (eb < ea or random.random() < pow(math.e, -(eb-ea)/T)):
            vec = vecb            
        #降低温度
        T = T * cool
    return vec                    
    
if __name__ == '__main__':
    domain = [(0,9)] * (len(people) * 2)
    #模拟退化法
    s = annealingoptimize(domain, schedulecost)
    print(schedulecost(s))
    printschedule(s)
    #新的模拟退火算法
    news = newannealingoptimize(domain, schedulecost, N = 10)
    print(schedulecost(news))
    printschedule(news)
    