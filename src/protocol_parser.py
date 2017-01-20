#-*- coding: utf-8 -*-
from scapy.all import*

class Parser(object):
    """
    攻撃によく利用されるプロトコルのパーサー
    """
    def __init__(self, pcap_path):
        self.pkts = rdpcap(pcap_path)

    def parse(self):
        raise NotImplementedError

class HTTPParser(Parser):
    def __init__(self, *args, **kwargs):
        super(HTTPParser, self).__init__(*args, **kwargs)

    def list_ips(self):
        pass

    def list_payloads(self):
        pass

    def parse(self):
        return self.pkts.show()



