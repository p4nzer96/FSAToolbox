import fsatoolbox
from fsatoolbox import *

def updateevents(eventslst, fsalst):
    for e in eventslst:
        for k,G in fsalst.items():
            try:
                props={
                    'isObservable':     e.isObservable,
                    'isControllable':   e.isControllable,
                    'isFault':          e.isFault
                }
                G.change_event_props(e, **props)
            except Exception as ex:
                pass

def checkevents(G, eventslst, fsalst):
    for e in G.E:
        if e not in eventslst:
            eventslst.append(e)
        else:
            ex_e = [i for i in eventslst if i.label == e.label][0]
            if(e.isObservable != ex_e.isObservable or e.isControllable != ex_e.isControllable or e.isFault != ex_e.isFault):
                print("Two events with the label \""+e.label+"\" have different proprieties, which one do you want to keep?")
                print("1) Observable: "+str(e.isObservable)+", Controllable: "+str(e.isControllable)+", Fault: "+str(e.isFault))
                print("2) Observable: "+str(ex_e.isObservable)+", Controllable: "+str(ex_e.isControllable)+", Fault: "+str(ex_e.isFault))
                inp = input(">")
                if inp=='2':
                    #keep the event proprieties from the pool
                    props={
                        'isObservable':     ex_e.isObservable,
                        'isControllable':   ex_e.isControllable,
                        'isFault':          ex_e.isFault
                    }
                    G.change_event_props(e, **props)
                else:
                    #update event proprieties
                    ex_e.isObservable=e.isObservable
                    ex_e.isControllable=e.isControllable
                    ex_e.isFault=e.isFault
    updateevents(eventslst, fsalst)