import pandas as pd
from fsatoolbox import fsa

def nfa2dfa(G, iterationsLimit=100, stepBystep=False, newStateNameType="conc"):
    """
    Function to compute the equivalent DFA of a NFA

    Parameters
    ----------
    G : input NFA

    iterationsLimit : Default=100, this avoids a infinite loop when there are unobservable loops

    stepByStep : Default=False, if true shows the steps followed by the algorithm

    newStateNameType : Default="conc", available values: "conc"
        this describes how the names of two or more states are used to build the new state name
        
    """
    DFA=fsa()
    
    #This dataframe contains D_eps and D_e for every state of the NFA
    #D_eps is the set of reachable states with zero or more unobservable transitions
    #D_e for every event e is the set of states reachable with a single event e
    D=pd.DataFrame({'x':G.X})

    Euo=[] #unobservable events
    Eo=[] #observable events
    for e in G.E:
        if(e.isObservable):
            Eo.append(e)
        else:
            Euo.append(e)
    
    #The alphabet of the output DFA is the set of observable events of the NFA
    DFA.E=Eo

    #build Deps
    Deps=[]
    for inx, currentst in enumerate(G.X):
        if(inx>iterationsLimit):
            raise Exception("Iterations limit reached, there is a unobservable loop in the automaton?") #TODO check
        t=[]
        tnew=[currentst]
        while(len(tnew)>0):
            st=tnew.pop(0)
            for ev in Euo:
                transitions=G.filter_delta(start=st.label, transition=ev.label)
                for jnx,tr in transitions.iterrows():
                    tnew.append(tr['end'])
            if(st not in t):
                t.append(st)
        Deps.append(t)
    D['Deps']=Deps

    #Build De for every event e
    for ev in Eo:
        De=[]
        for st in G.X:
            e=[]
            transitions=G.filter_delta(start=st.label, transition=ev.label)
            for jnx,tr in transitions.iterrows():
                    e.append(tr['end'])
            e.sort(key=lambda x:x.label)
            De.append(e)
        D['D'+ev.label]=De

    if(stepBystep): print(D)
    
    #build the "alpha-beta" table
    X=[]
    Xnew=[D['Deps'][0]] #initial state TODO check for multiple initial states
    AB=pd.DataFrame()

    while(len(Xnew)>0):
        x=Xnew.pop(0) #select a state to analyse
        if(stepBystep): print("Analyse the state:"+str(x))
        X.append(x)
        tempdf=pd.DataFrame({'x':[x]}) #initialize a data frame for this row
        for ev in Eo: #for every observable event
            if(stepBystep):print("     event:"+ev.label,end="->")
            alpha=[]
            for st in x: #for each NFA state in this DFA state
                #search where we can go with a single transition of the current event
                trInx=D.index[D.index[D['x']==st]].tolist()
                tr=D['D'+ev.label][trInx[0]]
                #if it's not already in alpha, add it
                if(len(tr)>0):
                    for el in tr:
                        if el not in alpha:
                            alpha.append(el)
            alpha.sort(key=lambda x:x.label) #sort alphabetically ste states
            tempdf['alpha:'+ev.label]=[alpha] #add entry in the current data frame row
            if(stepBystep):print("alpha:"+str(alpha),end=", ")
            #check for eps-transitions from the alpha states
            beta=[]
            for el in alpha:
                trInx=D.index[D.index[D['x']==el]].tolist()
                tr=D['Deps'][trInx[0]]
                if(len(tr)>0):
                    for elem in tr:
                        if elem not in beta:
                            beta.append(elem)
            beta.sort(key=lambda x:x.label) #sort alphabetically ste states
            tempdf['beta:'+ev.label]=[beta] #add entry in the current data frame row
            if(stepBystep):print("beta:"+str(beta))
            #check if the new state is already known, otherwise add it to Xnew
            if(len(beta)>0 and beta not in Xnew and beta not in X):
                Xnew.append(beta)
        AB=pd.concat([AB,tempdf],axis=0)

    if(stepBystep): print(AB)

    #Add the found states to the DFA
    #The states are a list of states, this converts them to a single state
    for x in X:
        final=0
        initial=0
        name=""
        if(newStateNameType=="conc"):
            for el in x:
                name=name+el.label
                if el.isFinal: final=1
                if el.isInitial: initial=1
        DFA.add_state(name, isFinal=final, isInitial=initial)
    
    #Add transitions to the DFA
    for i in range(AB.shape[0]):
        initial_st=""
        if(newStateNameType=="conc"):
            for el in (AB['x'].tolist())[i]:
                initial_st=initial_st+el.label
        for ev in Eo:
            end_st=""
            if(newStateNameType=="conc"):
                for el in (AB['beta:'+ev.label].tolist())[i]:
                    end_st=end_st+el.label
            if(not end_st==""):
                DFA.add_transition(initial_state=initial_st,event=ev,end_state=end_st)

    return DFA
