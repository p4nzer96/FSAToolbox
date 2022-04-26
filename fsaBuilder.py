import fsa

def unique(list1):
    # initialize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


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

if(1):
    print("States: ")
    print(X)
    print("Alphabet:")
    print(E)
    print("delta:")
    print(delta)
    print("Initial state:")
    print(x0)
    print("Final states:")
    print(Xm)

newFsa = fsa(X, E, delta, x0, Xm)