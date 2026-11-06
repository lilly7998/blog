import re,sys
def convert(md):
    md=re.split(r'^---\s*$',md,maxsplit=2,flags=re.M)[2]
    # drop source/footer after last horizontal rule
    parts=re.split(r'^---\s*$',md,flags=re.M)
    body=parts[0]
    out=[]
    for line in body.splitlines():
        l=line.strip()
        if not l or l.startswith('!['): continue
        if l.startswith('|'):
            cells=[c.strip() for c in l.strip('|').split('|')]
            if all(re.fullmatch(r':?-+:?',c) for c in cells): continue
            out.append('，'.join(cells)+'。'); continue
        l=re.sub(r'^#+\s*','',l)
        l=re.sub(r'^[-*]\s+','',l)
        l=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',l)
        l=re.sub(r'[*_`]','',l)
        if not re.search(r'[。！？.!?：:]$',l): l+='。'
        out.append(l)
    return '\n'.join(out)
if __name__=='__main__':
    print(convert(open(sys.argv[1]).read()))
