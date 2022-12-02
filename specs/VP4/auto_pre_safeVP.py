number_of_states= 4
start_state= 3
final_states= [2, 4]
signals= ['pre_safeVP', 'safeVP']
automata_transitions= {(3, '01'): 2, (3, '00'): 2, (3, '11'): 4, (3, '10'): 4, (2, '00'): 2, (2, '01'): 1, (2, '10'): 4, (2, '11'): 1, (4, '00'): 1, (4, '01'): 2, (4, '10'): 4, (4, '11'): 1, (1, '11'): 1, (1, '10'): 1, (1, '01'): 1, (1, '00'): 1}
input_vars=['pre_safeVP']
output_vars=['safeVP']
