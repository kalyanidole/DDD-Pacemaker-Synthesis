from dfa import DFA

import networkx as nx
import matplotlib.pyplot as plt



# input graph
#!cat graph

def min_automata(data_file):
	automata_trans={}
	final_st=[]
	# initialize DFA from file
	filename = data_file
	dfa = DFA(filename)
	#print(dfa)
	#dfa.draw()
	start_state=0
	num_of_state=0
	# minimize dfa
	automata_trans,final_st,start_state,num_of_state=dfa.minimize()
	#print(num_of_state,num_of_final,start_state)
	num_of_final=len(final_st)
	X = dfa.draw()
	# draw minimized dfa
	if True:
		with open('./tmp/min_aut.dot', 'w') as f:
			print(X, file=f) 

#min_automata('../tmp/data.txt')
	return automata_trans,final_st,num_of_state,num_of_final,start_state