#-*- coding: utf-8 -*-
from scapy.all import*
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class Parser(object):
    """
    攻撃によく利用されるプロトコルのパーサー
    """
    def __init__(self, pcap_path):
        self.pkts = rdpcap(pcap_path)

    def extract(self):
        """
        自身のプロトコルのパケットのみ抽出
        :return:
        """
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError

class HTTPParser(Parser):
    def __init__(self, *args, **kwargs):
        super(HTTPParser, self).__init__(*args, **kwargs)

    def extract(self):
        pass

    def list_ips(self):
        pass

    def list_headers(self):
        pass

    def list_payloads(self):
        pass

    def parse(self):
        s=""
        for pkt in self.pkts:
            if str(pkt).find("GET"):
                s += pkt.sprintf("{Raw:%Raw.load%}\n")
            else:
                self.logger.info("[!] this packet is not HTTP...")
        return s



