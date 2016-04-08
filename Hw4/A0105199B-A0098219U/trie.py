import os
import xml.etree.ElementTree as ET
import pygtrie as trie

ipc_trie = None

def init(filepath):
  global ipc_trie
  IPC_Dict = dict()

  files = os.listdir(filepath)

  for file in files:
    if file == '.DS_Store':
      continue
    try:
      doc = ET.parse(filepath + file).getroot()
      IPCs = doc.find('str/[@name="All IPC"]').text.strip()
      IPC_Raw_List = IPCs.split('|')
      IPC_List = map(lambda x: x.replace('/', '').strip(), IPC_Raw_List)
      for ipc in IPC_List:
        if ipc not in IPC_Dict:
          IPC_Dict[ipc] = set()
        
        IPC_Dict[ipc].add(file)
    except AttributeError:
      # All IPC field probably doesn't exist
      # print file
      pass

  ipc_trie = trie.CharTrie(IPC_Dict)

def find_longest_prefixes(prefix):
  pos = 0;
  count = len(ipc_trie.items(prefix[:pos]));
  while(count > 0 and pos < len(prefix)):
    try:
      pos += 1
      count = len(ipc_trie.items(prefix[:pos]));
    except KeyError:
      # prefix[:pos] doesn't exist anymore hence, return prefix[:pos - 1]
      break
  return prefix[:pos - 1]


def getfiles(prefix):
  if not ipc_trie:
    raise LookupError("Call init first")

  if prefix in ipc_trie:
    file_sets = ipc_trie.values(prefix)
    file_sets_union = reduce(lambda x, y: x.union(y), file_sets)
  else:
    longest_prefix = find_longest_prefixes(prefix)
    prefixes = ipc_trie.keys(longest_prefix)
    file_sets = map(getfiles, prefixes)
    file_sets_union = reduce(lambda x, y: x.union(y), file_sets)

  return file_sets_union
