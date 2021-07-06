# install dnspython: pip install dnspython
import subprocess
import requests


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
        For IP - 0 if the IP is active, 1 if the IP is not active, and 2 for errors.
        For Domains - 0 if the connection can established, 1 otherwise.
    '''

    def __init__(self, domain_ip = None, domain_url = None, url_type = None):
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
        '''

        self._domain_ip = domain_ip
        self._domain_url = domain_url
        self._url_type = url_type
        if self._domain_url is not None:
            assert self._url_type is not None
        self.status = self._check()

    @classmethod
    def ip_status(cls, domain_ip):
        return cls(domain_ip).status

    @classmethod
    def domain_status(cls, domain_url, url_type):
        return cls(None, domain_url, url_type).status

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
                return 1
            return 0
        except requests.ConnectionError:
            return 1

    def _ping(self, ipaddress):
        proc = subprocess.Popen(
            ['ping', ipaddress],
            stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        print("Pinged IP/URL {} with return code {}".format(ipaddress, proc.returncode))
        return proc.returncode


if __name__ == '__main__':
    new_connection = Connection('103.192.236.108').status
    print(new_connection)
    new_connection_2 = Connection(domain_url='google.com',url_type='domain')
    print(new_connection_2.status)
    new_connection_3 = Connection('1.1.1.1', url_type='doh')
    print(new_connection_3.status)
    new_connection_4 = Connection('1.1.1.1', domain_url='google.com',url_type='domain')
    print(new_connection_4.status)
    try:
        nc_5 = Connection(domain_url='google.com')
    except AssertionError:
        print("Assert Failed. No url type specified")

    nc_6 = Connection(domain_url='https://staging.visafe.vn/dns-query', url_type='doh')
    print(nc_6.status)

    nc_7 = Connection.domain_status('petmart.vn', 'domain')
    print("link: petmart.vn - status:", nc_7)
