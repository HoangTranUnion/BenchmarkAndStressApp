from src.main.MainComponents.DNS import DNS
from src.main.MainComponents.LocalStorage import LocalStorage
import dns.inet


class DNSTest:
    def __init__(self, dns_list:list, domain_list:list, storage : LocalStorage, data_type, instance_count = 100):
        '''
        Performs DNS testing.
        :param dns_list: A list of nameservers. This can be a mix of IPs and DNS over HTTPS (DoH) URLs
        '''

        self._dns_list = [self._create_dns_obj(nameserver) for nameserver in dns_list]
        self._dns_types = {dns_obj.dns_info: dns_obj.state for dns_obj in self._dns_list}
        self._domain_list = domain_list
        self.instance_count = int(instance_count)
        self.storage = storage
        self.data_type = data_type

        self.storage.add_nameserver_types(self._dns_types)

        self.total = self.instance_count * len(self._dns_list) * len(self._domain_list)

        # Records the time need to resolve in each thread for the given nameserver.
        self.thread_records = {}

        # Records the max, min, avg and std time for each nameserver.
        self.stats_records = {ns:{self.data_type:()} for ns in dns_list}

    @staticmethod
    def _create_dns_obj(nameserver):
        if dns.inet.is_address(nameserver):
            return DNS.ip(nameserver)
        else:
            return DNS.doh_url(nameserver)

    def add_dns(self, nameserver: str):
        self._dns_list.append(self._create_dns_obj(nameserver))

    def remove_dns(self, nameserver:str):
        dns_obj = self._create_dns_obj(nameserver)
        self._dns_list.remove(dns_obj)

    def set_instance_count(self, new_ic):
        self.instance_count = new_ic

    def run(self):
        from threading import Thread
        threads = []
        for nameserver in self._dns_list:
            process = Thread(target=nameserver.stress, args=[self._domain_list, self.thread_records, self.stats_records, self.data_type, self.storage, self.instance_count])
            process.start()
            threads.append(process)

        for process in threads:
            process.join()

        self.storage.store_records(self.thread_records)
        self.storage.store_results(self.stats_records)

    def get_stats(self):
        return self.stats_records
