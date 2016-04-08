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

def getfiles(prefix):
  if not ipc_trie:
    raise LookupError("Call init first")

  file_sets = ipc_trie.values(prefix)
  file_sets_union = reduce(lambda x, y: x.union(y), file_sets)
  return file_sets_union
