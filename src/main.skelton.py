#-*- coding: utf-8 -*-

import capture

handler = capture.SSHHandler(
    host="xxx.xxx.xxx.xxx", #Host
    port=12345, #Port
    user="test", #User
    password="test", #Password
    save_path="/remote/path/to/test.pcap", #save_path
)
handler.start_capture(iface="eth0", pktcount=10, bpf_filter="tcp port 80")
handler.download_pcap("/local/path/to/test.pcap")
