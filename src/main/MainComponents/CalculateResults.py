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

    all_entries = [list(list(record_dict.values())[i].values())[0][1] for i in range(len(list(record_dict.items()))) if len(record_dict[list(record_dict.keys())[i]][0][1]) != 0]
    if len(all_entries) != 0:
        stack = np.hstack(np.asarray(all_entries,dtype=object))
        avg_ = np.average(stack.astype(float))
        std_ = np.std(stack)
    else:
        avg_, std_ = 0, 0
    return max_, min_, avg_, std_


if __name__ == "__main__":
    import random
    record_ = {'valid':(2,1,0.6,0.4), 'random':(0,0,0,0), 'blocked': (13,4,3,0.6)}
    results = {'valid':{0:[random.randint(1,4) for _ in range(10)], 1: [random.randint(1,4) for _ in range(10)], 2: [random.randint(1,4) for _ in range(10)]},
               'random': {0:[random.randint(1,4) for _ in range(10)], 1: [random.randint(1,4) for _ in range(10)], 2: [random.randint(1,4) for _ in range(10)]},
               'blocked': {0:[random.randint(1,4) for _ in range(10)], 1: [random.randint(1,4) for _ in range(10)], 2: [random.randint(1,4) for _ in range(10)]}}

    print(calculate_res(record_, results))