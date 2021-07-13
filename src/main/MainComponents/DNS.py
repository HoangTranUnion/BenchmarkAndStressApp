# dependencies: datetime, dnspython
# after installing dnspython, PLEASE install dnspython[doh], or DoH will NEVER work.
from src.main.MainComponents.LocalStorage import LocalStorage
from src.main.MainComponents.connection import Connection
import dns.message
import dns.resolver
from datetime import timedelta
from threading import Thread
import numpy as np
import requests.exceptions


class ServerDown(Exception):
    pass


class UnableToResolve(Exception):
    pass


class DNS:
    def __init__(self,storage: LocalStorage,  **kwargs):
        '''
        Initialize the Domain class.
        NOTE: If domain_ip and domain_url is both not None, domain_ip will be prioritized.
        :param dns_ip: Optional. The IP of the domain.
        :param dns_url: Optional. The URL of the domain. This field refers to the DNS over HTTPS (DoH) URL of the domain,
                            granted that the domain supports DoH
        '''

        # Explanation: dns_info refers to the nameserver, and self.status is to see if the nameserver is active or not.
        self.storage = storage
        if 'dns_ip' in kwargs and kwargs['dns_ip'] is not None:
            self.dns_info = kwargs['dns_ip']
            self.status = Connection.ip_status(self.dns_info, self.storage)
            self.state = 'ip'
        elif 'dns_url' in kwargs and kwargs['dns_url'] is not None:
            self.dns_info = kwargs['dns_url']
            try:
                self.status = Connection.domain_status(self.dns_info,'doh', self.storage)
            except requests.exceptions:
                self.status = 1
            self.state = 'doh'
        else:
            raise KeyError("Keyword not identified")

    @classmethod
    def ip(cls, storage, dns_ip):
        return cls(storage, dns_ip = dns_ip)

    @classmethod
    def doh_url(cls, storage, doh_url):
        return cls(storage, dns_url = doh_url)

    def _run_time(self, nameserver: str, domain: str):
        '''
            Gets the time to resolve a domain under DoH
            :param nameserver: The nameserver that is being tested
            :param domain: The domain used to test
            :return: Time needed to resolve the domain, in milliseconds.
                    Raise ServerDown if the nameserver is not active.
                    Raise UnableToResolve if the domain is not resolvable.
                    Returns "Invalid" instead if the domain is not resolved, and none of the exceptions
                        got invoked.
        '''
        my_resolver = dns.resolver.Resolver()

        # This works because dns.resolver.Resolver.resolve() automatically uses the proper protocol.
        #   - If nameserver is IP, either TCP or UDP will be used.
        #   - If nameserver is an URL with https scheme, DoH will be used.
        # Check the source code of dns.resolver.Resolver.resolve() for more info.
        my_resolver.nameservers = [nameserver]

        try:
            # Note for future references:
            # - answer.response.time returns the time in format HH:MM:SS.S, type: datetime.timedelta or float,
            #   depending on what nameserver is being used.
            # - answer.response.time.total_seconds() returns the time in seconds, type: float
            # - int + datetime.timedelta WILL cause TypeError! :PekoraTired:

            answer = my_resolver.resolve(domain)
            time_type = type(answer.response.time)
            if time_type == timedelta:
                return answer.response.time.total_seconds() * 1000
            else:
                return answer.response.time * 1000

        # Intentional bare except.
        # dns.exception is not a class that inherits BaseException class
        # any exception from that usually means that the domain cannot be resolved.

        # except dns.exception as e:
        #     print(e)
        # This causes TypeError: catching classes that do not inherit from BaseException is not allowed

        except:
            if self.status:
                raise ServerDown("Server is down.")
            domain_status = Connection.domain_status(domain, 'domain')
            if not domain_status:
                raise UnableToResolve("Unable to resolve the given domain")
            return "Invalid"

    def _single_run(self, domain_list, instance: int, total_num_inst, storage_dict:dict, data_type, storage:LocalStorage):
        '''
            Runs a single instance of testing the nameserver under the given domain list
            :param domain_list: The list of domains that are being used for testing
            :param instance: The number indicating what instance is running.
            :param storage_dict: The dict containing the resolve times across all threads.
        '''
        domain_run_time = []
        filtered = []
        running = True
        index = 0
        while running and index < len(domain_list):
            domain = domain_list[index]
            line = "{} - Thread {}/{} - Domain {}/{} - {}".format(self.dns_info, instance + 1, total_num_inst, index + 1, len(domain_list), domain)
            # text_browser.append(line + "\n")
            # text_browser.show()
            print(line)
            storage.cur_string = line
            storage.update_counter()
            try:
                res = self._run_time(self.dns_info, domain)
                domain_run_time.append(res)
                if type(res) != str:
                    filtered.append(res)
                index += 1
            except ServerDown:
                storage.update_server_down(self.dns_info)
                running = False
            except UnableToResolve:
                index += 1
        storage_dict[self.dns_info][data_type][instance] = (domain_run_time, filtered)

    def stress(self, domain_list, storage_dict, stats_dict, data_type, storage, instance_count):
        '''
        Stress test a DNS IP/DoH URL under a number of concurrent instances
        :param domain_list: A list of domains that need to be resolved
        :param storage_dict: A dict containing the resolve times across all threads.
        :param stats_dict: A dict containing the statistics for the domains.
            For an entry in this dict, the value it will have will be a tuple
            containing
                - the maximum amount of time needed to resolve a domain,
                - the minimum amount of time needed to resolve a domain
        :param instance_count:
        :return:
        '''
        print(
            "Testing {} over {} concurrent instances and {} links per instance".format(self.dns_info, instance_count,
                                                                                              len(domain_list)))
        storage_dict[self.dns_info] = {data_type:{}}

        if int(instance_count) != 0:
            threads = []
            for n in range(int(instance_count)):
                process = Thread(target= self._single_run, args=[domain_list, n, instance_count, storage_dict, data_type, storage])
                process.start()
                threads.append(process)

            for process in threads:
                process.join()

            overall_max = 0
            overall_min = np.inf

            max_length = 0
            min_length = np.inf
            total_sum = 0
            total_length = 0
            all_norm_entries = []

            for k in storage_dict[self.dns_info][data_type].keys():
                entry = storage_dict[self.dns_info][data_type][k][1]
                all_norm_entries.append(entry)
                try:
                    max_ = max(entry)
                    min_ = min(entry)
                    sum_ = sum(entry)

                    length = len(entry)
                    if length > max_length:
                        max_length = length
                    if length < min_length:
                        min_length = length

                    if max_ > overall_max:
                        overall_max = max_
                    if min_ < overall_min:
                        overall_min = min_

                    total_sum += sum_
                    total_length += length

                except ValueError:
                    pass

            if overall_min == np.inf:
                overall_min = 0
                std_dev = 0
            else:
                # all_norm_entries WILL have irregular shapes. This is due to the fact that not all links can be resolved
                # To be able to calculate the std deviation of all_norm_entries, I use np.hstack (horizontal stack)
                # dtype = object is here due to deprecation warning.
                std_dev = np.std(np.hstack(np.asarray(all_norm_entries,dtype=object)))
            if total_length == 0:
                overall_avg = 0
            else:
                overall_avg = total_sum / total_length
            stats_dict[self.dns_info][data_type] = (overall_max, overall_min, overall_avg, std_dev)
        else:
            stats_dict[self.dns_info][data_type] = (0,0,0,0)

    def __eq__(self, other):
        if isinstance(other, DNS):
            if self.dns_info == other.dns_info:
                return True
        return False

if __name__ == '__main__':
    print(DNS(dns_ip='1.1.1.1').stress(['google.com'],{}, {'1.1.1.1':{'valid':()}}, 'valid',LocalStorage(), 0))
