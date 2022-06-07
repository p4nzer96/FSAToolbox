def get_reachability_info(fsa_obj):
    reachable_states = []  # List of reachable states
    current_start_states = [fsa_obj.x0[0]]  # take the first initial state

    end_algorithm_flag = 0
    reachable_states.append(current_start_states[0])

    # check if x0 is not connected to any transitions

    current_start_filtered_deltas = fsa_obj.filter_delta(start=fsa_obj.x0[0])
    if len(current_start_filtered_deltas) == 0:
        end_algorithm_flag = 1

    while end_algorithm_flag == 0:

        num_failed_filtering = 0

        for x_state in current_start_states:

            n_start_states = len(current_start_states)

            current_start_filtered_deltas = fsa_obj.filter_delta(start=x_state)

            if len(current_start_filtered_deltas) == 0:
                num_failed_filtering += 1

            else:
                for idx, start_state in current_start_filtered_deltas.iterrows():

                    end_state = start_state.end

                    if end_state not in reachable_states:
                        reachable_states.append(end_state)
                        current_start_states.insert(idx, end_state)

                    if n_start_states == idx + 1:
                        break

            if num_failed_filtering == len(current_start_filtered_deltas) or len(current_start_states) == len(
                    fsa_obj.X):
                end_algorithm_flag = 1

    for x_states in fsa_obj.X:

        if x_states in reachable_states:
            x_states.is_Reachable = True

        else:
            x_states.is_Reachable = False

    if len(reachable_states) == len(fsa_obj.X):
        print("The FSA is reachable")
        print("Reachable states: {}\n".format(reachable_states))
        fsa_obj.is_Reachable = True
    else:
        print("The FSA is not reachable")
        print("Reachable states: {}\n".format(reachable_states))
        fsa_obj.is_Reachable = False

    return fsa_obj.is_Reachable


def get_co_reachability_info(fsa_obj):
    co_reachable_states = []
    current_end_states = []
    for x in fsa_obj.Xm:
        current_end_states.append(x)
        co_reachable_states.append(x)  # All final states are co-reachable
    end_algorithm_flag = 0

    # Check if there are no final states

    if len(fsa_obj.Xm) == 0:

        # Set all states to no co-reachable

        for x in fsa_obj.X:
            x.is_co_Reachable = False
        end_algorithm_flag = 1

    while end_algorithm_flag == 0:

        num_failed_filtering = 0  # No transition to state x

        # For state in current end states list
        for x_state in current_end_states:

            n_end_states = len(current_end_states)

            current_end_filtered_deltas = fsa_obj.filter_delta(end=x_state)

            if len(current_end_filtered_deltas) == 0:
                num_failed_filtering += 1

            else:
                for idx, end_state in current_end_filtered_deltas.iterrows():

                    start_state = end_state.start

                    if start_state not in co_reachable_states:
                        co_reachable_states.append(start_state)
                        current_end_states.insert(idx, start_state)

                    if n_end_states == idx + 1:
                        break

            if num_failed_filtering == len(current_end_filtered_deltas) or len(current_end_states) == len(fsa_obj.X):
                end_algorithm_flag = 1

    # Set the co-reachability property

    for x_state in fsa_obj.X:

        if x_state in co_reachable_states:
            x_state.is_co_Reachable = True

        else:
            x_state.is_co_Reachable = False

    # Set the co-reachability property for the FSA

    if len(co_reachable_states) == len(fsa_obj.X):
        print("The FSA is co-reachable")
        print("Co-reachable states: {}\n".format(co_reachable_states))
        fsa_obj.is_co_Reachable = True
    else:
        print("The FSA is not co-reachable")
        print("Co-reachable states: {}\n".format(co_reachable_states))
        fsa_obj.is_co_Reachable = False

    return fsa_obj.is_co_Reachable


def get_blockingness_info(fsa_obj):
    # Check if Reachable and Co-Reachable properties are set

    if fsa_obj.is_Reachable is None:
        fsa_obj.get_reachability_info()

    if fsa_obj.is_co_Reachable is None:
        fsa_obj.get_co_reachability_info()

    fsa_obj.is_Blocking = False

    for x_state in fsa_obj.X:

        if x_state.is_Reachable is True and x_state.is_co_Reachable is False:
            x_state.is_Blocking = True
            fsa_obj.is_Blocking = True
        else:
            x_state.is_Blocking = False

    if fsa_obj.is_Blocking:
        print("The FSA is blocking")
        print("List of blocking states {}\n".format([x for x in fsa_obj.X if x.is_Blocking is True]))
    else:
        print("The FSA is not blocking\n")

    return fsa_obj.is_Blocking


def get_trim_info(fsa_obj):
    # Check if Reachable and Co-Reachable properties are set

    if fsa_obj.is_Reachable is None:
        get_reachability_info(fsa_obj)
    if fsa_obj.is_co_Reachable is None:
        get_co_reachability_info(fsa_obj)

    if fsa_obj.is_Reachable is True and fsa_obj.is_co_Reachable is True:
        fsa_obj.is_Trim = True
        print("The FSA is Trim\n")
    else:
        fsa_obj.is_Trim = False
        print("The FSA is not Trim\n")

    return fsa_obj.is_Trim


def get_deadness_info(fsa_obj):
    dead_states = []

    for x_state in fsa_obj.X:
        current_deltas = fsa_obj.filter_delta(start=x_state.label)

        if len(current_deltas) != 0:
            x_state.is_Dead = False
        else:
            x_state.is_Dead = True
            dead_states.append(x_state)

    if len(dead_states) != 0:
        print("There are dead states: {}\n".format(dead_states))
    else:
        print("There are no dead states\n")


def get_co_reachability_to_x0_info(fsa_obj):
    co_reachable_to_x0_states = []
    current_end_states = []
    for x in fsa_obj.x0:
        current_end_states.append(x)
        co_reachable_to_x0_states.append(x)
    end_algorithm_flag = 0
    iter_loop = 0

    # check if x0 is not an end state among the transitions
    current_end_filtered_deltas = fsa_obj.filter_delta(end=fsa_obj.x0[0])
    if len(current_end_filtered_deltas) == 0:
        end_algorithm_flag = 1

    while end_algorithm_flag == 0:

        iter_loop += 1
        num_failed_filtering = 0

        for x_state in current_end_states:

            n_end_states = len(current_end_states)

            current_end_filtered_deltas = fsa_obj.filter_delta(end=x_state)

            if len(current_end_filtered_deltas) == 0:
                num_failed_filtering += 1

            else:

                for idx, end_state in current_end_filtered_deltas.iterrows():

                    start_state = end_state.start

                    if start_state not in co_reachable_to_x0_states:
                        co_reachable_to_x0_states.append(start_state)
                        current_end_states.insert(idx, start_state)

                    if n_end_states == idx + 1:
                        break

            if num_failed_filtering == len(current_end_filtered_deltas) or start_state == fsa_obj.x0[0] or len(
                    current_end_states) == len(fsa_obj.X):
                end_algorithm_flag = 1

    for x_state in fsa_obj.X:

        if x_state in co_reachable_to_x0_states:
            x_state.is_co_Reachable_to_x0 = True

        else:
            x_state.is_co_Reachable_to_x0 = False

    print("Co-reachable to x0 states: {}\n".format(co_reachable_to_x0_states))


def get_reversibility_info(fsa_obj):
    if fsa_obj.is_Reachable is None:
        get_reachability_info(fsa_obj)

    if any([x.is_co_Reachable_to_x0 is None for x in fsa_obj.X]):
        get_co_reachability_to_x0_info(fsa_obj)

    for x_state in fsa_obj.X:
        if x_state.is_Reachable:
            if not x_state.is_co_Reachable_to_x0:
                fsa_obj.is_Reversible = False
                break
            else:
                fsa_obj.is_Reversible = True

    if fsa_obj.is_Reversible is True:
        print("The FSA is reversible\n")
    else:
        print("The FSA is not reversible\n")

    return fsa_obj.is_Reversible
