import pandas as pd
from fsa import FSA


def obs(G):
    O=FSA()
    
    D=pd.DataFrame({'x':G.X})

    Euo=[] #unobservable events
    Eo=[] #observable events
    for e in G.E:
        if(e.isObservable):
            Eo.append(e)
        else:
            Euo.append(e)
    
    O.E=Eo

    Deps=[]
    #this breaks if there is a unobservable loop
    for currentst in G.X:
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

    print(D)

    
    for ev in Eo:
        De=[]
        for st in G.X:
            e=[]
            transitions=G.filter_delta(start=st.label, transition=ev.label)
            print(transitions)
            for jnx,tr in transitions.iterrows():
                    e.append(tr['end'])
            De.append(e)
        D['D'+ev.label]=De

    print(D)