from fsa import FSA

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
    G=FSA()
    X=input("Insert the states, separated by a space: ").split(' ') #or comma?

    for x in X:
        G.add_state(x)

    E=input("Insert the events, separated by a space: ").split(' ')

    for e in E:
        G.add_event(e)

    delta=[]
    while(1):
        inp=input("Insert a transition (in the format x0 a x1) [!q to exit]: ").split(' ')
        if(inp[0]=='!q'):
            break
        if(len(inp)==3):
            G.add_transition(inp[0],inp[1],inp[2])
            '''
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
            '''
        else:
            print("not enough arguments provided, try again")


    #TODO insert objects instead of strings
    x0=input("Insert the initial states, separated by a space: ")
    Xm=input("Insert the final states, separated by a space: ")

    return G