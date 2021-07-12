from settings import VALID_CONFIG_KEYWORDS
import copy, math


class LocalStorage:
    '''
    Stores all the information needed by the application.
    Attributes:
        - nameservers: The list of nameservers that are being tested
        - nameservers_types: The dictionary of types of the nameservers. By default, this field is None
        - domains: The list domains that are being used to resolve
        - config: The configurations for the app.
        - random: The list containing randomly generated links. By default, this is None.
    '''
    def __init__(self):
        self.nameservers = []
        self.nameservers_types = None
        self.domain_types = ['valid','random','blocked']
        errors = ['ServerDown','UnableToResolve']
        self.default_domains = {key:[] for key in self.domain_types}
        self.domains = copy.deepcopy(self.default_domains)
        self.default_config = {'instance_count': [], 'domains_used':0}
        self.config = copy.deepcopy(self.default_config)
        self.result = []
        self.records = []
        self.error_record = {err:[] for err in errors}
        self.test_state = False

        self._cur_string = ""
        self._test_counter = 0

    def _update_total(self):
        inst_list = self.config['instance_count']
        ns_len = len(self.nameservers)
        if len(inst_list) != 0: # in theory, should only happen when we specify the number of instances
            return sum([val * ns_len * self.config['domains_used'] for val in inst_list])
        else:
            return 0

    def update_counter(self):
        self._test_counter += 1

    def get_progress(self):
        print(self._update_total())
        return math.floor(self._test_counter / self._update_total())

    @property
    def cur_string(self) -> str:
        return self._cur_string

    @cur_string.setter
    def cur_string(self, replacement:str):
        self._cur_string = replacement

    def add_nameserver(self, nameserver):
        self.nameservers.append(nameserver)
        self._update_total()

    def add_domain(self, domain, domain_type):
        if domain_type not in self.domain_types:
            raise KeyError("{} is an invalid key for domains".format(domain_type))
        self.domains[domain_type].append(domain)
        self._update_total()

    def add_nameservers(self, nameservers:list):
        for nameserver in nameservers:
            self.nameservers.append(nameserver)
        self._update_total()

    def add_domains(self, domains:list, domain_type):
        for domain in domains:
            self.domains[domain_type].append(domain)
        self._update_total()

    def add_domain_first(self, domain, domain_type):
        self.domains[domain_type].insert(0, domain)
        self._update_total()

    def add_nameserver_types(self, ns_dict):
        self.nameservers_types = ns_dict

    def add_domains_first(self, domains: list, domain_type):
        new_dm = reversed(domains)
        for elem in new_dm:
            self.domains[domain_type].insert(0, elem)
        self._update_total()

    def remove_nameserver(self, nameserver):
        self.nameservers.remove(nameserver)
        self._update_total()

    def remove_all_nameservers(self):
        self.nameservers.clear()
        self._update_total()

    def remove_domains(self, domain, domain_type):
        self.domains[domain_type].remove(domain)
        self._update_total()

    def remove_all_domains(self, type):
        self.domains[type].clear()
        self._update_total()

    def replace_nameservers(self, new_nameser_set):
        self.nameservers = new_nameser_set

    def replace_domains(self, new_dom_set):
        self.domains = new_dom_set

    def modify_nameserver(self, original, modified):
        ori_index = self.nameservers.index(original)
        ori = self.nameservers.pop(ori_index)
        self.nameservers.insert(ori_index, modified)

    def modify_domain(self, domain_type, original, modified):
        ori_index = self.domains[domain_type].index(original)
        ori = self.domains[domain_type].pop(ori_index)
        self.domains[domain_type].insert(ori_index, modified)

    def get_domains(self):
        return self.domains

    def get_domain_by_section(self, section):
        return self.domains[section]

    def get_valid_domains(self):
        return self.domains['valid']

    def get_random_domains(self):
        return self.domains['random']

    def get_blocked_domains(self):
        return self.domains['blocked']

    def get_nameservers(self):
        return self.nameservers

    def get_all(self):
        return self.nameservers, self.domains

    def store_results(self, results):
        self.result.append(results)

    def store_records(self, records):
        self.records.append(records)

    def _mod_test_results(self):
        ret_records = {}
        ret_results = {}
        for i in range(len(self.result)):
            for key in self.result[i]:
                if key not in ret_results:
                    ret_results[key] = {}
                ret_results[key].update(self.result[i][key])
            for key in self.records[i]:
                if key not in ret_records:
                    ret_records[key] = {}
                ret_records[key].update(self.records[i][key])
        return ret_results, ret_records

    def get_test_results(self):
        return self._mod_test_results()

    def get_nameserver_types(self):
        return self.nameservers_types

    def modify_config(self, keyword, value):
        if keyword not in VALID_CONFIG_KEYWORDS:
            raise KeyError("{} is an invalid keyword".format(keyword))
        self.config[keyword] = value
        self._update_total()

    def get_config(self):
        return self.config

    @property
    def cur_test_state(self):
        return self.test_state

    @cur_test_state.setter
    def cur_test_state(self, state):
        self.test_state = state

    def update_server_down(self, nameserver):
        if nameserver not in self.error_record['ServerDown']:
            self.error_record['ServerDown'].append(nameserver)

    def get_server_down_nameservers(self):
        return self.error_record['ServerDown']

    def clear_server_down_nameservers(self):
        self.error_record['ServerDown'].clear()

    def reset(self):
        self.result.clear()
        self.records.clear()
        self.config = copy.deepcopy(self.default_config)

    def copy_results(self):
        new_ls = LocalStorage()
        new_ls.add_nameserver_types(copy.deepcopy(self.nameservers_types))
        for ns in self.error_record['ServerDown']:
            new_ls.update_server_down(ns)

        for result in self.result:
            new_ls.store_results(result)
        for record in self.records:
            new_ls.store_records(record)
        return new_ls
