from fsatoolbox.fsa import fsa
from fsatoolbox.state import state
from fsatoolbox.event import event


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
    G = fsa()
    X = input("Insert the states, separated by a space: ").split(' ')  # or comma?

    # create new state

    states_dict = {}

    for x in X:
        states_dict[x] = state(x)
        G.add_state(states_dict[x])

    E = input("Insert the events, separated by a space: ").split(' ')

    # create new event

    event_dict = {}

    for e in E:
        event_dict[e] = event(e)
        G.add_event(event_dict[e])

    while 1:
        inp = input("Insert a transition (in the format x0 a x1) [!q to exit]: ").split(' ')
        if inp[0] == '!q':
            break
        if not len(inp) == 3:
            print("Incorrect transition format")
            continue

        else:

            i_state_err = inp[0] not in states_dict
            event_err = inp[1] not in event_dict
            f_state_err = inp[2] not in states_dict

            if i_state_err:
                print("The state " + inp[0] + " is not in X")
            if event_err:
                print("The event " + inp[1] + " is not in E")
            if f_state_err:
                print("The state " + inp[2] + " is not in X")

            if i_state_err or event_err or f_state_err:
                continue

            G.add_transition(states_dict[inp[0]], event_dict[inp[1]], states_dict[inp[2]])

        # Setting state properties

    while 1:
        answer = input("Do you want to set the state properties? [y/n]: \n")
        if answer == "y" or answer == "n":
            break

    if answer == "y":

        for x in states_dict.keys():

            # is an Initial State?

            while 1:

                ans = input("Is {} initial? [y/n] --- [blank for skip]: ".format(x))

                if str.lower(ans) == "y" or str.lower(ans) == "yes":

                    states_dict[x].isInitial = True
                    G.x0.append(states_dict[x])
                    break
                elif str.lower(ans) == "n" or str.lower(ans) == "no":

                    states_dict[x].isInitial = False
                    break
                else:

                    print("Enter a valid input")
                    continue

            # is a Final State?

            while 1:

                ans = input("Is {} final? [y/n] --- [blank for skip]: ".format(x))

                if str.lower(ans) == "y" or str.lower(ans) == "yes":

                    states_dict[x].isFinal = True
                    G.Xm.append(states_dict[x])
                    break
                elif str.lower(ans) == "n" or str.lower(ans) == "no":

                    states_dict[x].isFinal = False
                    break
                else:

                    print("Enter a valid input")
                    continue

    # Setting event properties

    while 1:
        answer = input("Do you want to set the events properties? [y/n]\n")
        if answer == "y" or answer == "n":
            break

    if answer == "y":

        for x in event_dict.keys():

            # is Controllable?

            while 1:

                ans = input("Is {} controllable? [y/n] --- [blank for skip]: ".format(x))

                if str.lower(ans) == "y" or str.lower(ans) == "yes":

                    event_dict[x].isControllable = True
                    break
                elif str.lower(ans) == "n" or str.lower(ans) == "no":

                    event_dict[x].isControllable = False
                    break
                else:

                    print("Enter a valid input")
                    continue

            # is Observable?

            while 1:

                ans = input("Is {} observable? [y/n] --- [blank for skip]: ".format(x))

                if str.lower(ans) == "y" or str.lower(ans) == "yes":

                    event_dict[x].isObservable = True
                    break
                elif str.lower(ans) == "n" or str.lower(ans) == "no":

                    event_dict[x].isObservable = False
                    break
                else:

                    print("Enter a valid input")
                    continue

            # is Faulty?

            while 1:

                ans = input("Is {} faulty? [y/n] --- [blank for skip]: ".format(x))

                if str.lower(ans) == "y" or str.lower(ans) == "yes":

                    event_dict[x].isFault = True
                    break
                elif str.lower(ans) == "n" or str.lower(ans) == "no":

                    event_dict[x].isFault = False
                    break
                else:

                    print("Enter a valid input")
                    continue

    return G
