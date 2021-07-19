from settings import VALID_CONFIG_KEYWORDS
import copy


class AppStorage:
    '''
    Stores all the information needed by the application.
    '''
    def __init__(self):
        self.nameservers = []
        self.nameservers_types = None
        self._domain_types = ['valid', 'random', 'blocked']
        errors = ['ServerDown','UnableToResolve']
        self.default_domains = {key:[] for key in self._domain_types}
        self.domains : dict = copy.deepcopy(self.default_domains)
        self.default_config = {'instance_count': [], 'domains_used':0}
        self.config = copy.deepcopy(self.default_config)

        self._test_object = None
        self._pinged = False

        self.result = []
        self.records = []
        self.error_record = {err:[] for err in errors}
        self.unable_resolve_record = {dom_type:[] for dom_type in self._domain_types if dom_type != 'random'}
        self.random_resolved = []
        self.test_state = False

        self._cur_string = ""

    @property
    def cur_string(self) -> str:
        return self._cur_string

    @cur_string.setter
    def cur_string(self, replacement:str):
        self._cur_string = replacement

    @property
    def pinged_ns(self):
        return self._test_object

    @pinged_ns.setter
    def pinged_ns(self, test_obj):
        self._test_object = test_obj

    @property
    def has_pinged(self) -> bool:
        return self._pinged

    @has_pinged.setter
    def has_pinged(self, state):
        self._pinged = state

    def add_nameserver(self, nameserver):
        self.nameservers.append(nameserver)

    def add_domain(self, domain, domain_type):
        if domain_type not in self._domain_types:
            raise KeyError("{} is an invalid key for domains".format(domain_type))
        self.domains[domain_type].append(domain)

    def add_valid_domain(self, domain):
        self.domains['valid'].append(domain)

    def add_random_domain(self, domain):
        self.domains['random'].append(domain)

    def add_blocked_domain(self, domain):
        self.domains['blocked'].append(domain)

    def add_nameservers(self, nameservers:list):
        for nameserver in nameservers:
            self.nameservers.append(nameserver)

    def add_domains(self, domains:list, domain_type):
        for domain in domains:
            self.domains[domain_type].append(domain)

    def add_valid_domains(self, domains):
        for domain in domains:
            self.domains['valid'].append(domain)

    def add_random_domains(self, domains):
        for domain in domains:
            self.domains['random'].append(domain)

    def add_blocked_domains(self, domains):
        for domain in domains:
            self.domains['blocked'].append(domain)

    def add_domain_first(self, domain, domain_type):
        self.domains[domain_type].insert(0, domain)

    def add_valid_domain_first(self, domain):
        '''
        Adds the domain to the top of the valid list
        :param domain: A domain to be added
        '''
        self.domains['valid'].insert(0, domain)

    def add_random_domain_first(self, domain):
        '''
        Adds the domain to the top of the random list
        :param domain: A domain to be added
        '''
        self.domains['random'].insert(0, domain)

    def add_blocked_domain_first(self, domain):
        '''
        Adds the domain to the top of the blocked list
        :param domain: A domain to be added
        '''
        self.domains['blocked'].insert(0, domain)

    def add_nameserver_types(self, ns_dict):
        self.nameservers_types = ns_dict

    def add_domains_first(self, domains: list, domain_type):
        new_dm = reversed(domains)
        for elem in new_dm:
            self.domains[domain_type].insert(0, elem)

    def add_valid_domains_first(self, domains: list):
        new_dm = reversed(domains)
        for elem in new_dm:
            self.domains['valid'].insert(0, elem)

    def add_random_domains_first(self, domains: list):
        new_dm = reversed(domains)
        for elem in new_dm:
            self.domains['random'].insert(0, elem)

    def add_blocked_domains_first(self, domains: list):
        new_dm = reversed(domains)
        for elem in new_dm:
            self.domains['blocked'].insert(0, elem)

    def remove_nameserver(self, nameserver):
        self.nameservers.remove(nameserver)

    def remove_all_nameservers(self):
        self.nameservers.clear()

    def remove_domains(self, domain, domain_type):
        self.domains[domain_type].remove(domain)

    def remove_valid_domain(self, domain):
        self.domains['valid'].remove(domain)

    def remove_random_domain(self, domain):
        self.domains['random'].remove(domain)

    def remove_blocked_domain(self, domain):
        self.domains['blocked'].remove(domain)

    def remove_all_domains(self, type):
        self.domains[type].clear()

    def remove_all_valid_domains(self):
        self.domains['valid'].clear()

    def remove_all_random_domains(self):
        self.domains['random'].clear()

    def remove_all_blocked_domains(self):
        self.domains['blocked'].clear()

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
        return copy.deepcopy(self.domains)

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
        self.clear_server_down_nameservers()
        self.clear_unresolved()
        self.clear_random_resolved()
        self.config = copy.deepcopy(self.default_config)

    def copy_results(self):
        new_ls = AppStorage()
        new_ls.add_nameserver_types(copy.deepcopy(self.nameservers_types))
        for ns in self.error_record['ServerDown']:
            new_ls.update_server_down(ns)

        for result in self.result:
            new_ls.store_results(result)
        for record in self.records:
            new_ls.store_records(record)
        return new_ls

    def add_unresolved_domains(self, domain, dom_type):
        if dom_type != 'random':
            dom_type_urr_domains = self.unable_resolve_record[dom_type]
            if domain not in dom_type_urr_domains:
                dom_type_urr_domains.append(domain)

    def get_unresolved_domains(self):
        return self.unable_resolve_record

    def clear_unresolved(self):
        for key in self.unable_resolve_record:
            self.unable_resolve_record[key].clear()

    def add_random_resolved(self, domain):
        if domain not in self.random_resolved:
            self.random_resolved.append(domain)

    def get_random_resolved(self):
        return self.random_resolved

    def clear_random_resolved(self):
        self.random_resolved.clear()

