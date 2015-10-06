import os, re, sys
import getopt

debug = True

def usage(progName):
    print "usage: %s [--help] [--stdin] [--count] <search> [<replace>]" % progName
    print 

def treat_file(fname, countOnly, toSearch, toReplace):
    content = open(fname, "r").read()
    
    outputContent = ''
    count = 0
    startAt = 0
    while True:
        pos = content.find(toSearch, startAt)
        if pos < 0:
            break
        
        count += 1
        
        if not countOnly:
            outputContent += content[startAt:pos] + toReplace
            
        startAt = pos + len(toSearch)

    if not countOnly and count:
        outputContent += content[startAt:]
        open(fname, "w").write(outputContent)
    
    if debug and count:
        print "%s: %d" % (fname, count)
    return count
    
if __name__ == '__main__':
    countOnly = False
    source = None
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["help", "stdin", "count"])
    except getopt.GetoptError as err:
        print str(err)
        usage(sys.argv[0])
        sys.exit(2)
        
    for option, arg in opts:
        if option in ("--help", "-h"):
            usage(sys.argv[0])
            sys.exit(0)
        elif option in ("--count"):
            countOnly = True
        elif option in ("--stdin"):
            source = sys.stdin.readlines()

    if not source:
        source = os.popen("git ls-files").readlines() 
    
    requiredArgs = 2
    if countOnly:
        requiredArgs = 1
        
    if len(args) < requiredArgs:
        print "missing arguments"
        usage(sys.argv[0])
        sys.exit(2)
    
    modified = 0
    for l in source:
        l = l.strip('\n')
        
        modified += treat_file(l, countOnly, args[0], countOnly and args[0] or args[1])
        
    if countOnly:
        print "got %d occurences" % modified