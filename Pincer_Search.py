import pandas as pd 
import datetime
from time import gmtime , strftime
from datetime import datetime

df = pd.read_csv('data_header_1000.tsv' , header = 0 , sep = '\t')

def time_conv(row):
	return datetime.strptime(row , '%Y,%m,%d,%H,%M,%S').month

df['month'] = df.apply(lambda row:time_conv(row['timestamp']) , axis =1)

f= df.groupby(['user_id','month'])


transactions = {}
count = 1

for k, gp in f:
	transactions["T"+str(count)]=set(f.get_group(k).drop_duplicates(['type_id']).index.values)
	count = count+1
    

for k,v in transactions.items():
	print(k,'::',v)

departments = {}

for i in range(0,len(df)):
	departments["D"+str(count)]=df['department'][i]
	count=count+1

result = {}
for key, value in departments.items():
	if value not in result.values():
		result[key] = value

departments = {}
i=1
for k,v in result.items():
	departments["D"+str(i)] =v
	i=i+1

t1=[]
for k,v in transactions.items():
	t1.append(k)

d1 = []
for k,v in departments.items():
	d1.append(k)

import numpy as np
g = pd.DataFrame(0,np.arange(len(d1)) , columns = t1)


#boolean_table:

i=0
j=0
for s,t in transactions.items():
	for items in t:
		j=0
		for c,d in departments.items():
			if df['department'].iloc[items] == d :
				g.iloc[j,i] = 1
			j=j+1	
	i=i+1





#transaction_items_matrix :

qw=[[]]
er=[]

for p,q in transactions.items():
	for n in q:
		er.append(df['type_id'].iloc[n])
	qw.append(er)
	er=[]


qw.pop(0)


#dictionary k holding transactions and product id


k={}


i=0
for p,q in transactions.items():
	k[p] = qw[i]
	i=i+1


# construct dataframe :
dtp= pd.DataFrame(k.items(),columns = ['Transactions','Itemsets'])
g=g.T
g.columns = list(departments.values())

def support_calculate(cndt):
	l=[]
	support={}
	deps=[]
	for key,value in cndt.items():
		listofvalues = list(value)
		for item in listofvalues:
			deps.append(item)
		l= (g[deps[0]]==1)
		for i in range(1,len(deps)):
			l=l&(g[deps[i]]==1)
		support[key] = list(g[l].count())[0]
		deps=[]
	return support


#minSupport = 2

def freq_Sets(supportMFCS,minSupport,MFCS):
	freqMFCS={}
	j={}
	j=supportMFCS
	for k,v in supportMFCS.items():
		if(v>=minSupport):
			freqMFCS[k]=MFCS[k]
			del(j[k])
		else:
			j[k] = MFCS[k]
	print '********freq/_Sets*******'
	return freqMFCS

import copy
def join(L):
	K = copy.deepcopy(L)
	C={}
	i=0
	for k,v in L.items():
		for key,val in L.items():
			#print v.intersection(val)
			#print (len(v)-1)
			if (key!=k and len(v.intersection(val))==(len(v)-1)):
				#print v.intersection(val)
				#print v,val
				C[str(i)] = v.union(val)
				#print C
				i=i+1
		del(L[k])
	print '*******JOINED*********'
	return C



def prune(L , MFS ,C):
	flag=0
	for k,v in C.items():
		for key,val in MFS.items():
			print v,val
			if(v.issubset(val)):
				#print 'v' , v
				del(C[k])
			
		for s,t in L.items():
			if(len(v.intersection(t))<len(t)):
				print 'v.intersection' , v.intersection(t) 
				print len(t) , len(v.intersection(t))
						#print 's' , t
						#print 'v' , v
			else:
				flag =1
			if(flag ==0):
				del(C[k])
				flag=0
		#print 'C' , C
	print "*****Set PRUNNEd*******"
	return C



def MFCS_updation(MFCS ,S):
	length = len(MFCS)
	list1=[]
	delete =[]
	add ={}
	for k,v in S.items():
		for key,val in MFCS.items():
			if v.issubset(val):
				delete.append(key)
				l=v.intersection(val)
				#print 'l' , l
				#print '================================'
				#print v
				#print '================================='
				u=set()
				for i in l:
					u.add(i)
					d=val - u
					add[str(length)] =d
					#print '===================values to be added========   ',add
					#MFCS[str(length)]= d
					length=length+1
					u.clear()
		for ind in delete:
			del(MFCS[ind])
		for k1,v1 in add.items():
			MFCS[k1]=v1
		delete =[]
		add={}
		#print '========MFCS========='
		#print MFCS
	#print "after MFCS finally done++++++++++++++++" 
	#print MFCS
	delete=[]
	for k,v in MFCS.items():
		for key,val in MFCS.items():
			if(key!=k and val<v and not(key in delete)):
				delete.append(key)
	for it in delete:
		if it in set(MFCS.keys()):
			del(MFCS[it])
	print "*****updated MFCS******"
	return MFCS



freq = {}
iteration=1
i=0
cndt={}
colName = list(g.columns)

for i in range(0,len(colName)):
	cndt[str(i)] = {(colName[i])}

MFCS={}
MFCS = {'0':set(colName)}
iteration =1
infreqCndt={}
MFS ={}
lenMFS =0
minSupport=2
delete = set()
while len(cndt)>0:
	supportCndt = support_calculate(cndt)
	supportMFCS = support_calculate(MFCS)
	freqMFCS = freq_Sets(supportMFCS , minSupport ,MFCS)
	freqCndt = freq_Sets(supportCndt , minSupport ,cndt)
	for v in freqMFCS.values():
		MFS[str(lenMFS)] = v
		lenMFS = lenMFS+1
	for k,v in MFS.items():
		for key,values in freqCndt.items():
			if values.issubset(v) and not key in delete:
				delete.add(key)
	for k in delete:
		del(freqCndt[k])
	print 'freq set is '
	print freqCndt
	print ' '
	print 'MFS' , MFS
	print ''
	delete=set()
	infreqCndt = supportCndt
	cndt = join(freqCndt)
	cndt = prune(freqCndt,MFS,cndt)
	MFCS = MFCS_updation(MFCS,infreqCndt)
	print MFCS , iteration
	print ''
	print 'MFS' , MFS
	iteration =iteration+1
	
