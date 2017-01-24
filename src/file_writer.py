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
            for session in self.parsed_obj['sessions'].keys():
                f.write("## {}\n".format(session))
                for idx, pkt in enumerate(self.parsed_obj['sessions'][session]):
                    f.write('[{}]\n'.format(idx))
                    #Method
                    f.write('### Method: \n'),
                    f.write('\t- {}\n'.format(pkt['method']))

                    #URL
                    f.write('### URL: \n'),
                    for name, value in pkt['url']:
                        f.write('\t- {}: {}\n'.format(name, value))

                    #Version
                    f.write('### Version: \n'),
                    f.write('\t- {}\n'.format(pkt['version']))

                    #Headers
                    f.write('### Headers: \n')
                    for header,value in pkt['headers'].items():
                        f.write('\t- {}: {}\n'.format(header, value))

                    #Body
                    f.write('### Body: \n')
                    f.write(pkt['body'].decode('utf-8'))

class TextWriter(Writer):
    def __init__(self):
        pass
