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


if __name__ == "__main__":
    import random
    copy_1 = [random.randint(1,4) for _ in range(10)]
    copy_2 =[random.randint(1,4) for _ in range(10)]
    record_ = {'valid':(2,1,0.6,0.4), 'random':(0,0,0,0), 'blocked': (0,0,0,0)}
    results = {'valid':{0:(copy_1,copy_1), 1: (copy_2, copy_2)},
               'random': {},
               'blocked': {}}

    print(calculate_res(record_, results))