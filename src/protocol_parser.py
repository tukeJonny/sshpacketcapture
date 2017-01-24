#-*- coding: utf-8 -*-
from collections import defaultdict
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from http_parser.http import HttpStream, HttpParser
from scapy.all import*

class Parser(object):
    """
    攻撃によく利用されるプロトコルのパーサー
    """
    def __init__(self, pcap_path):
        self.pkts = rdpcap(pcap_path)

    def extract_generator(self):
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
        self.methods = ["GET", "POST"]
        self.only_request = True

    def extract_generator(self, pkts):
        for pkt in pkts:
            if pkt[TCP].dport == 80 or not self.only_request:
                yield pkt

    # def list_ips(self):
    #     ips = []
    #     for pkt in self.extract_generator():
    #         if pkt.haslayer(IP):
    #             ips.append(pkt[IP].src)
    #     return ips

    def list_headers(self):
        pass

    def list_sessions(self):
        sessions = [(k,v) for k, v in self.pkts.sessions().items()]
        return sessions

    def list_payloads(self):
        payloads = []
        for pkt in self.extract_generator():
                payloads.append(pkt.sprintf("{Raw:%Raw.load%}\n").split('\n'))
        return payloads

    def parse(self):
        ret = {
            'sessions': {

            }
        }
        for session, pkts in self.pkts.sessions().items():
            ret['sessions'][session] = []
            for pkt in self.extract_generator(pkts):
                if pkt.haslayer(Raw):
                    raw = pkt[Raw].load
                    p = HttpParser()
                    p.execute(raw, len(raw))
                    ret['sessions'][session].append({
                        'method': p.get_method(),
                        'url': [
                            ('full_url', p.get_url()),
                            ('path', p.get_path()),
                            ('query', p.get_query_string()),
                            ('fragment', p.get_fragment()),
                        ],
                        'version': p.get_version(),
                        'headers': p.get_headers(),
                        'body': p.recv_body(),
                    })
        return ret


