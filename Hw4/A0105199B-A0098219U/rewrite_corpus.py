import os
import codecs
from utils import xml_parse, raw_preprocess_text

class CorpusProcessor(object):

    def __init__(self, initial_dir):
        self.initial_dir = initial_dir

    def xml_to_text(self, destination_dir):
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        for root, dirs, files in os.walk(self.initial_dir):
            for f in files:
                fdata = ''

                inpath = os.path.join(self.initial_dir, f)

                with open(inpath, 'r') as fin:
                    fdata = fin.read().decode('utf-8')

                processed_file = raw_preprocess_text(xml_parse(fdata))

                ofname = f.split('.')[0] + '.xml'
                opath = os.path.join(destination_dir, ofname)

                with codecs.open(opath, 'w', 'ascii', errors='ignore') as fout:
                    fout.write(processed_file)
