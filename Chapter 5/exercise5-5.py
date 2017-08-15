#所有学生
stduent = ['Toby', 'Steve', 'Karen', 'Sarah', 'Dave', 'Jeff', 'Fred', 'Suzie', 'Laura', 'James']

#代表学生的首选和次选
prefs = [('Toby', ('Steve', 'Karen')),
       ('Steve', ('Laura', 'Toby')),
       ('Karen', ('Jeff', 'James')),
       ('Sarah', ('Toby', 'Dave')),
       ('Dave', ('Sarah', 'Jeff')), 
       ('Jeff', ('Dave', 'Suzie')), 
       ('Fred', ('Suzie', 'Sarah')), 
       ('Suzie', ('Fred', 'Laura')), 
       ('Laura', ('James', 'Karen')), 
       ('James', ('Fred', 'Steve'))]

#宿舍个数
dormnum = 5

def dormcost(vec):
    cost = 0
    #建立一个槽序列
    slots = [0,0,1,1,2,2,3,3,4,4]
    #建立宿舍字典，房间号->学生
    dorms = {}
    #遍历每一名学生
    for i in range(len(vec)):
        x = int(vec[i])
        dorms.setdefault(slots[x], [])
        dorms[slots[x]].append(i)
        #删除选中的槽
        del slots[x]
    #计算成本，首选成本值为0，次选成本值为1，不在选择之列则成本之为3
    for s1, s2 in dorms.values():
        #学生1
        pref1 = prefs[s1][1]
        if pref1[0] == s2:
            cost += 0
        elif pref1[1] == s2:
            cost += 1
        else:
            cost += 3
        #学生2
        pref2 = prefs[s2][1]
        if pref2[0] == s1:
            cost += 0
        elif pref2[1] == s1:
            cost += 1
        else:
            cost += 3
    return cost
    
