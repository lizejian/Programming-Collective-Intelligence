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
    return totalprice + totalwait


#遗传算法 
def geneticoptimize(domain, costf, popsize = 50, step = 1, 
                    mutprob = 0.2, elite = 0.2, maxiter = 100):
    #变异操作
    def mutate(vec):
        i = random.randint(0, len(domain) - 1)
        if vec[i] > domain[i][0] and vec[i] < domain[i][1]:
            if random.random() < 0.5:
                return vec[0:i] + [vec[i] - step] + vec[i+1:]
            else:
                return vec[0:i] + [vec[i] + step] + vec[i+1:]
        elif vec[i] == domain[i][0]:
            return vec[0:i] + [vec[i] + step] + vec[i+1:]
        elif vec[i] == domain[i][1]:
            return vec[0:i] + [vec[i] - step] + vec[i+1:]
    #交叉操作
    def crossover(r1, r2):
        i = random.randint(1, len(domain) - 2)
        return r1[0:i] + r2[i:]
    #构造初始种群
    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(vec)
    #每一代中有多少胜出者？
    topelite = int(elite * popsize)
    #主循环
    for i in range(maxiter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s, v) in scores]
        #从纯粹的胜出者开始
        pop = ranked[0:topelite]
        #添加变异和配对后的胜出者
        while len(pop) < popsize:
            if random.random() < mutprob:
                #变异
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                #交叉
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))
    return scores[0][1]

#修改后的遗传算法
def newgeneticoptimize(domain, costf, popsize = 50, step = 1,
                    mutprob = 0.2, elite = 0.2, maxiter = 10):
    #变异操作
    def mutate(vec):
        i = random.randint(0, len(domain) - 1)
        if vec[i] > domain[i][0] and vec[i] < domain[i][1]:
            if random.random() < 0.5:
                return vec[0:i] + [vec[i] - step] + vec[i+1:]
            else:
                return vec[0:i] + [vec[i] + step] + vec[i+1:]
        elif vec[i] == domain[i][0]:
            return vec[0:i] + [vec[i] + step] + vec[i+1:]
        elif vec[i] == domain[i][1]:
            return vec[0:i] + [vec[i] - step] + vec[i+1:]
    #交叉操作
    def crossover(r1, r2):
        i = random.randint(1, len(domain) - 2)
        return r1[0:i] + r2[i:]
    #构造初始种群
    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(vec)
    #每一代中有多少胜出者？
    topelite = int(elite * popsize)
    #在10次迭代后，如果任一最优解没有任何改善，则结束
    cnt = 0
    while 1:
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        if cnt > 10 and scores[0][0] == mincost:
            return scores[0][1]
        mincost = scores[0][0]
        ranked = [v for (s, v) in scores]
        #从纯粹的胜出者开始
        pop = ranked[0:topelite]
        #添加变异和配对后的胜出者
        while len(pop) < popsize:
            if random.random() < mutprob:
                #变异
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                #交叉
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))
        cnt += 1
                    
    
if __name__ == '__main__':
    domain = [(0,9)] * (len(people) * 2)  
    #遗传算法
    s = geneticoptimize(domain, schedulecost)
    print(schedulecost(s))
    printschedule(s)  
    #遗传算法,10次之后如果没有改善，则结束
    news = newgeneticoptimize(domain, schedulecost)
    print(schedulecost(news))
    printschedule(news)
    