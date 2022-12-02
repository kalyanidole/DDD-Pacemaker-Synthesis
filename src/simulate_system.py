import sys
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import copy
from pathlib import Path
from collections import defaultdict

import matplotlib.ticker as ticker
# plt.rcParams['text.usetex'] = True
# plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{amssymb} \usepackage{mathtools}')


sys.path.extend(list(map(str, Path("specs").iterdir())))
sys.path.extend([str(Path("input"))])

#----------------------------------------------------------
# Automaton utils

automatons = {}


def print_automaton( a ) :
    print(a.input_vars)
    print(a.output_vars)
    print(a.automata_transitions)
    
    # print contents of automaton
    
def read_automaton(automataName):
    #new_module = __import__(automataName+'_dc')
    new_module = __import__(automataName)
    return new_module

def load_all_automatons( automataNames ):
    for automataName in automataNames:
        automatons[automataName] = read_automaton( automataName)

def find_err_state( a ):
    # start_state,final_states,number_of_states
    # return a.error_state
    for i in range(1, a.number_of_states+1):
        if (i not in a.final_states) and (i != a.start_state):
            return i

def check_automaton( a ):
    inter = intersection(a.output_vars,a.input_vars)
    #inter = list(set(a.output_vars) & set(a.input_vars))
    if not(inter) and (a.signals == Union(a.output_vars , a.input_vars)):
        pass
    else:
        print("wrong inp,out variables declared")
    lst = [] 
    for i in range(1, a.number_of_states+1):
        if (i not in a.final_states) and (i != a.start_state):
            lst.append(1)
    if len(lst) == 1:
        pass
    else:
        print("multiple error states found") 
    # empty == a.output_vars \intersation a.input_vars    
    # there is exactly one error state
    pass


#----------------------------------------------------------
# step of a single automaton

            
def create_out_sequences(inputs,signals,a):
    new_dict = {}
    new_list=[]
    #for i in signals:
    #    if i in inputs.keys():
    lSig = len(signals)
    n1 = 0
    n2 = 0
    for j in inputs.keys():
        for k in range(lSig):
            if j == signals[k] and j not in a.output_vars:
                n1 += (2**(lSig-k-1))
                n2 += ((2**(lSig-k-1))*inputs[j])

    c = len(signals)
    maxVal = 2**c
    for i in range(2**c):
        if ( i & n1 ) == n2:
        #if n1 == (~(i^n2))&n1:
            k = "{0:b}".format(int(maxVal + i))[1:]
            new_list.append(k)

    return new_list

def check_dummy_inp( curr_state, inputs, a , dummy_input):
    finished = True #bit indicates if all input vars were present in inputs
    dummy = []
    d_idx = 0
    for i in a.input_vars:
        if i not in inputs:
            inputs[i] = dummy_input[d_idx] # choose a dummy value
            d_idx = d_idx + 1
            # 
            # todo add checks if dummy value choice is safe
            #
            finished = False
            dummy.append(i)
    # print(inputs)
    comp_list = create_out_sequences(inputs, a.signals,a)


    for d in dummy:
        inputs.pop(d)
    new_dict = {}
    c = 0 
    #for key in automata_transitions.keys():
    for i in comp_list:
        key = (int(curr_state),i) 
        #state = a.automata_transitions[key]
        if a.automata_transitions[key] in a.final_states and c == 0:
            c = c + 1
            state = a.automata_transitions[key] 
            for out_var in a.output_vars:
                new_dict[out_var] = int( i[ a.signals.index(out_var)] )

    # if( c > 1 ):
    #     print(a.output_vars[0])
    #     # print_automaton( a )
    #     # print(curr_state)
    #     # exit()

    assert( c < 2 )
    if c == 0:
        # print(a.name)
        print(a.input_vars)
        print(a.output_vars)
        print( curr_state)
        print( inputs )
        print(comp_list)
        raise Exception( "final state unreachable" )
    else:
        return new_dict, state, finished, dummy

zeros = [0,0,0,0,0]
dummy_ones = [ [1] ]
dummy_twos = [ [0,1], [1,0], [1,1] ]
dummy_threes = [ [0,0,1], [0,1,0], [1,0,0], [1,1,0], [0,1,1], [1,0,1], [1,1,1] ]

def step( curr_state, inputs, a ):
    err_state = find_err_state(a)
    new_dict = {}
    new_dict1= {}
    
    #finished = True #bit indicates if all input vars were present in inputs
    new_dict, state, finished,dummy = check_dummy_inp(curr_state, inputs, a, zeros)

    # if( a.output_vars[0] == 'EVA' ):
    #     print_automaton( a )
    #     print(new_dict)
    #     print(finished)
        
    if( len(dummy) == 0 ):
        assert( finished )
        return new_dict, state, finished

    if( len(dummy) > 5): # code is wrong
        print(dummy)     # many dummy is a problem
        print_automaton( a )
        assert(False)

    assert( not finished )
    
    # check if output signal is stable on flip of dummy
    if len(dummy) == 1:
        stable_checks = dummy_ones
    elif len(dummy) == 2:
        stable_checks = dummy_twos
    elif len(dummy) == 3:
        stable_checks = dummy_threes
    else:
        assert(False)
    assert( len(a.output_vars) == 1 )
    unstable = False
    for s_check in stable_checks:
        new_dict1,state1,finished1,dummy =check_dummy_inp(curr_state,inputs,a,s_check)
        for out_var in a.output_vars:
            #print(out_var,new_dict[out_var],new_dict1[out_var])
            if  new_dict[out_var] != new_dict1[out_var]:
                unstable = True
    if unstable:
        new_dict.pop( out_var )
    return new_dict, state, finished            


def getState( automataName, curr_state, inputs ):
    a = automatons[automataName]
    # out_vars = []
    # for var in a.signals:
    #     if var not in inputs.keys():
    #         out_vars.append(var)
    if curr_state == None:
        curr_state = a.start_state
    return step( curr_state, inputs, a)

def all_step( topology, currentStates, inputs ):
    #print(currentStates)
    finalState = []
    finished_automatons = []

    # step automatons
    for i in range(len(topology)):
        automataName = topology[i]
        state = currentStates[i]
        outs, next_state, finished = getState( automataName, state, inputs )
        inputs.update( outs )
        finalState.append( next_state )
        finished_automatons.append( finished )
    # print( finished_automatons )
    # print( finalState )
    # fix the dummy next states due to dummy inputs due to the cycles
    for i in range(len(topology)):
        if not finished_automatons[i]:
            automataName = topology[i]
            state = currentStates[i]
            # if( automataName == 'F5_imply'):
            #     print_automaton(automatons[automataName])
            #print(inputs)
            #     print(currentStates)
            outs, next_state, finished = getState( automataName,state, inputs )
            inputs.update( outs )
            finalState[i] = next_state
            if( not finished):
                # print(outs)
                #print_automaton( automatons[automataName] )
                print(automataName)
                assert( False ) # now all automaton must be finished
    
    return finalState,inputs

def plot_sigs(collect, sig_list):
    # collect: list of dicts, each dict contains (signal_name, signal_value)
    
    # 
    Ys = []
    # matplotlib.rcParams.update({'font.size': 8})
    for sig in sig_list:
        timeSeries = []
        for i in range(len(collect)):
            timeSeries.append(float(collect[i][sig]))
        Ys.append(timeSeries)
    Ys = np.array(Ys)   # (signals, time)

    # Y_new = np.zeros(Ys.shape[1])
    # Y_new[301] = 1
    # Y_new[401] = 1
    # Ys = np.concatenate([Ys, Y_new[np.newaxis, :]], axis=0)
    #print(Ys[2,:])
    
    n_signals, n_time_steps = Ys.shape
    x = np.arange(n_time_steps)

    # fig = plt.figure(figsize=(15, 5))
    # gs = fig.add_gridspec(n_signals, hspace=1)
    # axs = gs.subplots(sharex=True)

    fig, axs = plt.subplots(n_signals, sharex=False, figsize=(10, 6))

    cmap = plt.get_cmap("tab10")
    
    for i in range(n_signals):
        # axs[i].plot(x, Ys[i], c=cmap(i))
        axs[i].step(x, Ys[i], c=cmap(i))
        # axs[i].bar(x, Ys[i], color=cmap(i), width=0.8)
        # axs[i].annotate(text=signal_texts[i], xy=(x[-1], Ys[i, -1]), xytext=(x[0], Ys[i, -1]+0.1), size=15, horizontalalignment="left")
        axs[i].annotate(text=f"{sig_list[i]}", xy=(x[-1], 0), xytext=(x[0], 0.1), size=18, horizontalalignment="left")
        
        axs[i].set_xlim(0, n_time_steps)
        axs[i].set_ylim(0, 1)


        axs[i].spines['top'].set_visible(False)
        axs[i].spines['left'].set_visible(False)
        axs[i].spines['right'].set_visible(False)
        axs[i].spines['bottom'].set_visible(False)
        axs[i].xaxis.set_major_locator(ticker.NullLocator())
        axs[i].yaxis.set_major_locator(ticker.NullLocator())

    fig.tight_layout()
    plt.savefig("url_holdoff.png", dpi=300)
    plt.show()

def generate_pace(inp_dict,curr_state=None):
    # We carefully order the automatons in the topology such that the input to the current automata depends on the outputs of the automata that have occurred before it.
    # The output obtained from the above topology is equivalent to the output obtained after running the same input on the conjunction of all automatons.
    topology  = [
            'auto_boot',
            # Blanking V # cycle of VSA
            'auto_PAVB',
            'auto_PVVB',
            'auto_SVVB',
            'auto_SAVB',
            'auto_initVSA',
            # Blanking A # cycle of ASA
            'auto_PVAB',
            'auto_PAAB',
            'auto_SVAB',
            'auto_SAAB',        
            'auto_initASA',
            # Refractory VS
            'auto_A_imply',
            'auto_PVVR',
            'auto_PVAR',
            'auto_VSN',
            'auto_PAAR',
            'auto_NoAS',
            'auto_C_imply',
            'auto_ExPVAR',
            'auto_ASN',
            # Limits defs 
            'auto_D_imply',
            'auto_LRL', 'auto_URL', 
            #-----------------------
            'auto_SAFE','auto_Vother',
            # Refractory AS
            'auto_entire_PAV',
            'auto_early_PAV',
            'auto_fin_PAV',
            'auto_entire_SAV',
            'auto_early_SAV',
            'auto_fin_SAV',
            # VA interval
            'auto_EPAV', 'auto_ESAV', 
            'auto_B_imply',
            'auto_entire_VA',
            'auto_early_VA',
            'auto_fin_VA', 'auto_EVA',
            # ----------------------------------------
            # Pacing A
            'auto_VAend_AP',
            #-----------------------------------------
            # Pacing V
            'auto_scheduledVP',
            'auto_endURL', 'auto_bet_lateVP', 'auto_pre_lateVP', 
            'auto_endSAFE', 'auto_bet_safeVP', 'auto_pre_safeVP',
            'auto_fin_VP',    
            #--------------- --------------------------
            # Limit conditions
            # 'S1_LRL',
            # 'S2_URL',
        ]
    load_all_automatons(topology)
    ##reset current state
    if curr_state is None:
        curr_state = [None]*len(topology)
    
    # read input
    # input_files = sorted(list(map(str, Path("./inputs").iterdir())))
    # ['inputs/as_vs.json', 'inputs/as_vs1.json', 'inputs/feature.json', 'inputs/in_sig_0.json', 'inputs/input_generator.py', 'inputs/n_zeros.json', 'inputs/new.json', 'inputs/refractory.json', 'inputs/safe.json', 'inputs/safe1.json', 'inputs/zero_new.json', 'inputs/zeros.json', 'inputs/zeros_as.json', 'inputs/zeros_as1.json', 'inputs/zeros_vs.json']
    # Select input as desired
    #input_file = "input/url_holdoff.json" # CHANGEME  
    #rein_file = "input/rein.json"
    # input_file = "inputs_old/safe.json" # CHANGEME
    #f = open(input_file)
    #g = open(rein_file)
    #inputs = {"0": inp_dict}
    #inputs = json.load(f)
    #rein = json.load(g)
    
    # simulate system
    #collect = []
    #trace_size = len(inputs)
    #for var in range(trace_size):
    #ins = inputs[str(var)]
    #ins['reinINP'] = rein[str(var)]['reinINP']
    #print(ins)
    curr_state,output = all_step(topology,copy.deepcopy(curr_state), copy.deepcopy(inp_dict))
    #curr_state,output = all_step(topology,curr_state,inp_dict)

    #collect.append(inputs1)

    
    
    # Plot desired signals
    # signal_names = 'VS', 'AS','VP', 'AP', 'PVVB', 'PAVB',
              # 'SVVB', 'SAVB',  'SVAB', 'SAAB',
              # 'VSA','ASA','PVVR','PVAR','VSN',
              # 'PAAR','PVAR','PAV','SAV','ASN',
              # 'PAV','SAV','ESAV', 'EPAV', 'VSN', 'VA', 'EVA','LRL','URL',
              # 'VA','EVA','VAINB','AAINB','scheduledVP', 'lateVP','pre_lateVP','VVINB', 'safeVP', 'SAFE'

    # choose from above set of signal_names
    sig_list = ['AS', 'VS', 'AP', 'VP', 'PAV', 'SAV', 'scheduledVP', 'lateVP', 'VO', 'VA', 'SAFE']  # demonstrates URL holdoff
    
    #plot_sigs(collect,sig_list)
    return output, curr_state

  

def main():
    # We carefully order the automatons in the topology such that the input to the current automata depends on the outputs of the automata that have occurred before it.
    # The output obtained from the above topology is equivalent to the output obtained after running the same input on the conjunction of all automatons.
    topology  = [
        'auto_boot',
        # Blanking V # cycle of VSA
        'auto_PAVB',
        'auto_PVVB',
        'auto_SVVB',
        'auto_SAVB',
        'auto_initVSA',
        # Blanking A # cycle of ASA
        'auto_PVAB',
        'auto_PAAB',
        'auto_SVAB',
        'auto_SAAB',        
        'auto_initASA',
        # Refractory VS
        'auto_A_imply',
        'auto_PVVR',
        'auto_PVAR',
        'auto_VSN',
        'auto_PAAR',
        'auto_NoAS',
        'auto_C_imply',
        'auto_ExPVAR',
        'auto_ASN',
        # Limits defs 
        'auto_D_imply',
        'auto_LRL', 'auto_URL', 
        #-----------------------
        'auto_SAFE','auto_Vother',
        # Refractory AS
        'auto_entire_PAV',
        'auto_early_PAV',
        'auto_fin_PAV',
        'auto_entire_SAV',
        'auto_early_SAV',
        'auto_fin_SAV',
        # VA interval
        'auto_EPAV', 'auto_ESAV', 
        'auto_B_imply',
        'auto_entire_VA',
        'auto_early_VA',
        'auto_fin_VA', 'auto_EVA',
        # ----------------------------------------
        # Pacing A
        'auto_VAend_AP',
        #-----------------------------------------
        # Pacing V
        'auto_scheduledVP',
        'auto_endURL', 'auto_bet_lateVP', 'auto_pre_lateVP', 
        'auto_endSAFE', 'auto_bet_safeVP', 'auto_pre_safeVP',
        'auto_fin_VP',    
        #--------------- --------------------------
        # Limit conditions
        # 'S1_LRL',
        # 'S2_URL',
    ]
    load_all_automatons(topology)
    curr_state = [None]*len(topology)
    
    # read input
    # input_files = sorted(list(map(str, Path("./inputs").iterdir())))
    # ['inputs/as_vs.json', 'inputs/as_vs1.json', 'inputs/feature.json', 'inputs/in_sig_0.json', 'inputs/input_generator.py', 'inputs/n_zeros.json', 'inputs/new.json', 'inputs/refractory.json', 'inputs/safe.json', 'inputs/safe1.json', 'inputs/zero_new.json', 'inputs/zeros.json', 'inputs/zeros_as.json', 'inputs/zeros_as1.json', 'inputs/zeros_vs.json']
    # Select input as desired
    input_file = "input/url_holdoff.json" # CHANGEME  
    rein_file = "input/rein.json"
    # input_file = "inputs_old/safe.json" # CHANGEME
    f = open(input_file)
    g = open(rein_file)
    inputs = json.load(f)
    rein = json.load(g)
    
    # simulate system
    collect = []
    trace_size = len(inputs)
    for var in range(trace_size):
        ins = inputs[str(var)]
        ins['VO'] = rein[str(var)]['VO']
        #print(ins)
        curr_state,outputs = all_step(topology,curr_state, ins)
        collect.append(outputs)

    
    
    # Plot desired signals
    # signal_names = 'VS', 'AS','VP', 'AP', 'PVVB', 'PAVB',
              # 'SVVB', 'SAVB',  'SVAB', 'SAAB',
              # 'VSA','ASA','PVVR','PVAR','VSN',
              # 'PAAR','PVAR','PAV','SAV','ASN',
              # 'PAV','SAV','ESAV', 'EPAV', 'VSN', 'VA', 'EVA','LRL','URL',
              # 'VA','EVA','VAINB','AAINB','scheduledVP', 'lateVP','pre_lateVP','VVINB', 'safeVP', 'SAFE'

    # choose from above set of signal_names
    sig_list = ['AS', 'VS', 'AP', 'VP', 'PAV', 'SAV', 'scheduledVP', 'lateVP', 'reinVP', 'VO', 'VA', 'SAFE', 'VO', 'reinVP', 'error']  # demonstrates URL holdoff
    
    # sig_list = sig_list[::-1]
    out_dir = Path("./output")
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
    
 
    
    with open(f"{out_dir}/{Path(input_file).stem}.txt", "w") as f:
        #for i in range(len(collect)):
        #    for j in collect[i]:
        #        if (j == 'AP' or 'VP'):
        #            f.write(str(collect[i][j]))
        #outdict = {}
     
        outdict = defaultdict(lambda: defaultdict(dict))
        odict = {}
        for i in range(len(collect)):
            for key, value in collect[i].items():
                if key == 'AP' or key=='VP' or key == 'error' or key == 'PAV':
                    odict[key] = value
                
            outdict[i] = odict   
            odict = {}      
                        
        #print(outdict)
        f.write(str(outdict))            
    plot_sigs(collect,sig_list)
  
#-------------------------------------------------------------------------------------------

def testJohn(inDict):
    class ss:
        generate_pace = generate_pace
    stats,states = ss.generate_pace(inDict)
    #print(f'{stats} {states}')
    # new_module = __import__('2022-08-16-input')
    # in_data = new_module.inPattern
    # new_module = __import__('ats')
    in_data = [
        {'AS': 0, 'VS': 1, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 1},
        {'AS': 0, 'VS': 0, 'VO': 1},
        {'AS': 0, 'VS': 0, 'VO': 1},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 1},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 1},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 1},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 1, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 0},
        {'AS': 0, 'VS': 0, 'VO': 1}
    ]
    vaInt = 10
    collect=[]
    #print(f' AS  AP   VP PAV SAV VA  PVAR')
    for i in range(len(in_data)):

        #print(inDict)
        stats,states = ss.generate_pace(inDict,states)

        #copy.deepcopy(stats)
        collect.append(copy.deepcopy(stats))
        #print(f'{stats["AS"]:3} {stats["AP"]:3} {stats["VP"]:3} {stats["PAV"]:3} {stats["SAV"]:3} {stats["VA"]:3} {stats["PVAR"]:3}')
        
        #print(stats['AP'])
        # if stats['VA'] == 1 :
        #     vaInt -= 1
        #     if vaInt == 0:
        #         inDict = {'AS':1, 'VS':0, 'VO':0}
        #         #print(inDic)
        #     else:
        #         inDict = {'AS':0, 'VS':0, 'VO':0}

        # else:
        #     inDict = {'AS':0, 'VS':0, 'VO':0}
        #     vaInt = 10
        inDict = in_data[i]

    #print(states)
    #sig_list = ['AP', 'VP']
    sig_list = ['AS','ASN', 'VS', 'AP', 'VP', 'SAV', 'EPAV', 'Vother', 'ESAV','VSN','URL','scheduledVP', 'lateVP', 'VO', 'VA', 'SAFE', 'VO',]  # demonstrates URL holdoff
    print([state['AP'] for state in collect])
    plot_sigs(collect,sig_list)
    return(collect)

if __name__ == '__main__':
    #main()
    #give_input({'AS':0,'VS':0,'reinINP':0})
    inp_dict = {'AS':0,'VS':0,'VO':0}
    #When resetting the system, don't provide curr_state, it will be NULL by default
    # output,curr_state= generate_pace(inp_dict)
    #out_next,curr_state_next = generate_pace(inp_dict,curr_state)
   
    collect = testJohn(inp_dict)
 
