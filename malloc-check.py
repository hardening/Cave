import os, re, sys


ANALYZED_FILES = ('c', 'cxx', 'cpp')

STATE_SEARCH, STATE_CHECK = range(0, 2)
MAX_SCAN = 5

mallocRe = re.compile("([^=]+)=\\s*malloc\\s*\\(")
callocRe = re.compile("([^=]+)=\\s*calloc\\s*\\(")
strdupRe = re.compile("([^=]+)=\\s*_?strdup\\s*\\(")

ifRe = re.compile("\\s*if\\s*\\((.*)")
returnRe = re.compile("\\sreturn(.+)")

def treat_file(fname):
    line_no = 0
    state = STATE_SEARCH
    
    f = open(fname, "r")
    lines = []
    for l in f.readlines():
        lines.append(l[0:-1])
    
    nlines = len(lines)
    for i in range(0, nlines):
        l = lines[i]

        v = mallocRe.search(l)
        if not v:
            v = callocRe.search(l)
            
            if not v:
                v = strdupRe.search(l)
        
        if not v:
            continue
        
        if ifRe.match(l):
            continue
        
        if returnRe.match(l):
            continue
        
        # retrieve the variables
        vars = v.group(1).strip(" \t").split("=")
        toSearch = []
        for v in vars:
            index = v.rfind(" ")
            toAdd = v
            if index > 0:
                toAdd = v[index+1:]

            if toAdd[0] == "*":
                toAdd = toAdd[1:]
            toSearch.append(toAdd)
            
        # then scan next lines for a if or a return referencing one of this variables
        endScan = i + MAX_SCAN
        if endScan > nlines:
            endScan = nlines
        
        found = False
        for j in range(i + 1, endScan):
            m = ifRe.match(lines[j])
            if m:
                ifStatement = m.group(1)
                for v in toSearch:
                    if v in ifStatement:
                        found = True
                        break

            m = returnRe.match(lines[j])
            if m:
                retStatement = m.group(1)
                for v in toSearch:
                    if v in retStatement:
                        found = True
                        break
            
            if found:
                break
        
        if not found:
            #print "vars=%s" % toSearch
            for j in range(i, endScan):
                print "%s:%d: %s" % (fname, j, lines[j])
            print "====================================================================="
            
            
            
    f.close()
    
if __name__ == '__main__':
    source = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stdin":
            source = sys.stdin.readlines()
        else:
            source = fopen(sys.argv[1], "r").readlines()
    else:
        source = os.popen("git ls-files").readlines() 
    
    for l in source:
        l = l.strip('\n')
        tokens = l.split('.')
        if l[-1] not in ANALYZED_FILES:
            continue  
        
        treat_file(l)