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


if __name__ == "__main__":

    # List of nameservers.
    dns_list = ['1.1.1.1','8.8.8.8',
                "https://dns.google/dns-query",
                "https://cloudflare-dns.com/dns-query",
                'https://dns-staging.visafe.vn/dns-query']

    from extract_domain import *
    from settings import MOCK_DATA_FOLDER, ROOT_FOLDER

    new_links = os.path.join(MOCK_DATA_FOLDER, "new_links.txt")
    top_500 = os.path.join(MOCK_DATA_FOLDER, "top500Domains.csv")

    # Nutshell: shuffle determines if the data should be shuffled or not
    #           limit determines how much data should only be gained from a file.
    # In this case, nl_data is only taking in 10 links.
    nl_data = ExtractDomain(new_links, shuffle= True, limit = 10).data

    import pandas as pd
    top_data = pd.read_csv(top_500)['Root Domain'][:30]

    obj = DNSTest(dns_list, nl_data)

    # At the very moment, the stress test and benchmark test are not concurrent.
    # This will change in a later push.
    obj_2 = DNSTest(dns_list, nl_data)

    from datetime import datetime
    start_timer = datetime.now()
    obj.run()
    end_timer = datetime.now()

    print("Duration:", end_timer - start_timer)
    obj.report_stats(ROOT_FOLDER)

    # Benchmark. Hence, the number of instances is reduced to 1.
    obj_2.set_instance_count(1)
    start_timer = datetime.now()
    1
    end_timer = datetime.now()

    print("Duration:", end_timer - start_timer)
    obj.report_stats(ROOT_FOLDER, "Report_2.xls")