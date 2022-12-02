#!/usr/bin/python3


# Kosaraju's algorithm to find strongly connected components in Python

from collections import defaultdict
from itertools import combinations

import sys
import random
import re
import time

class Graph:


    def __init__(self, vertex):
        self.V = []
        #for i in range(1,vertex+1):
        for i in range(0,vertex):
            self.V.append(i)
            #self.V.append(-i)
        self.graph = defaultdict(list)

      


    # Add edge into the graph
    def add_edge(self, s, d):
        self.graph[s].append(d)
        #print self.graph
    def get(self, s):
        return self.graph[s]



    # dfs
    def dfs(self, d, visited_vertex, collected):
        traversalStack = [d]
        while (len(traversalStack) >0):
            currNode = traversalStack[-1]
            traversalStack.remove(currNode)

            if visited_vertex[currNode] == True:
                continue

            visited_vertex[currNode] = True
               
            collected.append(currNode)
            #print(currNode)

            adjNodes = self.graph[currNode]
            nrNodes = len(adjNodes)

            for idx in range(nrNodes):
                i = adjNodes[nrNodes - idx -1]
                if not visited_vertex[i]:
                    traversalStack.append(i)
    # dfs
    def dfs_k(self, d, visited_vertex, collected):
        visited_vertex[d] = True
        print(d)
        collected.append(d)

        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.dfs(i, visited_vertex, collected)




    def fill_order(self, d, visited_vertex, stack):

        traversalStack = [d]
        alreadyAdded = [False]*len(visited_vertex)
        #parentMap = {}
        while (len(traversalStack) > 0):
            currNode = traversalStack[-1]

            if alreadyAdded[currNode]==True:
                traversalStack.pop()
                continue

            visited_vertex[currNode] = True
               

            adjNodes = self.graph[currNode]
            nrNodes = len(adjNodes)
            allVisited = True

            for idx in range(nrNodes):
                i = adjNodes[nrNodes - idx-1]
                if visited_vertex[i] == False:
                    traversalStack.append(i)
                    allVisited = False
  
            if allVisited == True:
                traversalStack.pop()
                
                stack.append(currNode)  
                alreadyAdded[currNode] = True 
                #print(currNode)          



    def fill_order_k(self, d, visited_vertex, stack):

        
        visited_vertex[d] = True
        #print(self.graph)
        #print("**********")
        #print(d,self.graph[d])
        for i in self.graph[d]:

            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)

        #print(d)
        stack = stack.append(d)



    # transpose the matrix
    def transpose(self):
        #g = Graph(int(len(self.V)/2))
        g = Graph(int(len(self.V)))
        
        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g


    # Print stongly connected components
    def print_scc(self):
        stack = []
        visited_vertex = dict()
        for v in self.V:
            visited_vertex[v] = False


        for i in self.V:
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)


        gr = self.transpose()


        for v in self.V:
            visited_vertex[v] = False
        # print(self.V)
        # print(stack)
        sccs = []
        while stack:
            i = stack.pop()
            if not visited_vertex[i]:
                scc = []
                gr.dfs(i, visited_vertex, scc)
                sccs.append(scc)
        #print(sccs)
        return sccs

#def rand_lit(n):
#    p1=random.randint(1, n)
#    if random.randint(0, 1) == 0:
 #       return p1
 #   else:
 #       return -p1


#def add_clause(g, n):
#    l1 = rand_lit(n)
#    l2 = rand_lit(n)
#    print( str(l1) + " "+str(l2) )
#    g.add_edge(-l1,l2)
#    g.add_edge(-l2,l1)

#def add_automata(s, d, e,f):
#    if (e == 'X' and f== 'X'):
#        automata[s,'0'+'0'] = d
#        automata[s,'0'+'1'] = d
#        automata[s,'1'+'0'] = d
#        automata[s,'1'+'1'] = d
#    elif (e == 'X' and f!= 'X'):
#        automata[s,'0'+f] = d
#        automata[s,'1'+f] = d
#    elif e != 'X' and f== 'X':
#        automata[s,e+'0'] = d
#        automata[s,e+'1'] = d
#    elif  e != 'X' and f!= 'X':
#        automata[s,e+f] = d
#    else:
 #       print('no label is matched')

def add_automata(s, d, e):
    for i in e:
        automata[s,i] = d

def returnAllCombinations(pattern):
 
    # create an empty stack (we can also use set, deque
    # or any other container)
    kal =[]
    stack = []
    stack.append(pattern)  # push the pattern into the stack
 
    # loop till stack is empty
    while stack:
 
        # pop string from stack and process it
        curr = stack.pop()
 
        # index stores position of first occurrence of wildcard
        # pattern in curr
        index = curr.find('X')
        if index != -1:
            # replace '?' with 0 and 1 and push it to the stack
            for ch in "01":
                curr = curr[:index] + ch + curr[index + 1:]
                stack.append(curr)
            #return stack
        # If no wildcard pattern is found, print the string
        else:
            kal.append(curr)
    return kal


# Finds nodes not a part of the strong component or even leading to it
def remove_nodes(SC,g):
    rem_nodes=[]
    main_comp=[]
    l=len(SC)
    for i in range(0,l):
        if len(SC[i])>1:
            #if len(main_comp) >0:
                #print(SC)
                #raise "more than one Sccs found in the automata" 
            main_comp.append(SC[i])
            
    single_nodes = []
    for i in range(0,l):
        if len(SC[i]) == 1:
            single_nodes.append(SC[i])
   
    for j in single_nodes:
        done = []
        worklist =[]
        worklist.append(j[0])

        reach_maincomp = 0
        while len(worklist) > 0 and reach_maincomp==0:
            n = worklist.pop()
            done.append(n)
            more = g.get(int(n))
            #more = get next states from n
            for n1 in more:
                if any(n1 in sublist for sublist in main_comp):
                #if n1 in (item for sublist in main_comp for item in sublist): 
                    reach_maincomp = 1 
                    break
                elif n1 not in done:
                    done.append( n1 )
                    worklist.append(n1)   
 
        if  reach_maincomp==0:
            rem_nodes.append(j[0])
          
    return rem_nodes



def dump_python_automata(automata_trans,final_st,num_of_state,num_of_final,start_state,result_file,signals, input_vars, output_vars):

    lines = []
    
        #sys.stdout = f

    #r_file = open(result_file)  
        #print ('import sys') 
        #print ('Au='+str(automata))
    lines.append('number_of_states= '+str(num_of_state))
    lines.append('start_state= '+str(start_state))
    lines.append('final_states= '+str(final_st))

    lines.append("signals= "+str(signals))  

    
    lines.append('automata_transitions= '+str(automata_trans))
    lines.append('input_vars='+str(input_vars))
    lines.append('output_vars='+str(output_vars))

    #with  as f:
    #time.sleep(.1)
    f = open(result_file, 'w')
    f.close()
    f = open(result_file, 'a')
    for line in lines:
        f.writelines([line])
        f.writelines(['\n'])
    f.close()
        #print ('sys.path.insert(1, \'../code/\')')
        #print ('import automaton')

        #print ('a=automaton.Automaton(number_of_states,start_state,final_states,automata_transitions)')
        #f.close()

def copy_data(result_file,dest_file):
    f = open(result_file,'r')
    f1 = open(dest_file, 'w')

    for line in f.readlines():
        f1.write(line)

    f1.close()
    f.close()

def extract_data(out_file):

    num_states = 0
    for line in open(out_file):
        #print(line)
        match = re.search('Automaton has (\d+)', line)
        if match:
            #print match.group(1)
            num_states = match.group(1)

    if num_states == 0:
        print('DCValid output file not formatted!')
        return
    
    g = Graph(int(num_states))
    

         
    for line in open(out_file):
        match = re.search('State (\d+): (.*) -> state (\d+)', line)
        if match:
            p = match.group(1) 
            q = match.group(3)
            r1 = match.group(2)

            #r2=returnAllCombinations(r1)
            g.add_edge(int(p),int(q))
            #add_list(int(p),int(q),r1,r2)
            

    #print("Strongly Connected Components:")
    Sccs = g.print_scc()
    Useless_nodes=remove_nodes(Sccs,g)

    # Extracting accepting states from out
    Acc =""
    Acc_states = []
    for line in open(out_file):
        match = re.search('Accepting states: (\d+)', line)
        if match:
            Acc= line
            Acc_states = list(map(int, re.findall(r'\d+', Acc)))
    #for i in Useless_nodes:
     #   if i in Acc_states:
      #      Acc_states.remove(i)
    #below line disabled from old code  
    #Acc_states = [x for x in Acc_states if x not in Useless_nodes]

    if len(Acc_states) == 1 and Acc_states[0] in Useless_nodes:
        Useless_nodes.remove(Acc_states[0])

    #Keeping all the nodes except the usless nodes in final dict
    for line in open(out_file):
        match = re.search('State (\d+): (.*) -> state (\d+)', line)
        if match:
            p = match.group(1) 
            q = match.group(3)
            r1 = match.group(2)

            r2=returnAllCombinations(r1)
            add_automata(int(p),int(q),r2)   

    signals=[]
    varbs = ""
    for line in open(out_file):
        match = re.search('DFA for formula with free variables: ([\w\s]+)', line)
        if match: 
            varbs = match.group(1)
            #signals = [x.strip() for x in varbs.split(',')]
            #varbs = varbs.strip()
            #varbs.replace(" ",',')
            signals.append(varbs)
            #signals=varbs[0].split()
            signals= ' '.join(signals).split() 
    return num_states,Acc_states,Useless_nodes,signals
automata = dict()

#process('../tmp/test.dcvalid.out','/tmp/a.py')
#num_states,Acc_states,Useless_nodes=extract_data('../tmp/out')










