from numpy import*
import operator
def  createDataSet():
	pass
	return group,label

def classifyo(inX,dataSet,labels,k):  # inx：用于分类的输入向量，k:用于最后选择的邻居的数目
	dataSetSize=dataSet.shape[0]
	diffMat=tile(inX,(dataSetSize,1))-dataSet
	sqDiffMat=diffMat**2
	sqDistances=sqDiffMat.sum(axis=1)
	distances=sqDiffMat**0.5  #以上用于距离计算
	sortedDistances=distances.argsort()
	classCount={}
	for i in range(k):
		voteIlabel=labels[sortedDistances[i]]
		classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
	sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)  #排序
	return sortedClassCount[0][0]  #P返回最小值的label,即分类的类别

def file2matrix(filename):
	fr=open(filename)
	arrayOLines=fr.readline()
	numberOfLines=len(arrayOLines)
	returnMat=zeros((numberOfLines,3))
	classLabelVector=[]
	index=0
	for line in arrayOLines:
		line=line.strip()
		listFromLiine=line.split('\t')
		