from cmath import pi
import sys
import os
import strcomp
import data_for_minimize
import minimize
import shutil


def extractArguments(specs, fName):
    lenFn = len(fName)
    startIdx = specs.find(fName)+lenFn
    paranths = 1

    endIdx = startIdx
    while paranths>0:
        endIdx+=1
        paranths += 1*(specs[endIdx]=='(') -1*(specs[endIdx]==')') 

    argmts = specs[startIdx+1:endIdx]
    return argmts


def convertTRIG( I, d, O, result_file, input_vars, output_vars ):
    sigs = [I,O]
    init = d
    edges = {}
    final_states = []

    # d is the initial state
    edges[(d, '10')] = 0    # go to start of  
    edges[(d, '00')] = d    # idling
    edges[(d, '01')] = d+1
    edges[(d, '11')] = d+1
    final_states.append(d)

    for i in range(0,d):
        final_states.append(i)
        edges[(i, '01')] = i+1 # passing time
        edges[(i, '11')] = 0   # reset
        edges[(i, '00')] = d+1 # jump to error
        edges[(i, '10')] = d+1 # jump to error
    
    #error state
    edges[(d+1, '00')] = d+1
    edges[(d+1, '01')] = d+1
    edges[(d+1, '10')] = d+1
    edges[(d+1, '11')] = d+1
        
    num_finals = len(final_states)
    num_states = num_finals+1
    strcomp.dump_python_automata( edges, final_states, num_states, num_finals, init, result_file, sigs, input_vars, output_vars)


def wrapper_TRIG(specs):
    argmts = extractArguments(specs,'TRIG').split(',')
    con_val = specs.find(argmts[1]+"=")
    k= specs[con_val:]
    start_val=k.find('=')
    end_val=k.find(';')

    input_pt = specs.find("--i/p:")
    output_pt = specs.find("--o/p:")
    end = specs.find('\n', input_pt)
    end1 = specs.find('\n', output_pt)
    input_vars = specs[input_pt+6:end]
    output_vars = specs[output_pt+6:end1]
    input_vars = input_vars.replace(' ','')
    output_vars = output_vars.replace(' ','')
    input_vars = input_vars.split(',')
    output_vars = output_vars.split(',')
  
    convertTRIG(argmts[0], int(k[start_val+1:end_val]), argmts[2], argmts[3][1:-1], input_vars, output_vars)


def converttBetween(argmts):

    #define neverB() as
    i1 = "([[!({1})]] && [[{2}]])".format(*argmts.split(','))
    #i1 = "([[!({})]] && [[{}]])".format(argmts.split(',')[1],argmts.split(',')[2])

    #define neverA() as
    i2 = "([[!({0})]] && [[!{2}]])".format(*argmts.split(','))
    #i2 = "([[!({})]] && [[!{}]])".format(argmts.split(',')[0],argmts.split(',')[2])

   #define waitForA() as
    #i3 = "((neverA()^slen=1^<{0}>^true) ||  ( neverA() ))".format(*argmts.split(','))
    #[]( ((<{}> && <!{}>)^true) => ({}) )".format(argmts.split(',')[0],argmts.split(',')[1] , i6)
    i3 = "(({}^slen=1^(<{}> && <!({})>)^true) ||  ( {} ) || ( (<{}> && <!({})>)^true))".format(i2, argmts.split(',')[0],argmts.split(',')[2],i2, argmts.split(',')[0],argmts.split(',')[2])

    #define waitForB() as
    #i4 = "( neverB() || ( neverB()^ slen=1 ^(<{1}> && <!{2}>)^waitForA() ) || ((<{1}> && <!{2}>)^waitForA()) )".format(*argmts.split(','))
    i4 = "( {} || ( {}^ slen=1 ^((<{}> && <{}>)^true) ) || ((<{}> && <{}>)^true ) )".format(i1,i1,argmts.split(',')[1],argmts.split(',')[2],argmts.split(',')[1],argmts.split(',')[2])
    
    #define tBetween() as
    #i5 = "[]( ((<{0}>^true)) => ( waitForB() ) )".format(*argmts.split(','))
    i5 = "[]( ((<{}>^true)) => ( {} ) )".format(argmts.split(',')[0],i4)

    #define new_waitForB() as
    #i6 = "( neverB() || ( neverB()^ slen=1 ^(<{1}>^true) ))".format(*argmts.split(','))
    i6 = "( {} || ( {}^ slen=1 ^(<{}>^true) ))".format(i1,i1,argmts.split(',')[1])

    #define waitForA_mod() as
    #i7 = "((slen=1 && (<!{2}>^true))^ ( waitForA() || (<{0}>^true)) )".format(*argmts.split(','))
    i7 = "( (slen=1 )^( {} || (<{}>^true)) )".format(i3,argmts.split(',')[0])

    cvrted1 = "[]( (slen>=1 && ((<{}> && <!({})>)^true)) => ( slen=1^{} ) )".format(argmts.split(',')[0],argmts.split(',')[1] ,i4)
    #cvrted1 = "[]( ((<{0}> && <!{1}>)^true) => ( ( ([[!{1}]] && [[{2}]]) || ( ([[!{1}]] && [[{2}]])^ slen=1 ^(<{1}>^true) )) ) )".format(*argmts.split(','))

    cvrted2 = "[](( slen>=1 && ((<{}>)^true)) => ( slen=1^{} ) )".format(argmts.split(',')[1],i3)
    #cvrted2 = "[]( ((<{1}> && <!{0}>)^true) => ( ((([[!{0}]] && [[!{2}]])^slen=1^<{0}>^true) ||  ( ([[!{0}]] && [[!{2}]]) )) ) )".format(*argmts.split(','))

    cvrted3 = "[]( (slen>=1 && ((<{}> && <{}>)^true)) => ({} ) )".format(argmts.split(',')[0],argmts.split(',')[1],i7)
    #cvrted3 = "[]( (slen>=1 && ((<{0}> && <{1}>)^true)) => (((slen=1 && (<!{2}>^true))^ ( ((([[!{0}]] && [[!{2}]])^slen=1^<{0}>^true) ||  ( ([[!{0}]] && [[!{2}]]) )) || (<{0}>^true)) ) ))".format(*argmts.split(','))

    #cvrted = cvrted1 +" && "+ cvrted2 +" && "+ cvrted3
    cvrted = "({}) && ({})".format(cvrted1,cvrted2)
    return cvrted

def convertendOf(argmts):
    #cvrted = "[](( ((<{0}>^slen=1^<!{0}>)^true) <=> (<{0}>^slen=1^<!{0}>^<{1}> ^true)))".format(*argmts.split(','))
    cvrted = "[](( ((<{0}>^slen=1^<!{0}>)^true) <=> (slen=1^<{1}> ^true)))".format(*argmts.split(','))
    return cvrted

def replaceFn(specs, fName):
    argmts = extractArguments(specs, fName)
    fullFN = fName + '(' + argmts +')'
    if fName == 'tBetween':
       cvrtb = converttBetween(argmts)
       specs = specs.replace(fullFN,cvrtb)
    elif fName == 'endOf':
        cvrtf = convertendOf(argmts)
        specs = specs.replace(fullFN,cvrtf)
    else:
        specs = specs 
    return specs

def expandFunction(specs, fnKey):
    if specs.find(fnKey)!=-1:
        specs = replaceFn(specs, fnKey)

    return specs

def convertSpecs(specs):
    specs = expandFunction(specs, 'tBetween')
    specs = expandFunction(specs, 'endOf')
    return specs


def execute(specs, file_name):
    # expand custom macros used before passing to dcvalid
    dir_name = os.path.dirname(file_name)   # e.g. specs/2
    spec_name = os.path.splitext(os.path.basename(file_name))[0] # e.g. PAVB
    
    
    dcSpecs = convertSpecs(specs)
    is_macro_exp = False
    if specs != dcSpecs:
        is_macro_exp = True
        dir_macro_exp = f"{dir_name}/macro_expanded"
        if os.path.exists(dir_macro_exp) == False:
            os.mkdir(dir_macro_exp)
        macro_exp_filename = f"{dir_macro_exp}/{spec_name}.dc"
        specsFile = open(macro_exp_filename, "w")
        specsFile.write(dcSpecs)
        specsFile.close()
        
        macro_exp_filename

    # run dcvalid to generate automata from specification
    if os.path.exists('tmp') == False:
        os.mkdir('tmp')
    out_file = './tmp/out'
    inter_data ='./tmp/data.txt'

    if is_macro_exp:
        dc_valid_cmd = 'dcvalid ' + macro_exp_filename + ' -w'+ '>' + out_file
    else:
        dc_valid_cmd = 'dcvalid ' + file_name + ' -w'+ '>' + out_file
    os.system(dc_valid_cmd)
    
    result_file = f"{dir_name}/auto_{spec_name}.py"
    # '../'+sp_f+'/'+'auto_'+sp_nm+'.py'

    if os.path.isfile(out_file):
        num_states,Acc_states,Useless_nodes,signals=strcomp.extract_data(out_file)
    else:
        print('Intermediate outfile was not generated. DCValid is not configured')
        exit()
    
    # minimize generated automata
    data_for_minimize.data(inter_data,num_states,Useless_nodes,Acc_states,signals)

    automata_trans,final_st,num_of_state,num_of_final,start_state = minimize.min_automata(inter_data)

    input_pt = specs.find("--i/p:")
    output_pt = specs.find("--o/p:")
    end = specs.find('\n', input_pt)
    end1 = specs.find('\n', output_pt)
    input_vars = specs[input_pt+6:end]
    output_vars = specs[output_pt+6:end1]
    input_vars = input_vars.replace(' ','')
    output_vars = output_vars.replace(' ','')
    input_vars = input_vars.split(',')
    output_vars = output_vars.split(',')
    strcomp.dump_python_automata(automata_trans,final_st,num_of_state,num_of_final,start_state,result_file,signals,input_vars,output_vars)

    shutil.rmtree("./tmp")
    os.remove("./cppout.dc")

def main():
    
    # if TRIG macro is used, then bypass dcvalid and create custom automata
    file_name = sys.argv[1] 
    file = open(file_name, "r")
    specs = file.read()
    if specs.find('TRIG') != -1:
        wrapper_TRIG(specs)
        return

    # else use dcvalid to create automata (expand any custom macros used)
    execute(specs,file_name)


if __name__ == "__main__":
    main()
