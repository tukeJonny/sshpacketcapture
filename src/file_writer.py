#-*- coding:  utf-8 -*-

class Writer(object):
    """
    解析結果を書き出すファイルの形式ごとのWriter
    """
    def __init__(self):
        pass


class MarkDownWriter(Writer):
    def __init__(self, parsed_obj):
       self.parsed_obj = parsed_obj

    def write(self, fpath):
        with open(fpath, "w") as f:
            f.write("# ")
            for session in self.parsed_obj['sessions'].keys():
                f.write("# {}\n".format(session))
                for pkt in self.parsed_obj['sessions'][session]:
                    f.write('## Method: {}\n'.format(pkt['method'])),
                    f.write('## URL: {}\n'.format(pkt['url'])),
                    f.write('## Version: {}\n'.format(pkt['version'])),
                    f.write('## Headers: \n')
                    for header,value in pkt['headers'].items():
                        f.write('\t- {}: {}\n'.format(header, value))
                f.write('\n-----\n')

class TextWriter(Writer):
    def __init__(self):
        pass
