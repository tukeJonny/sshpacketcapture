#-*- coding: utf-8 -*-
# mecVovkeejMatsyas
import argparse
import getpass
import capture
import protocol_parser as pparser
import file_writer as fwriter

def parse_arguments():
    parser = argparse.ArgumentParser(description="capture tool")
    parser.add_argument("-u", "--user", type=str, help='ssh username (required)')
    parser.add_argument("-i", "--ip", type=str, help='ssh host ip (required)')
    parser.add_argument("-p", "--port", type=int, default=22, help='ssh port (required)')
    parser.add_argument("--lppath", type=str, default='.', help='path to save pcap file (local)')
    parser.add_argument("--rppath", type=str, default='/tmp/paramiko.pcap', help='path to save pcap file (remote. default /tmp/paramiko.pcap)')
    parser.add_argument("--mdpath", type=str, default='.', help='path to save md file')
    parser.add_argument("--pktcount", type=int, default=3, help='packet count (default 3)')
    parser.add_argument("--bpffileter", type=str, help="BPF Filter string")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()
    password = getpass.getpass()

    #Download
    handler = capture.SSHHandler(
        host=args.host,
        port=args.port,
        user=args.user,
        password=password,
        save_path=args.rppath #Remote Pcap Path
    )
    if args.bpffilter is None:
        handler.start_capture(iface="eth0", pktcount=args.pktcount)
    else:
        handler.start_capture(iface="eth0", pktcount=args.pktcount, bpf_filter=args.bpffilter)
    handler.download_pcap(args.lppath)

    #Parse
    http_parser = pparser.HTTPParser(args.lppath)
    parsed_obj = http_parser.parse()

    #Write to file
    mdwriter = fwriter.MarkDownWriter(parsed_obj)
    mdwriter.write(args.mdpath)

    #Close
    handler.close()



