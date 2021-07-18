from src.main.MainComponents.DNSPing import DNSPing
from src.main.MainComponents.LocalStorage import AppStorage


class DNSTest:
    def __init__(self, pinged_ns: DNSPing, domain_list:list, storage : AppStorage, data_type, instance_count = 100):
        '''
        Performs DNS testing.
        :param pinged_ns: A list of nameservers that has been pinged and DNS objects of those nameservers.
            These nameservers can be a mix of IPs and DNS over HTTPS (DoH) URLs
        :param domain_list: A list of domains for testing
        :param storage: A storage to store the test results
        :param data_type: The type of domain that is being tested
        :param instance_count: The number of concurrent instances to stress test.
        '''

        self._ns, self._dns = pinged_ns.get()
        self._domain_list = domain_list
        self.instance_count = int(instance_count)
        self.storage = storage
        self.data_type = data_type

        # Records the time need to resolve in each thread for the given nameserver.
        self.thread_records = {}

        # Records the max, min, avg and std time for each nameserver.
        self.stats_records = {ns:{self.data_type:()} for ns in self._ns}

    def run(self):
        from threading import Thread
        threads = []
        for nameserver in self._dns:
            process = Thread(target=nameserver.stress, args=[self._domain_list, self.thread_records, self.stats_records, self.data_type, self.storage, self.instance_count])
            process.start()
            threads.append(process)

        for process in threads:
            process.join()

        self.storage.store_records(self.thread_records)
        self.storage.store_results(self.stats_records)


class ValidTest(DNSTest):
    def __init__(self, pinged_ns: DNSPing, domain_list:list, storage : AppStorage, instance_count = 100):
        super(ValidTest, self).__init__(pinged_ns, domain_list, storage, 'valid', instance_count)


class RandomTest(DNSTest):
    def __init__(self, pinged_ns: DNSPing, domain_list:list, storage : AppStorage, instance_count = 100):
        super(RandomTest, self).__init__(pinged_ns, domain_list, storage, 'random', instance_count)


class BlockedTest(DNSTest):
    def __init__(self, pinged_ns: DNSPing, domain_list:list, storage : AppStorage, instance_count = 100):
        super(BlockedTest, self).__init__(pinged_ns, domain_list, storage, 'blocked', instance_count)
