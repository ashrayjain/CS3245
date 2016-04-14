import xml.etree.ElementTree as et
pset = set()

with open('q1-qrels-ve.txt') as f:
    data = f.read()
    for filename in data.split('\n'):
        if filename.strip():
            with open('patsnap-corpus/' + filename.strip() + '.xml') as d:
                root = et.fromstring(d.read())
                for child in root:
                    if "IPC Primary" == child.attrib.get("name"):
                        pset.add(child.text.strip())
                        print child.text.strip(), filename.strip()


print
print
nset = set()
with open('q1-qrels+ve.txt') as f:
    data = f.read()
    for filename in data.split('\n'):
        if filename.strip():
            with open('patsnap-corpus/' + filename.strip() + '.xml') as d:
                root = et.fromstring(d.read())
                for child in root:
                    if "IPC Primary" == child.attrib.get("name"):
                        nset.add(child.text.strip())
                        print child.text.strip(), filename.strip()

print pset.intersection(nset)
