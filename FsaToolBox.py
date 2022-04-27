import fsa

#TODO: non mi piace come soluzione
def unique(list1):
    # initialize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def fsabuilder():
    X=unique(input("Insert the states, separated by a space: ").split(' ')) #or comma?

    E=unique(input("Insert the events, separated by a space: ").split(' '))
    delta=[]
    while(1):
        inp=input("Insert a transition (in the format x0 a x1) [!q to exit]: ").split(' ')
        if(inp[0]=='!q'):
            break
        if(len(inp)==3):
            if(inp[0] not in X):
                print("The state " + inp[0] + " is not in X")
                continue
            if(inp[1] not in E):
                print("The event " + inp[1] + " is not in E")
                continue
            if(inp[2] not in X):
                print("The state " + inp[2] + " is not in X")
                continue
            delta.append(inp)
        else:
            print("incorrect, try again")

    x0=input("Insert the initial states, separated by a space: ")
    Xm=input("Insert the final states, separated by a space: ")

    return fsa(X, E, delta, x0, Xm)

def cc(G0, G1):
    CC=fsa()
    CC.E=unique(G0.E+G1.E)
    X=[]
    Xnew=[G0.getInital(), G1.getInital()]

    while(len(Xnew)>0):
        st=Xnew[0]
        
        newTransFound=0
        for event in CC.E:
            if(event in G0.E and event not in G1.E): #private to G0
                trans=G0.getTransFrom(st[0])
                if(len(trans)>0): #TODO check what happens if there are not distinguishable events
                    newState=[trans[2],st[1]]
                    newTransFound=1
                    
            elif(event not in G0.E and event in G1.E): #private to G1
                trans=G1.getTransFrom(st[1])
                if(len(trans)>0):
                    newState=[st[0],trans[2]]
                    newTransFound=1
                    
            else: #synchronized
                transG0=G0.getTransFrom(st[0])
                transG1=G1.getTransFrom(st[1])
                if(len(transG0)>0 and len(transG1)>0):
                    newState=[transG0[2],transG0[2]]
                    newTransFound=1
                    
            if(newTransFound):
                CC.newTrans("".join(st),event,"".join(newState))
                if(newState in X and newState in Xnew):
                    Xnew.append(newState)
        X.append(st)
        Xnew.remove(st)
            
    #the algorithm stores the new state as a list, here i will convert the list to a string that will became the new state name (simple concatenation of the two names)
    for st in X:
        CC.X.append("".join(st))

    #final states
    for st in X:
        if(st[0] in G0.Xm and st[1] in G1.Xm):
            CC.Xm.append("".join(st))
        

#def obs(G):


#def fm(G):
