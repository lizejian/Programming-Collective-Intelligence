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
    if latestarrival > getminutes(08:00):
        totalprice += 20
    return totalprice + totalwait

    