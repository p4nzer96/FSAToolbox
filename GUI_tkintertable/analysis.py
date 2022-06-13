"""FSA-Analysis functions"""

def get_reachability_info(fsa):
    # print("get_reachability_info")
    reachable_states = []
    current_start_states = []
    end_algorithm_flag = 0
    temp_list = []
    list_next_states = []
    dict_new_reach_states = {}

    # check if there is the initial state
    if len(fsa.x0) == 0:
        pass
    else:
        current_start_states.append(fsa.x0[0])
        reachable_states.append(current_start_states[0])
        current_start_filtered_deltas = fsa.filter_delta(start=str(fsa.x0[0]), transition=None, end=None)
        if len(current_start_filtered_deltas) == 0:
            pass
        else:
            for iter in range(len(current_start_filtered_deltas)):
                current_start_state = current_start_filtered_deltas.end[current_start_filtered_deltas.index[iter]]
                if current_start_state.label not in [x.label for x in reachable_states]:
                    reachable_states.append(current_start_state)
                    temp_list.append(current_start_state)
                    list_next_states = temp_list.copy()
            i = 0
            dict_new_reach_states.update({str(i): list_next_states})
            # # print("dict_new_reach_states: ", dict_new_reach_states)

            while end_algorithm_flag == 0:
                # # print("i: ", i)
                j = 0
                # # print("dict_new_reach_states[str(i)]: ", dict_new_reach_states[str(i)])
                # # print("len(dict_new_reach_states[str(i)]: ", len(dict_new_reach_states[str(i)]))
                temp_list.clear()
                while j < len(dict_new_reach_states[str(i)]):
                    # # print("j: ", j)
                    # # print("dict_new_reach_states[str(i)][j]: ", dict_new_reach_states[str(i)][j])
                    current_start_filtered_deltas = fsa.filter_delta(start=dict_new_reach_states[str(i)][j], transition=None, end=None)
                    # # print("current_start_filtered_deltas:\n", current_start_filtered_deltas)
                    j += 1
                    if len(current_start_filtered_deltas) == 0:
                        pass
                        #break
                    else:
                        for iter in range(len(current_start_filtered_deltas)):
                            current_start_state = current_start_filtered_deltas.end[current_start_filtered_deltas.index[iter]]
                            if current_start_state.label not in [x.label for x in reachable_states]:
                                reachable_states.append(current_start_state)
                                temp_list.append(current_start_state)

                                # # print("reachable_states: ", reachable_states)
                                # # print("temp_list: ", temp_list)

                if len(temp_list) == 0:
                    end_algorithm_flag = 1
                else:
                    i += 1
                    dict_new_reach_states.clear()
                    list_next_states = temp_list.copy()
                    dict_new_reach_states.update({str(i): list_next_states})
                    # # print("dict_new_reach_states: ", dict_new_reach_states)

        for iter_x in range(len(fsa.X)):
            for iter_reach in range(len(reachable_states)):
                # print(str(reachable_states[iter_reach].label) + "=?=" + str(fsa.X[iter_x].label))
                if str(reachable_states[iter_reach].label) == str(fsa.X[iter_x].label):
                    fsa.X[iter_x].is_Reachable = 1
                    break
                else:
                    fsa.X[iter_x].is_Reachable = 0

    # # print("reachable_states:\n", reachable_states)
    if len(reachable_states) == len(fsa.X) and len(reachable_states) != 0:
        # # print("The FSA is reachable")
        fsa.is_Reachable = 1
    else:
        # # print("The FSA is not reachable")
        fsa.is_Reachable = 0

    return fsa.is_Reachable

def get_co_reachability_info(fsa):
    # print("get_co_reachability_info")
    co_reachable_states = []
    final_states = []


    # check if there are final states
    if len(fsa.Xm) == 0:
        for iter_x in range(len(fsa.X)):
            fsa.X[iter_x].is_co_Reachable = 0
    else:
        for i in range(len(fsa.Xm)):
            final_states.append(fsa.Xm[i])

        temp_list = []
        list_next_states = []
        dict_new_co_reach_states = {}

        for iter_finals in range(len(fsa.Xm)):
            # # print("iter_finals: ", iter_finals)
            end_algorithm_flag = 0
            i = 0
            dict_new_co_reach_states.clear()
            list_next_states.clear()
            list_next_states.append(fsa.Xm[iter_finals])
            co_reachable_states.append(fsa.Xm[iter_finals])
            dict_new_co_reach_states.update({str(i): list_next_states})
            # # print("dict_new_co_reach_states: ", dict_new_co_reach_states)
            while end_algorithm_flag == 0:
                # # print("i: ", i)
                j = 0
                temp_list.clear()
                while j < len(dict_new_co_reach_states[str(i)]):
                    # # print("j: ", j)
                    # # print("dict_new_co_reach_states[str(i)][j]: ", dict_new_co_reach_states[str(i)][j])
                    current_end_filtered_deltas = fsa.filter_delta(start=None, transition=None, end=dict_new_co_reach_states[str(i)][j])
                    # # print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
                    j += 1
                    if len(current_end_filtered_deltas) == 0:
                        pass
                    else:
                        for iter in range(len(current_end_filtered_deltas)):
                            current_start_state = current_end_filtered_deltas.start[current_end_filtered_deltas.index[iter]]
                            if current_start_state.label not in [x.label for x in co_reachable_states]:
                                co_reachable_states.append(current_start_state)
                                temp_list.append(current_start_state)
                                # # print("co_reachable_states: ", co_reachable_states)
                                # # print("temp_list: ", temp_list)

                if len(temp_list) == 0:
                    end_algorithm_flag = 1
                    # # print("end_algorithm_flag = 1")
                else:
                    i += 1
                    dict_new_co_reach_states.clear()
                    list_next_states = temp_list.copy()
                    dict_new_co_reach_states.update({str(i): list_next_states})
                    # # print("dict_new_co_reach_states: ", dict_new_co_reach_states)

        for iter_x in range(len(fsa.X)):
            for iter_reach in range(len(co_reachable_states)):
                # print(str(co_reachable_states[iter_reach].label) + "=?=" + str(fsa.X[iter_x].label))
                if str(co_reachable_states[iter_reach].label) == str(fsa.X[iter_x].label):
                    fsa.X[iter_x].is_co_Reachable = 1
                    break
                else:
                    fsa.X[iter_x].is_co_Reachable = 0

    # print results
    # # print("co_reachable_states:\n", co_reachable_states)
    if len(co_reachable_states) == len(fsa.X):
        # # print("The FSA is co_reachable")
        fsa.is_co_Reachable = 1
    else:
        # # print("The FSA is not co_reachable")
        fsa.is_co_Reachable = 0

    return fsa.is_co_Reachable

def get_blockingness_info(fsa):
    # print("get_blockingness_info")
    if fsa.is_Reachable is None:
        get_reachability_info(fsa)
    if fsa.is_co_Reachable is None:
        get_co_reachability_info(fsa)

    fsa.is_Blocking = 0
    for iter_x in range(len(fsa.X)):
        if fsa.X[iter_x].is_Reachable == 1 and fsa.X[iter_x].is_co_Reachable == 0:
            fsa.X[iter_x].is_Blocking = 1
            fsa.is_Blocking = 1
        else:
            fsa.X[iter_x].is_Blocking = 0

    return fsa.is_Blocking

def get_trim_info(fsa):
    # print("get_trim_info")
    if fsa.is_Reachable is None:
        get_reachability_info(fsa)
    if fsa.is_co_Reachable is None:
        get_co_reachability_info(fsa)

    if fsa.is_Reachable == 1 and fsa.is_co_Reachable == 1:
        fsa.is_Trim = 1
    else:
        fsa.is_Trim = 0

    return fsa.is_Trim

def get_deadness_info(fsa):
    # print("get_deadness_info")
    for iter_x in range(len(fsa.X)):
        current_deltas = fsa.filter_delta(start=str(fsa.X[iter_x].label), transition=None, end=None)
        if len(current_deltas) != 0:
            fsa.X[iter_x].is_Dead = 0
        else:
            fsa.X[iter_x].is_Dead = 1

def get_co_reachability_to_x0_info(fsa):
    # print("get_co_reachability_to_x0_info")
    co_reachable_to_x0_states = []
    final_states = []

    # check if there is the initial state
    if len(fsa.x0) == 0:
        for iter_x in range(len(fsa.X)):
            fsa.X[iter_x].is_co_Reachable_to_x0 = 0
    else:
        final_states.append(fsa.x0[0])
        temp_list = []
        list_next_states = []
        dict_new_co_reach_to_x0_states = {}

        for iter_x0 in range(len(fsa.x0)):
            # # print("iter_x0: ", iter_x0)
            end_algorithm_flag = 0
            i = 0
            dict_new_co_reach_to_x0_states.clear()
            list_next_states.clear()
            list_next_states.append(fsa.x0[iter_x0])
            co_reachable_to_x0_states.append(fsa.x0[iter_x0])
            dict_new_co_reach_to_x0_states.update({str(i): list_next_states})
            # # print("dict_new_co_reach_to_x0_states: ", dict_new_co_reach_to_x0_states)
            while end_algorithm_flag == 0:
                # # print("i: ", i)
                j = 0
                temp_list.clear()
                while j < len(dict_new_co_reach_to_x0_states[str(i)]):
                    # # print("j: ", j)
                    # # print("dict_new_co_reach_to_x0_states[str(i)][j]: ", dict_new_co_reach_to_x0_states[str(i)][j])
                    current_end_filtered_deltas = fsa.filter_delta(start=None, transition=None,
                                                                   end=dict_new_co_reach_to_x0_states[str(i)][j])
                    # # print("current_end_filtered_deltas:\n", current_end_filtered_deltas)
                    j += 1
                    if len(current_end_filtered_deltas) == 0:
                        pass
                        # break
                    else:
                        for iter in range(len(current_end_filtered_deltas)):
                            current_start_state = current_end_filtered_deltas.start[current_end_filtered_deltas.index[iter]]
                            if current_start_state.label not in [x.label for x in co_reachable_to_x0_states]:
                                co_reachable_to_x0_states.append(current_start_state)
                                temp_list.append(current_start_state)
                                # # print("co_reachable_to_x0_states: ", co_reachable_to_x0_states)
                                # # print("temp_list: ", temp_list)

                if len(temp_list) == 0:
                    end_algorithm_flag = 1
                    # # print("end_algorithm_flag = 1")
                else:
                    i += 1
                    dict_new_co_reach_to_x0_states.clear()
                    list_next_states = temp_list.copy()
                    dict_new_co_reach_to_x0_states.update({str(i): list_next_states})
                    # # print("dict_new_co_reach_to_x0_states: ", dict_new_co_reach_to_x0_states)

        for iter_x in range(len(fsa.X)):
            for iter_reach in range(len(co_reachable_to_x0_states)):
                if str(co_reachable_to_x0_states[iter_reach].label) == str(fsa.X[iter_x].label):
                    fsa.X[iter_x].is_co_Reachable_to_x0 = 1
                    break
                else:
                    fsa.X[iter_x].is_co_Reachable_to_x0 = 0

    # # print("co_reachable_to_x0_states:\n", co_reachable_to_x0_states)
    if len(co_reachable_to_x0_states) == len(fsa.X):
        # # print("The FSA is co-reachable to the initial state")
        fsa.is_co_Reachable_to_x0 = 1
    else:
        # # print("The FSA is not co-reachable to the initial state")
        fsa.is_co_Reachable_to_x0 = 0

def get_reversibility_info(fsa):
    # print("get_reversibility_info")
    if fsa.is_Reachable is None:
        get_reachability_info(fsa)
    if fsa.X[0].is_co_Reachable_to_x0 is None:
        get_co_reachability_to_x0_info(fsa)

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
