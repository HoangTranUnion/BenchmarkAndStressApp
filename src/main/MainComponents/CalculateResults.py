import numpy as np


def calculate_res(result_dict, record_dict):
    '''
    Calculate the results for the tests on a nameserver
    :param result_dict: The resulting dictionary for different types of domains.
        Each entry in the dictionary has the type of domain as key, and the tuple containing the
        maximum, minimum, average and standard deviation response time to resolve a number of domains as the value
    :param record_dict: The dictionary that records the results from testing different types of domains.
        Each entry in the dictionary has the type of domain as key, and the dictionary containing
        the response times recorded in each thread for each link as the value.
    :return: The tuple containing the maximum, minimum, average, and standard deviation response time to
        resolve a number of domains.
    '''
    max_ = 0
    min_ = np.inf
    for entry_key in result_dict:
        entry_max, entry_min, avg, std = result_dict[entry_key]
        if entry_max > max_:
            max_ = entry_max
        if entry_min < min_ and avg != 0:
            min_ = entry_min

    all_entries = []
    for key in record_dict.keys():
        value_dict = record_dict[key]
        all_instances_in_dict = list(value_dict.keys())
        if len(all_instances_in_dict) != 0:
            for instance in all_instances_in_dict:
                filtered_result = value_dict[instance][1]
                if len(filtered_result) != 0:
                    all_entries.append(filtered_result)

    if len(all_entries) != 0:
        stack = np.hstack(np.asarray(all_entries,dtype=object))
        avg_ = np.average(stack.astype(float))
        std_ = np.std(stack)
    else:
        avg_, std_ = 0, 0
    return max_, min_, avg_, std_
