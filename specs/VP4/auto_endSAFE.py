number_of_states= 4
start_state= 4
final_states= [1, 2]
signals= ['SAFE', 'endSAFE']
automata_transitions= {(4, '01'): 1, (4, '00'): 1, (4, '11'): 2, (4, '10'): 2, (1, '00'): 1, (1, '01'): 3, (1, '10'): 2, (1, '11'): 3, (2, '00'): 3, (2, '01'): 1, (2, '10'): 2, (2, '11'): 3, (3, '11'): 3, (3, '10'): 3, (3, '01'): 3, (3, '00'): 3}
input_vars=['SAFE']
output_vars=['endSAFE']
