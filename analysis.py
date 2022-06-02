

def get_reachability_info(fsa):
    reachable_states = []
    current_start_states = []
    current_start_states.append(fsa.x0[0])
    # print("reachable_states:\n", reachable_states)
    end_algorithm_flag = 0
    iter_loop = 0
    reachable_states.append(current_start_states[0])

    # check if x0 is not connected to any transitions
    current_start_filtered_deltas = fsa.filter_delta(start=str(fsa.x0[0]), transition=None, end=None)
    if len(current_start_filtered_deltas) == 0:
        end_algorithm_flag = 1

    # print("reachable_states:\n", reachable_states)
    while end_algorithm_flag == 0:
        iter_loop += 1
        # print("iter_loop = ", iter_loop)
        num_failed_filtering = 0
        for i in range(len(current_start_states)):
            current_start_filtered_deltas = fsa.filter_delta(start=str(current_start_states[i].label), transition=None,
                                                              end=None)
            # print("current_start_filtered_deltas:\n", current_start_filtered_deltas)
            if len(current_start_filtered_deltas) == 0:
                # print("current_start_filtered_deltas:\n", current_start_filtered_deltas)
                num_failed_filtering += 1
                # print("num_failed_filtering = ", num_failed_filtering)
            else:
                for iter in range(len(current_start_filtered_deltas)):
                    # print("iter:", iter)
                    current_start_state = current_start_filtered_deltas.end[current_start_filtered_deltas.index[iter]]
                    # print("current_start_state: ", current_start_state)
                    if current_start_state.label not in [x.label for x in reachable_states]:
                        reachable_states.append(current_start_state)
                        current_start_states.insert(iter, current_start_state)
                        # print("reachable_states:\n", reachable_states)
                        # print("current_start_states:\n", current_start_states)
                # print("exit for")
            if num_failed_filtering == len(current_start_filtered_deltas) or len(current_start_states) == len(fsa.X):
                end_algorithm_flag = 1
                # print("end_algorithm_flag = ", end_algorithm_flag)
            else:
                pass

    for iter_x in range(len(fsa.X)):
        for iter_reach in range(len(reachable_states)):
            # print(str(reachable_states[iter_reach].label) + "=?=" + str(fsa.X[iter_x].label))
            if str(reachable_states[iter_reach].label) == str(fsa.X[iter_x].label):
                fsa.X[iter_x].is_Reachable = 1
                break
            else:
                fsa.X[iter_x].is_Reachable = 0

    # print results
    print("reachable_states:\n", reachable_states)
    if len(reachable_states) == len(fsa.X):
        print("The FSA is reachable")
        fsa.is_Reachable = 1
    else:
        print("The FSA is not reachable")
        fsa.is_Reachable = 0

    return fsa.is_Reachable


def get_co_reachability_info(fsa):
    co_reachable_states = []
    current_end_states = []
    for i in range(len(fsa.Xm)):
        current_end_states.append(fsa.Xm[i])
        co_reachable_states.append(fsa.Xm[i])
    end_algorithm_flag = 0
    iter_loop = 0
    # print("co_reachable_states:\n", co_reachable_states)

    # check if there are not final states
    if len(fsa.Xm) == 0:
        end_algorithm_flag = 1

    while end_algorithm_flag == 0:
        iter_loop += 1
        # print("iter_loop = ", iter_loop)
        num_failed_filtering = 0
        for i in range(len(current_end_states)):
            current_end_filtered_deltas = fsa.filter_delta(start=None, transition=None,
                                                            end=str(current_end_states[i].label))
            if len(current_end_filtered_deltas) == 0:
                # print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
                num_failed_filtering += 1
                # print("num_failed_filtering = ", num_failed_filtering)
            else:
                for iter in range(len(current_end_filtered_deltas)):
                    current_end_state = current_end_filtered_deltas.start[current_end_filtered_deltas.index[iter]]
                    # print("current_end_states:\n", current_end_states)
                    if current_end_state.label not in [x.label for x in co_reachable_states]:
                        co_reachable_states.append(current_end_state)
                        current_end_states.insert(iter, current_end_state)
                        # print("co_reachable_states:\n", co_reachable_states)
                        # print("current_end_states:\n", current_end_states)
            if num_failed_filtering == len(current_end_filtered_deltas) or len(current_end_states) == len(fsa.X):
                end_algorithm_flag = 1
                # print("end_algorithm_flag = ", end_algorithm_flag)
            else:
                pass

    for iter_x in range(len(fsa.X)):
        for iter_reach in range(len(co_reachable_states)):
            # print(str(co_reachable_states[iter_reach].label) + "=?=" + str(fsa.X[iter_x].label))
            if str(co_reachable_states[iter_reach].label) == str(fsa.X[iter_x].label):
                fsa.X[iter_x].is_co_Reachable = 1
                break
            else:
                fsa.X[iter_x].is_co_Reachable = 0

    # print results
    print("co_reachable_states:\n", co_reachable_states)
    if len(co_reachable_states) == len(fsa.X):
        print("The FSA is co_reachable")
        fsa.is_co_Reachable = 1
    else:
        print("The FSA is not co_reachable")
        fsa.is_co_Reachable = 0

    return fsa.is_co_Reachable


def get_blockingness_info(fsa):
    if fsa.is_Reachable == None:
        fsa.get_reachability_info()
    if fsa.is_co_Reachable == None:
        fsa.get_co_reachability_info()

    fsa.is_Blocking = 0
    for iter_x in range(len(fsa.X)):
        if fsa.X[iter_x].is_Reachable == 1 and fsa.X[iter_x].is_co_Reachable == 0:
            fsa.X[iter_x].is_Blocking = 1
            fsa.is_Blocking = 1
        else:
            fsa.X[iter_x].is_Blocking = 0

    return fsa.is_Blocking


def get_trim_info(fsa):
    if fsa.is_Reachable == None:
        fsa.get_reachability_info()
    if fsa.is_co_Reachable == None:
        fsa.get_co_reachability_info()

    if fsa.is_Reachable == 1 and fsa.is_co_Reachable == 1:
        fsa.is_Trim = 1
    else:
        fsa.is_Trim = 0

    return fsa.is_Trim


def get_deadness_info(fsa):
    for iter_x in range(len(fsa.X)):
        current_deltas = fsa.filter_delta(start=str(fsa.X[iter_x].label), transition=None, end=None)
        if len(current_deltas) != 0:
            fsa.X[iter_x].is_Dead = 0
        else:
            fsa.X[iter_x].is_Dead = 1


def get_co_reachability_to_x0_info(fsa):
    current_end_state = None
    co_reachable_to_x0_states = []
    current_end_states = []
    for i in range(len(fsa.x0)):
        current_end_states.append(fsa.x0[i])
        co_reachable_to_x0_states.append(fsa.x0[i])
    end_algorithm_flag = 0
    iter_loop = 0
    # print("co_reachable_to_x0_states:\n", co_reachable_to_x0_states)

    # check if x0 is not an end state among the transitions
    current_end_filtered_deltas = fsa.filter_delta(start=None, transition=None, end=str(fsa.x0[0]))
    if len(current_end_filtered_deltas) == 0:
        end_algorithm_flag = 1

    while end_algorithm_flag == 0:
        # print("end_algorithm_flag = ", end_algorithm_flag)
        iter_loop += 1
        # print("iter_loop = ", iter_loop)
        num_failed_filtering = 0
        # print("len(current_end_states) = ", len(current_end_states))
        for i in range(len(current_end_states)):
            # print("i: ", i)
            current_end_filtered_deltas = fsa.filter_delta(start=None, transition=None,
                                                            end=str(current_end_states[i].label))
            # print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
            if len(current_end_filtered_deltas) == 0:
                # print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
                num_failed_filtering += 1
                # print("num_failed_filtering = ", num_failed_filtering)
            else:
                for iter in range(len(current_end_filtered_deltas)):
                    current_end_state = current_end_filtered_deltas.start[current_end_filtered_deltas.index[iter]]
                    # print("current_end_state:\n", current_end_state)
                    if current_end_state.label not in [x.label for x in co_reachable_to_x0_states]:
                        co_reachable_to_x0_states.append(current_end_state)
                        current_end_states.insert(iter, current_end_state)
                        # print("co_reachable_to_x0_states:\n", co_reachable_to_x0_states)
                        # print("current_end_states:\n", current_end_states)

            # print("num_failed_filtering :", num_failed_filtering)
            # print("len(current_end_filtered_deltas) :", len(current_end_filtered_deltas))
            if num_failed_filtering == len(current_end_filtered_deltas) or current_end_state == fsa.x0[0] or len(
                    current_end_states) == len(fsa.X):
                end_algorithm_flag = 1
                # print("end_algorithm_flag = ", end_algorithm_flag)
            else:
                pass

    for iter_x in range(len(fsa.X)):
        for iter_reach in range(len(co_reachable_to_x0_states)):
            # print(str(co_reachable_to_x0_states[iter_reach].label) + "=?=" + str(fsa.X[iter_x].label))
            if str(co_reachable_to_x0_states[iter_reach].label) == str(fsa.X[iter_x].label):
                fsa.X[iter_x].is_co_Reachable_to_x0 = 1
                break
            else:
                fsa.X[iter_x].is_co_Reachable_to_x0 = 0

    # print results
    print("co_reachable_to_x0_states:\n", co_reachable_to_x0_states)
    if len(co_reachable_to_x0_states) == len(fsa.X):
        print("The FSA is co-reachable to the initial state")
        fsa.is_co_Reachable_to_x0 = 1
    else:
        print("The FSA is not co-reachable to the initial state")
        fsa.is_co_Reachable_to_x0 = 0

def get_reversibility_info(fsa):
    # print("get_reversibility_info")
    if fsa.is_Reachable == None:
        # print("get_reachability_info")
        fsa.get_reachability_info()
    if fsa.X[0].is_co_Reachable_to_x0 == None:
        # print("get_co_reachability_to_initial_state_info")
        fsa.get_co_reachability_to_x0_info()

    for iter_x in range(len(fsa.X)):
        if fsa.X[iter_x].is_Reachable == 1:
            if fsa.X[iter_x].is_co_Reachable_to_x0 == 0:
                fsa.is_Reversible = 0
                break
            else:
                fsa.is_Reversible = 1
        else:
            pass

    return fsa.is_Reversible