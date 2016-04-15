import os
import re
import xml.etree.ElementTree as ET
import pygtrie.pygtrie as trie
import pickle


class Trie(object):
    """
    Trie to map a IPC code to a patent document in patsnap corpus. It utilizes the pygtrie library to store and retrieve patent documents corresponding to an IPC code.
    """
    splitter = re.compile('[A-Z]')
    saved_filename = "trie_obj"

    def __init__(self, filepath=None):
        """
        Creates a new Trie object for the patsnap corpus from the filepath specified. If no filepath is specifed, it loads the previously created Trie object stored as a file.
        """
        self.ipc_trie = None
        self.ipc_dict = None
        if filepath is None:
            with open(self.saved_filename, "rb") as f:
                self.ipc_dict = pickle.load(f)
                self.ipc_trie = trie.CharTrie(self.ipc_dict)
        else:
            self.create_trie(filepath)

    def create_trie(self, filepath):
        """
        Creates a new Trie object from the patsnap corpus directory specified in the filepath.
        """ 
        self.ipc_dict = {}
        files = os.listdir(filepath)
        for f in files:
            if f == '.DS_Store':
                continue
            doc = ET.parse(os.path.join(filepath, f)).getroot()
            ipc_node = doc.find('str/[@name="All IPC"]')
            if ipc_node is not None:
                ipcs = ipc_node.text.strip().split('|')
                for ipc in ipcs:
                    ipc_parts = ipc.strip().split('/')
                    split_len = len(ipc_parts[0]) - \
                        self.splitter.search(ipc_parts[0][::-1]).span()[0]
                    normalized_ipc = ipc_parts[0][:split_len]
                    normalized_ipc += ipc_parts[0][split_len:].rjust(4, '0')
                    normalized_ipc += ipc_parts[1].ljust(6, '0')
                    self.ipc_dict.setdefault(normalized_ipc, set()).add(f)
        self.ipc_trie = trie.CharTrie(self.ipc_dict)

    def find_longest_prefixes(self, prefix):
        """
        Returns the longest prefix of the specified IPC prefix contained in the Trie.  
        """ 
        longest_prefix = prefix in self.ipc_trie or \
            self.ipc_trie.has_subtrie(prefix)
        if longest_prefix:
            return prefix
        for i in xrange(-1, -len(prefix), -1):
            temp_prefix = prefix[:i]
            if temp_prefix in self.ipc_trie or \
                    self.ipc_trie.has_subtrie(temp_prefix):
                return temp_prefix
        return None

    def getfiles(self, prefix):
        """
        Returns all the a set of patent numbers that reference the IPC code given. If only a prefix of the IPC code is given, it returns all the patent documents referencing IPC codes starting with that prefix.  
        """
        if not self.ipc_trie:
            raise LookupError("Call init first")

        if prefix in self.ipc_trie:
            file_sets = self.ipc_trie.values(prefix)
        else:
            longest_prefix = self.find_longest_prefixes(prefix)
            file_sets = self.ipc_trie.values(longest_prefix)
        file_sets_union = reduce(lambda x, y: x.union(y), file_sets)
        return file_sets_union

    def save(self):
        """
        Saves the current Trie object to disk.
        """ 
        with open(self.saved_filename, "wb") as f:
            pickle.dump(self.ipc_dict, f, -1)
