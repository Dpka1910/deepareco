


#MFCS_Updation:

length = len(MFCS)
list1=[]
for k,v in S.items():
	for key,val in MFCS.items():
		if v.issubset(val):
			del(MFCS[key])
			l=v.intersection(val)
			print 'l' , l
			u=set()
			for i in l:
				u.add(i)
				d=val - u
				MFCS[str(length)]= d
				length=length+1
				#list1.append(d)
				#print 'list1' , list1
				u.clear()


for k,v in MFCS.items():
	for key,val in MFCS.items():
		if(key!=k and val.issubset(v)):
			del(MFCS[key])




# join :


K = copy.deepcopy(L)
C={}
i=0
for k,v in L.items():
	for key,val in L.items():
		#print v.intersection(val)
		#print (len(v)-1)
		if (key!=k and len(v.intersection(val))==(len(v)-1)):
			print v.intersection(val)
			print v,val
			C[str(i)] = v.union(val)
			print C
			i=i+1
	del(L[k])


#prune:

flag=0
for k,v in C.items():
	for key,val in MFCS.items():
		print v,val
		if(v.issubset(val)):
			#print 'v' , v
			del(C[k])
		else:
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












===========================================================================================================================			
#MFCS= copy.deepcopy(M)
list2=set()
for k,v in MFCS.items():
	for i in list1:
		if(i.issubset(v)):
			print 'i' , i
			list2.add(frozenset(v))
			print 'M[k]' , MFCS[k]
			#del(MFCS[k])
			print 'list1', list1
			list1.remove(i)




if(len(list2)>0):
	w=set.union(*list2)
		
if(len(list1)>0):
	for i in list1:
		MFCS[str(length)] = i
		length=length+1

length = len(MFCS)
list1=[]
for k,v in S.items():
	for key,val in MFCS.items():
		if v.issubset(val):
			#del(MFCS[key])
			l=v.intersection(val)
			print 'l' , l
			print v, val
			d = val - v
			print 'd' , d
			list1 = list(product(l,d))
			print list1




newset = set()
for k,v in MFCS.items():
	if any(val<v for key,val in MFCS.items()):
			print v ,val
			del(MFCS[key])





		



			
