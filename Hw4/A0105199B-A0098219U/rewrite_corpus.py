import os
from utils import xml_parse

class CorpusProcessor(object):

    def __init__(self, initial_dir):
        self.initial_dir = initial_dir

    def xml_to_text(self, destination_dir):
        for root, dirs, files in os.walk(self.initial_dir):
            for f in files:
                print 'Processing ', f
                processed_file = xml_parse(f)

                ofname = f.split('.')[0] + '.txt'
                opath = os.path.join(destination_dir, ofname)

                with open(opath, 'w') as fout:
                    fout.write(processed_file)
