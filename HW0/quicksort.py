
def partition(begin,end,A):
	if A[begin]>A[begin+1]:
		temp=A[begin]
		A[begin]=A[begin+1]
		A[begin]=temp
	pivot=begin
	print(A[pivot])
	i=begin	
	for j in range(begin+1,end+1):
		if A[pivot]>=A[j]:
			i+=1
			temp=A[j]
			A[j]=A[i]
			A[i]=temp
	temp=A[pivot]
	A[pivot]=A[i]
	A[i]=temp
	print(A)
	return i
def quicksort(begin,end,A):
	if begin>=end:
		return
	pivot=partition(begin,end,A)
	quicksort(begin,pivot-1,A)
	quicksort(pivot+1,end,A)

A=[1,4,2,2,9,6]
quicksort(0,len(A)-1,A)
print (A)
			
		

