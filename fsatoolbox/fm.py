from fsatoolbox import fsa, state

def fm(G):
    FM=fsa()

    #the alphabet is the same
    FM.E=G.E

    #states generation
    N=state(label="N", initial=True, final=False)
    FM.add_state(N)
    F=state(label="F", initial=False, final=False)
    FM.add_state(F)
    
    for el in FM.E:
        match el.isFault:
            case None:
                raise ValueError("The event "+el.label+" is not initialized properly: Fault state not set")
            case 1:
                FM.add_transition(N,el,F)
                FM.add_transition(F,el,F)
            case 0:
                FM.add_transition(N,el,N)
                FM.add_transition(F,el,F)
    return FM

