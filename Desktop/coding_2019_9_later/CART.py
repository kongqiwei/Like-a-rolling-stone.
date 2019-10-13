#树回归
#《机器学习实战p161页作者说其实也可以考虑用类方法自定义树的机构，例如：
class treeNode():
   def __init__(self,feat,val,right,left):
       feature=feat
       valueOfsplit=val
       rightBranch=right
       leftBracnch=left


###因为Python灵活，所以抛弃定义类的方式，而用字典结构，但是其实类是一个可以使用的选择

from numpy import*

def loadDataSet(filename):
    dataMat=[]
    fr=open(filename)
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def binSplitDataSet(dataSet,feature,value):   #按照给定特征将数据集划分为两部分返回
    mat0=dataSet[nonzero(dataSet[:,feature]>value)[0],:][0]  #遍历数据，如果feature的value符合要求则划到一个集合
    mat1=dataSet[nonzero(dataSet[:,feature]<=value)[0],:][0]
    return mat0,mat1
    
#加一个函数和上面这个对比理解：
def splitDataSet(dataSet,axis,value):  #按照给定特征抽取数据集，返回的是符合要求的数据 
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def createTree(dataSet,leafTyp=regLeaf,errType=regErr,ops=(1,4)):
    feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
    if feat==None:
       return val
    retTree={}  #建立了一个字典结构的树，后面在加入左右孩子
    retTree['spInd']=feat  #记录每一个节点的划分特征
    retTree['spVal']=val     #记录每一个节点的划分值
    lSet,rSet=binSplitDataSet(dataSet,feat,val)   #调用上一个函数将数据一分为二
    retTree['left']=createTree(lSet,leafType,errType,ops)   #递归建立左右树
    retTree['right']=createTree(rSet,leafType,errType,ops)
    return retTree

def regLeaf(dataSet):   #叶子节点，返回数据集的均值
    return mean(dataSet[:,-1])

def regErr(dataSet):   #误差函数，调用了var方法求方差
    return var(dataSet[:,-1])*shape(dataSet)[0]

def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4))  #获取最佳划分索引和最佳划分值
    tolS=ops[0]  #容许误差下降值，即如果变化效果小于这个值则认为已经训练的很不错了
    tolN=ops[0]   #数据集最少样本数
    if len(set(dataSet[:,-1].T.tolist()[0]))==1:  #如果所有的值相等则退出，set这个方法是一个集合，集合的长度为1则都相等
        return None,leafType(dataSet)    #调用传入的参数函数返回数据均值
    m,n=shape(dataSet)
    S=errType(dataSet)  #调用传入的参数函数返回误差
    bestS=inf   #inf是一个特殊值关键字,无穷大
    bestIndex=0 
    bestValue=0
    for featIndex in range(n-1)：
        for splitVal in set(dataSet[:,featIndex])
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            if (shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):
               continue
            news=errType(mat0)+errType(mat1)
            if news<bests:   #根据误差得出最好的划分特征和最好的特征值
               bestIndex=featIndex
               bestValue=splitVal
               bests=news
    if (S-bests)<tolS:  #如果误差在可以接受的范围内，则退出并返回叶子节点即均值，不在继续划分
        return None,leafType(datSet)
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestbaValue)
    if (shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):  #如果数据集已经分的很小了则退出并返回叶子节点即均值
        return None,leafType(dataSet)
    return bestIndex,bestValue      #如果上述两个条件都不符合则返回

def isTree(obj):  #判断是否是树，即字典结构
    return (type(obj).__name__=='dict')

def getMean(tree):
    if isTree(tree['right']):
        tree['right']=getMean(tree['right'])
    if isTree(tree['left']):
        tree['left']=getMean(tree['left'])
    return (tree['left']+tree['right'])/2

def  prune(tree,testData):
    if shape(testData)[0]==0:    # 没有测试数据则对树进行塌陷处理
       return getMean(tree)
    if (isTree(tree['right']) or isTree(tree['left'])):
       lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])  #对测试数据进行二类划分然后在左右树中递归剪枝
    if isTree(tree['left']):
       tree['left']=prune(tree['left'],lSet)  #递归剪枝
    if isTree(tree['right']):
       tree['right']=prune(tree['right'],rSet)
    if not isTree(Tree['left']) and not isTree(Tree['right']):
       lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree[s'pVal'])    #如果左右都不是树，则将数据划分
       errorNoMerge=sum(power(lSet[:,-1]-tree['left'],2))+sum(power(rSet[:,-1]-tree['right']),2)  #节点误差计算
       treeMean=(tree['left']+tree['right'])/2  
       errorMerge=sum(power(testData[:,-1]-treeMean,2))   ##合并后的误差计算
       if errorMerge<errorNoMerge:    #按条件剪枝
          print("merging")
          return treeMean
       else:
          return tree   #不剪枝
    else:
       return tree     #返回树

def  linearSolve(dataSet):  #用于将数据格式化为X和 Y变量，后面用于执行简单的线性回归
    m,n=shape(dataSet)   #  获取数据集的行列数
    X=mat(ones((m,n)))   
    Y=mat(ones((m,1)))
    X[:,1:n]=dataSet[:,0:n-1]  #将数据的除了最后一行外都复制到X的除第一行后的其他行
    Y=dataSet[:,-1]   #将最后一行复制给Y
    xTx=X.T*X    #计算X的转置矩阵乘积
    if linalg.det(xTx)==0:  #计算数组的行列式
       raise NameError('this matrix is singular, cannot do iinverse,try increasing the second value of ops')
    ws=xTx,I*(X.T*Y)
    return ws,X,Y   返回线性回归数值

def  modeLeaf(dataSet):     #如果是不在继续划分，返回系数
    ws,X,Y=linarSolve(dataSet)
    return ws

def modelErr(dataSet):    #计算模型误差
    ws,X,Y=linearSolve(dataSet)
    yHat=X*ws
    return sum(power(Y-yHat,2))

def regTreeEval(model,inDat):  #回归树叶子节点预测，对数据格式化处理返回预测值，为了在调用传参时候便于处理，和modelTreeEval一样有两个参数
    return float(model)

def modelTreeEval(model,inDat):   #回归树节点预测
    n=shape(inDat)[1]
    x=mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

def treeForeCast(tree,inData,modelEval=regTreeEval):  #  从上到下遍历整个树，直到命中叶子节点为止，即数据类型不是字典为止
    if not isTree(tree):
       return modelEval(tree,inData)
    if inData[tree['spInd']]>tree['spInd']:
       if isTree(tree['left']):
          return treeForeCast(tree['left'],inData,modelEval)
        else:
          return modelEval(tree['left'],inData,modelEval)
    else:
       if isTree(tree['right']):
          return treeForeCast(tree['right'],inData,modelEval)
       else:
          return modelEval(tree['right'],inData)

def createForeCast(tree,testData,modelEval=regTree):   #以向量形式返回预测值
    m=len(testData)
    yHat=mat(zeros((m,1)))
    for i in range(m):
      yHat[i,0]=treeForeCast(tree,mat(testData[i]),modelEval)
    return yHat

#更改一部分代码可是实现很多树的操作
