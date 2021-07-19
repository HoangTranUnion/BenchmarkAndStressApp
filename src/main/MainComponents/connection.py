# install dnspython: pip install dnspython
import subprocess
import requests
from src.main.MainComponents.LocalStorage import AppStorage

class Connection:
    '''
    Checks the status of the given domain IP, DoH URL or normal URL.
    For convenience, if you have already known what type you are checking,
        instead of instantiating the Connection class, you can do

    ```
    ip_stat = Connection.ip_status(ip) # for IPs
    doh_stat = Connection.domain_status(domain, 'doh') # for DoH urls
    domain_stat = Connection.domain_status(domain, 'domain') # for normal domains
    ```
    :returns
        For IP and DoH URL - 0 if the IP is active, 1 if the IP is not active, and 2 for errors.
        For Domains - 0 if the connection can established, 1 otherwise.
    '''

    def __init__(self, domain_ip = None, domain_url = None, url_type = None, storage :AppStorage = None):
        '''
        Initializes the Connection class.
        NOTE: If domain_ip and domain_url is both not None, domain_ip will be prioritized.
        :param domain_ip: Optional. The IP of the domain.
        :param domain_url: Optional. The URL of the domain.
                This field can refer to both the DNS over HTTPS (DoH) URL of the domain,
                granted that the domain supports DoH; and the normal domain link
                (https://google.com, or google.com for instance)
        :param url_type: Optional - must be used if domain_url is present.
                Specifies the type of the input url
                Options: 'doh' or 'domain'.
                Raises AssertionError if domain_url is present but url_type is not
        :param storage: Optional - only useful if you want to store the ping status to a domain.
        '''

        self._domain_ip = domain_ip
        self._domain_url = domain_url
        self._url_type = url_type
        if self._domain_url is not None:
            assert self._url_type is not None
        else:
            if self._url_type is not None:
                raise AssertionError("There should be a domain associated with the url type")
        self.storage = storage

        self.status = self._check()

    @classmethod
    def ip_status(cls, domain_ip, storage = None):
        return cls(domain_ip, storage = storage).status

    @classmethod
    def domain_status(cls, domain_url, url_type, storage = None):
        return cls(None, domain_url, url_type, storage).status

    def _check(self):
        if self._domain_ip is None and self._domain_url is None:
            return False
        elif self._domain_ip is not None:
            return self._verify_connection(self._domain_ip, 'ip')
        elif self._domain_url is not None:
            return self._verify_connection(self._domain_url, self._url_type)

    def _verify_connection(self, target, type):
        if type.lower() == 'ip':
            return self._ping(target)
        if type.lower() == 'doh':
            stripped_url = target.replace("https://","").replace("/dns-query","")
            return self._ping(stripped_url)
        else:
            if "https://" not in target and "http://" not in target:
                if "https:" in target:
                    url_to_req_https = self._domain_url.replace("https:", "https://")
                    return self._req(url_to_req_https)
                elif "http:" in target:
                    url_to_req_http = target.replace("http:", "http://")
                    return self._req(url_to_req_http)
                else:
                    url_to_req_https = "https://" + target
                    url_to_req_http = "http://" + target
                return self._req(url_to_req_https) or self._req(url_to_req_http)
            else:
                return self._req(target)

    def _req(self, url):
        try:
            r = requests.get(url, headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.114 Safari/537.36"})
            sc = r.status_code
            if str(sc).startswith("4") or str(sc).startswith("5"):
                return False
            return True
        except requests.ConnectionError:
            return False

    def _ping(self, ipaddress):
        proc = subprocess.Popen(
            ['ping', ipaddress],
            stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        ping_str = "Pinged IP/URL {} with return code {}".format(ipaddress, proc.returncode)
        if self.storage is not None:
            self.storage.cur_string = ping_str
        print(ping_str)
        return proc.returncode

