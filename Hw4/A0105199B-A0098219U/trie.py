import os
import re
import xml.etree.ElementTree as ET
import pygtrie as trie

ipc_trie = None
splitter = re.compile('[A-Z]')


def init(filepath):
    global ipc_trie
    IPC_Dict = {}
    files = os.listdir(filepath)
    for f in files:
        if f == '.DS_Store':
            continue
        doc = ET.parse(filepath + f).getroot()
        ipc_node = doc.find('str/[@name="All IPC"]')
        if ipc_node is not None:
            ipcs = ipc_node.text.strip().split('|')
            for ipc in ipcs:
                ipc_parts = ipc.strip().split('/')
                split_len = len(ipc_parts[0]) - \
                    splitter.search(ipc_parts[0][::-1]).span()[0]
                normalized_ipc = ipc_parts[0][:split_len]
                normalized_ipc += ipc_parts[0][split_len:].rjust(4, '0')
                normalized_ipc += ipc_parts[1].ljust(6, '0')
                IPC_Dict.setdefault(normalized_ipc, set()).add(f)
    ipc_trie = trie.CharTrie(IPC_Dict)


def find_longest_prefixes(prefix):
    longest_prefix = prefix in ipc_trie or ipc_trie.has_subtrie(prefix)
    if longest_prefix:
        return prefix
    for i in xrange(-1, -len(prefix), -1):
        temp_prefix = prefix[:i]
        if temp_prefix in ipc_trie or ipc_trie.has_subtrie(temp_prefix):
            return temp_prefix
    return None


def getfiles(prefix):
    if not ipc_trie:
        raise LookupError("Call init first")

    if prefix in ipc_trie:
        file_sets = ipc_trie.values(prefix)
    else:
        longest_prefix = find_longest_prefixes(prefix)
        file_sets = ipc_trie.values(longest_prefix)
    file_sets_union = reduce(lambda x, y: x.union(y), file_sets)
    return file_sets_union
