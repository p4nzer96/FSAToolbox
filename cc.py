
from fsa import FSA

def cc(G0, G1, stepBystep=False):

    CC=FSA()
    CC.E=[]
    for x in (G0.E+G1.E):
        if x not in CC.E:
            CC.E.append(x)
    X=[]
    Xnew=[[G0.x0[0], G1.x0[0]]] #TODO multiple starting states?
    delta=[]
    while(len(Xnew)>0):
        st=Xnew[0]
        print("Stato: ("+st[0].label+","+st[1].label+")")
        for event in CC.E:
            print("Evento: "+event.label, end='->')
            if(event in G0.E and event not in G1.E): #private to G0
                print("Private G0", end='->')
                trans=G0.filter_delta(start=str(st[0].label),transition=str(event.label))
                if (not trans.empty):
                    for inx,el in trans.iterrows():
                        print(el['start'].label+" "+el['transition'].label+" "+el['end'].label)
                        newState=[el['end'],st[1]]
                        delta.append([st,event,newState])
                        if(newState not in X and newState not in Xnew):
                            Xnew.append(newState)
                else:
                    print("No transitions")
                    
            elif(event not in G0.E and event in G1.E): #private to G1
                print("Private G1", end='->')
                trans=G1.filter_delta(start=str(st[1].label),transition=str(event.label))
                if (not trans.empty):
                    for inx,el in trans.iterrows():
                        print(el['start'].label+" "+el['transition'].label+" "+el['end'].label)
                        newState=[st[0],el['end']]
                        delta.append([st,event,newState])
                        if(newState not in X and newState not in Xnew):
                            Xnew.append(newState)
                else:
                    print("No transitions")
                    
            else: #synchronized
                print("Synchronized", end='->')
                transG0=G0.filter_delta(start=str(st[0].label),transition=str(event.label))
                transG1=G1.filter_delta(start=str(st[1].label),transition=str(event.label))
                
                if(not transG0.empty and not transG1.empty):
                    for inx,el0 in transG0.iterrows():
                        for jnx,el1 in transG1.iterrows():
                            print("["+el0['start'].label+" "+el0['transition'].label+" "+el0['end'].label,end=" , ")
                            print(el1['start'].label+" "+el1['transition'].label+" "+el1['end'].label+"]")
                            newState=[el0['end'],el1['end']]
                            delta.append([st,event,newState])
                            if(newState not in X and newState not in Xnew):
                                Xnew.append(newState)
                else:
                    print("No transitions")
                
        X.append(st)
        Xnew.remove(st)
            
    
    #the algorithm stores the new states as a list, here it will convert the list to a string that will became the new state name (simple concatenation of the two names)
    CC.X=[] #?
    for st in X:
        CC.add_state(st[0].label+st[1].label)

    for el in delta:
        CC.add_transition(el[0][0].label+el[0][1].label, el[1].label, el[2][0].label+el[2][1].label)

    #final states
    CC.Xm=[]
    for st in X:
        if(st[0] in G0.Xm and st[1] in G1.Xm):
            CC.Xm.append(st[0].label+st[1].label)
    
    return CC