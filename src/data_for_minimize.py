import re
#import run
import strcomp
import itertools


def data(inter_data,num_states,Useless_nodes,Acc_states,signals):
	f = open(inter_data, "w")
	n = num_states
	
	for i in range(1,int(n)):

		f.write('%d' % i +" ")	
	f.write('\n')


	#arr = [None] * len(signals)
	#generateAllBinaryStrings(len(signals), arr, 0)
	lst =[]  
	#lst = list(itertools.product([0, 1], repeat=len(signals)))
	lst = [list(i) for i in itertools.product([0, 1], repeat=len(signals))]
	m= ""
	for i in lst:
		m=''.join(map(str, i))
		f.write(str(m)+" ")
	#f.write(str(Useless_nodes))	
	f.write('\n')	



	#f.write('%s' % '00' +" "+'%s' % '01' +" "+'%s' % '10' +" "+'%s' % '11'+'\n')
		#+'%s' % 11 +" ")
		#+'%s' % 0X +" 
		#+'%s' % X0 +" "+'%s' % XX +" "+'%s' % 1X +" "+'%s' % X1 +" ")
	f.write('%d' % 1 +'\n')	
	for i in Acc_states:
		#below line disabled from main code
		if i not in Useless_nodes:
			f.write('%d' % i +" ")
	f.write('\n')

	#for line in open('out'):
	#    match = re.search('State (\d+): ([X|0|1])([X|0|1]) -> state (\d+)', line)
	#    if match:
	#    	p = match.group(1) 
	#    	q = match.group(4)
	#    	r1 = match.group(2)
	#    	r2 = match.group(3)
	 #   	f.write('%d' % int(p) +" " +'%s' % r1+r2 +" "+'%d' % int(q)+ '\n')

		
	for key, value in strcomp.automata.items() :    	
		f.write(" ".join(map(str,key))+" " +str(value) +'\n') 
	f.close()
		

#def generateAllBinaryStrings(n, arr, i):  
  
    #if i == n: 
	#	printTheArray(arr, n)  
	#	return
      
    # First assign "0" at ith position  
    # and try for all other permutations  
    # for remaining positions  
    #arr[i] = 0
   # generateAllBinaryStrings(n, arr, i + 1)  
  
    # And then assign "1" at ith position  
    # and try for all other permutations  
    # for remaining positions  
  #  arr[i] = 1
 #   generateAllBinaryStrings(n, arr, i + 1)  
#

#def printTheArray(arr, n):  
  
#    for i in range(0, n):  
#        print(arr[i], end = " ")  
      
 #  print() 

# Driver Code  
#if __name__ == "__main__":  
  
 #   n = 4
 #   arr = [None] * n  
  
    # Print all binary strings  
  #  generateAllBinaryStrings(n, arr, 0)  


