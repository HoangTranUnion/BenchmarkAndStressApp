from src.main.MainComponents.DNS import DNS
import dns.inet


class DNSPing:
    '''
    Pings the listed nameservers.
    '''
    def __init__(self, ns_list, storage):
        self._ns_list = ns_list
        self._dns_list = [self._create_dns_obj(storage, nameserver) for nameserver in ns_list]
        self._dns_types = {dns_obj.dns_info: dns_obj.state for dns_obj in self._dns_list}
        self.storage = storage
        self.storage.add_nameserver_types(self._dns_types)

    @staticmethod
    def _create_dns_obj(storage, nameserver):
        if dns.inet.is_address(nameserver):
            return DNS.ip(storage, nameserver)
        else:
            return DNS.doh_url(storage, nameserver)

    def get(self):
        return self._ns_list, self._dns_list

    def __len__(self):
        return len(self._dns_list)

