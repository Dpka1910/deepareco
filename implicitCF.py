import pandas as pd
import numpy as np
df = pd.read_csv('userItemComplete.tsv' , header = 0 , sep = '\t',error_bad_lines=False)
# countTable stores count for user-item pairs
countTable = df.pivot_table(columns = ['type_id'],index = ['user_id'],values=['count'])
countTable = countTable.fillna(0)

m,n = countTable.shape
niterations = 20
nfactors = 100

#consrtucting pui : preference user-item table (boolean)
p = pd.DataFrame(countTable.values, columns = list(set(df['type_id'])) , index = list(set(df['user_id'])) )

l=(p.values>0).astype(int)
pui = pd.DataFrame(l , columns = list(set(df['type_id'])) , index = list(set(df['user_id'])))

x =pd.DataFrame(np.random.rand(), index = pui.index , columns = range(0,nfactors))

y =pd.DataFrame(np.random.rand(), index = pui.columns , columns = range(0,nfactors))

x=x.fillna(0)
y=y.fillna(0)
c=(40*(countTable.values))+1
cuidf = pd.DataFrame(c, columns = pui.columns , index = pui.index)

#cuidf.loc['scusr-796039df-d71c-487f-9456-e9510366e','fk_577st1fkgtb7o'] = 1.0


from numpy.linalg import inv
for i in range(20):
	yty = y.T.dot(y)
	yt = y.T
	xt = x.T
	xtx = xt.dot(x)
	for u in x.index:
		x.loc[u] = userfactor(y,yt,yty,u,cuidf,nfactors,0.1)
	for i in y.index:
		y.loc[i] = itemfactor(x,xt,xtx,i,cuidf,nfactors,0.1)


# xu = inv(yTCuy+lambda(I))(yTCup(u))

def userfactor(y,yt, yty ,u, cuidf , nfactors,lamda):
	cu = np.diag(cuidf.loc[u].values)
	kk= cu-np.matrix(np.identity(len(y)))
	kkk = yt.dot(kk)
	kkkk = kkk.dot(y.values)
	w=yty+kkkk+lamda*((np.matrix(np.identity(nfactors))))
	inversew = np.linalg.inv(w)
	ll=yt.dot(cu)
	lll=ll.dot(pui.loc[u].values)
	xu = inversew.dot(lll)
	return xu

def itemfactor(x,xt,xtx ,i,cuidf,nfactors,lamda):
	ci = np.diag(cuidf.loc[:,i].values)
	kk= ci-np.matrix(np.identity(len(x)))
	kkk = xt.dot(kk)
	kkkk = kkk.dot(x.values)
	w =xtx+kkkk+lamda*((np.matrix(np.identity(nfactors))))
	inversew = np.linalg.inv(w)
	ll = xt.dot(ci)
	lll = ll.dot(pui.loc[:,i].values)
	yi = inversew.dot(lll)
	return yi

import heapq

phat = x.dot(y.T)
  
for u in pui.index:
	print '.....'
	print '....'
	print '==============================================='
	print 'user_clicks' , df[(df['user_id'] == u)]['title']
	print '==================================================='
	o=phat.loc[u].values
	for i in heapq.nlargest(7,range(len(o)),o.take):
		print set(df[(df['type_id'] ==pui.columns.values[i])]['title'])

# making dictionary :

dictuser={}
temptdict1={}
#tempdict2={}
for u in pui.index:
	o=phat.loc[u].values
	temptdict1={}
	temptdict1['activities'] = list(df[(df['user_id'] == u)]['title'])
	lis=[]
	for ind in range(0,len(temptdict1['activities'])):
		lis.append(list(df[(df['title'] == temptdict1['activities'][ind])].count())[0])
	#print lis
	temptdict1['count_activities'] = lis
	print 'tempdict1' , temptdict1
	#print temptdict1
	items=[]
	l4=[]
	o=phat.loc[u].values
	for i in heapq.nlargest(7,range(len(o)),o.take):
		t= list(df[(df['type_id'] == pui.columns.values[i])]['title'])[0]
		print t 
		items.append(list(df[(df['type_id'] == pui.columns.values[i])]['title'])[0])
		l4.append(list(df[(df['title'] == t)].count())[0])
	#print l4
	temptdict1['recommended_products'] = items
	temptdict1['zount_recommended_products'] = l4
	dictuser.update({u:temptdict1})
