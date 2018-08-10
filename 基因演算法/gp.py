# -*- coding: utf-8 -*-
from random import random,randint,choice 
from copy import deepcopy 
from math import log 
 
class fwrapper: 
    def __init__ (self,function,childcount,name): 
        self.function=function 
        self.childcount=childcount 
        self.name=name 
 
class node: 
    def __init__(self,fw,children): 
        self.function=fw.function 
        self.name=fw.name 
        self.children=children  
    def evaluate(self,inp): 
        results=[n.evaluate(inp) for n in self.children] 
        return self.function(results)
    def display(self,indent=0):
        print((' '*indent)+self.name)
        for c in self.children: c.display(indent+1)
 
# 輸入參數
class paramnode: 
    def __init__(self,idx): 
        self.idx=idx  
    def evaluate(self,inp): 
        return inp[self.idx] 
    def display(self,indent=0):
        print('%sp%d' % (' '*indent,self.idx))
# 常數
class constnode: 
    def __init__(self,v): 
        self.v=v  
    def evaluate(self,inp): 
        return self.v 
    def display(self,indent=0):
        print('%s%d' % (' '*indent,self.v))
 


 
addw=fwrapper(lambda l:l[0]+l[1],2,'add') 
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract') 
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply') 
def iffunc(l): 
    if l[0]>0: return l[1] 
    else: return l[2]  
ifw=fwrapper(iffunc,3,'if') 
 
def isgreater(l): 
    if l[0]>l[1]:return 1 
    else: return 0 
gtw=fwrapper(isgreater,2,'isgreater') 
 
# 疊代邏輯
flist=[addw,mulw,ifw,gtw,subw] 
 

def makerandomtree(pc,maxdepth=4,fpr=0.5,ppr=0.6):
    if random()<fpr and maxdepth>0:
        f=choice(flist)
        children=[makerandomtree(pc,maxdepth-1,fpr,ppr) for i in range(f.childcount)]
        return node(f,children)
    elif random()<ppr:
        return paramnode(randint(0,pc-1))
    else: return constnode(randint(0,10))
 
def hiddenfunction(x,y):
    return x**2+y

# 建立隱藏function 
def buildhiddenset():
    rows=[]
    for i in range(200):
        x=randint(0,40)
        y=randint(0,40)
        rows.append([x,y,hiddenfunction(x,y)])
    return rows

# 取得節點總分
def scorefunction(tree,s):
    dif=0
    for data in s:
        v=tree.evaluate([data[0],data[1]])
        dif+=abs(v-data[2])
    return dif

# 變異
def mutate(t,pc,probchange=0.1):
    if random()<probchange:
        return makerandomtree(pc)
    else:
        result=deepcopy(t)
        if isinstance(t,node):
            result.children=[mutate(c,pc,probchange) for c in t.children]
        return result    
# 交配
def crossover(t1,t2,probswap=0.7,top=1):
    if random()<probswap and not top:
        return deepcopy(t2)
    else:
        result=deepcopy(t1)
        if isinstance(t1,node) and isinstance(t2,node):
            result.children=[crossover(c,choice(t2.children),probswap,0) for c in t1.children]
        return result
        

# 測試 樹 的產生
def exampletree(): 
    # paramnode() = 輸入參數
    # constnode() = 常數
    # looks like
    # def func(x,y)
    #   if x>3:
    #     return y+5
    #   else:
    #     return y-2
    
    return node(ifw,[node(gtw,[paramnode(0),constnode(3)]),node(addw,[paramnode(1),constnode(5)]),node(subw,[paramnode(1),constnode(2)])]) 
 
# 配合exampletree
def showExample():
    hiddenset=buildhiddenset()
    extree=exampletree() 
    extree.display() 
    
    print('extree score: {0}'.format(scorefunction(extree,hiddenset)))
    muttree=mutate(extree,2)
    muttree.display()
    print()
    print('muttree score: {0}'.format(scorefunction(muttree,hiddenset)))  
 
    random1=makerandomtree(2)
    random1.display() 
    random2=makerandomtree(2)
    random2.display() 
    cross=crossover(random1,random2)
    cross.display()

 

print('開始進行疊代 :')
def evolve(pc,popsize,rankfunction,maxgen=500,mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
    def selectindex():
        return int(log(random())/log(pexp)) #pexp越小 得到的隨機數就越小
    
    # 產生popsize個樹
    populateion=[makerandomtree(pc) for i in range(popsize)]

    # 開始
    for i in range(maxgen):
        # 排序 (找出最佳)
        scores=rankfunction(populateion)
        print('本次交配 分數為: {0}'.format(scores[0][0]))
        if scores[0][0]==0:break # 結果為0(跳出迴圈 代表已經找到結果)
        newpop=[scores[0][1],scores[1][1]] # 最佳兩個結果 結果保存

        # 建構下一代，透過最佳兩個結果進行交配popsize次
        while len(newpop)<popsize:
            if random()>pnew:                
                newpop.append(mutate(crossover(scores[selectindex()][1],scores[selectindex()][1],probswap=breedingrate),pc,probchange=mutationrate))
            else:
                # 加入隨機節點 增加多樣性
                newpop.append(makerandomtree(pc))

        # 更新populateion
        populateion=newpop
    # 疊代完成，顯示結果
    scores[0][1].display()
    return scores[0][1] # 返回對應公式
        
# 排序
def getrankfunction(dataset):
    def rankfunction(populateion):
        scores=[(scorefunction(t,dataset),t) for t in populateion] 
        # Python2
        scores.sort(key=lambda x: x[0])        
        # 若使用 Pythonista for iOS 使用這個排序
        #sorted(scores)

        return scores
    return rankfunction


rf=getrankfunction(buildhiddenset())

evolve(2,500,rf,mutationrate=0.2,breedingrate=0.1,pexp=0.7,pnew=0.1)

 
# (0+(x+x)-x)+y 扭捏1號

