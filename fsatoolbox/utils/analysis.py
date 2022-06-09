def get_reachability_info(fsa_obj, set_fsa=True):
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

                count = 0

                for _, start_state in current_start_filtered_deltas.iterrows():

                    count += 1

                    end_state = start_state.end

                    if end_state not in reachable_states:
                        reachable_states.append(end_state)
                        current_start_states.insert(count, end_state)

                    if n_start_states == count + 1:
                        break

            if num_failed_filtering == len(current_start_filtered_deltas) or len(current_start_states) == len(
                    fsa_obj.X):
                end_algorithm_flag = 1

        for x_states in fsa_obj.X:

            if x_states in reachable_states:
                x_states.is_Reachable = True

            else:
                x_states.is_Reachable = False

    is_reachable = all([x.is_Reachable for x in fsa_obj.X])

    if set_fsa is True:
        fsa_obj.is_Reachable = is_reachable

    return is_reachable, reachable_states


def get_co_reachability_info(fsa_obj, set_fsa=True):
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

                count = 0

                for _, end_state in current_end_filtered_deltas.iterrows():

                    count += 1

                    start_state = end_state.start

                    if start_state not in co_reachable_states:
                        co_reachable_states.append(start_state)
                        current_end_states.insert(count, start_state)

                    if n_end_states == count + 1:
                        break

            if num_failed_filtering == len(current_end_filtered_deltas) or len(current_end_states) == len(fsa_obj.X):
                end_algorithm_flag = 1

    # Set the co-reachability property

    for x_state in fsa_obj.X:

        if x_state in co_reachable_states:
            x_state.is_co_Reachable = True

        else:
            x_state.is_co_Reachable = False

    is_co_reachable = all([x.is_Reachable for x in fsa_obj.X])

    if set_fsa is True:
        fsa_obj.is_co_Reachable = is_co_reachable

    return is_co_reachable, co_reachable_states


def get_blockingness_info(fsa_obj, set_fsa=True):
    # Check if Reachable and Co-Reachable properties are set

    if fsa_obj.is_Reachable is None:
        get_reachability_info(fsa_obj)

    if fsa_obj.is_co_Reachable is None:
        get_co_reachability_info(fsa_obj)

    fsa_obj.is_Blocking = False

    for x_state in fsa_obj.X:

        if x_state.is_Reachable is True and x_state.is_co_Reachable is False:
            x_state.is_Blocking = True
        else:
            x_state.is_Blocking = False

    is_blocking = any([x.is_Blocking for x in fsa_obj.X]) is True

    if set_fsa is True:
        fsa_obj.is_Blocking = is_blocking

    return is_blocking, [x for x in fsa_obj.X if x.is_Blocking]


def get_trim_info(fsa_obj, set_fsa=True):
    # Check if Reachable and Co-Reachable properties are set

    if fsa_obj.is_Reachable is None:
        get_reachability_info(fsa_obj)
    if fsa_obj.is_co_Reachable is None:
        get_co_reachability_info(fsa_obj)

    if fsa_obj.is_Reachable is True and fsa_obj.is_co_Reachable is True:
        is_trim = True
    else:
        is_trim = False

    if set_fsa is True:
        fsa_obj.is_Trim = is_trim

    return is_trim


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

                count = 0

                for _, end_state in current_end_filtered_deltas.iterrows():

                    count += 1

                    start_state = end_state.start

                    if start_state not in co_reachable_to_x0_states:
                        co_reachable_to_x0_states.append(start_state)
                        current_end_states.insert(count, start_state)

                    if n_end_states == count + 1:
                        break

            if num_failed_filtering == len(current_end_filtered_deltas) or start_state == fsa_obj.x0[0] or len(
                    current_end_states) == len(fsa_obj.X):
                end_algorithm_flag = 1

    for x_state in fsa_obj.X:

        if x_state in co_reachable_to_x0_states:
            x_state.is_co_Reachable_to_x0 = True

        else:
            x_state.is_co_Reachable_to_x0 = False


def get_reversibility_info(fsa_obj, set_fsa=True):

    if fsa_obj.is_Reachable is None:
        get_reachability_info(fsa_obj)

    if any([x.is_co_Reachable_to_x0 is None for x in fsa_obj.X]):
        get_co_reachability_to_x0_info(fsa_obj)

    for x_state in fsa_obj.X:
        if x_state.is_Reachable:
            if not x_state.is_co_Reachable_to_x0:
                is_reversible = False
                break
            else:
                is_reversible = True

    if set_fsa is True:

        fsa_obj.is_Reversible = is_reversible

    return is_reversible
