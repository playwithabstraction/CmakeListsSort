#!/usr/bin/python

# ToDo: option to override input-file
# ToDo: vor dem Check die Leerzeichen aus dem String entfernen
# ToDo: Duplikate entfernen

import sys

class CMakeListsProcessor:
    def __init__(self):
        self.state='CopyState'
        self.blockLines=[]
        self.outputLines=[]

    def isBlockStart(self,lineString):
        if (lineString.find(')')>=0):
            return False
        elif (lineString.startswith('target_sources(')):
            return True
        elif (lineString.startswith('add_executable(')):
            return True
        else:
            return False

    def isBlockEnd(self,lineString):
        if (lineString.startswith(')') or lineString.find('PRIVATE')>=0 or lineString.find('PUBLIC')>=0):
            return True
        else:
            return False

    def processLine(self,lineString):
        if (self.isBlockStart(lineString)):
            self.outputLines.append(lineString)
            self.state='BlockState'
            self.blockLines=[]            
        elif (self.isBlockEnd(lineString)):
            self.blockLines.sort();
            self.outputLines.extend(self.blockLines)
            self.blockLines=[]
            self.outputLines.append(lineString)
            if lineString.startswith(')'):
                self.state='CopyState'            
        else:
            if self.state=='BlockState':
                self.blockLines.append(lineString)
            else:
                self.outputLines.append(lineString)


def testFunc(fileReader):
    lineProcessor=CMakeListsProcessor()
    lines = []
    line = fileReader.readline()
    while line != '':  # The EOF char is an empty string
        lines.append(line)
        lineProcessor.processLine(line)
        line = fileReader.readline()
    return lineProcessor.outputLines

if (len(sys.argv)!=2):
    print "CMakeLists.txt source-file sorter v0.1.0"
    print "usage: " + sys.argv[0] + " <FileNameWithPath>"
    exit()
reader = open(sys.argv[1], 'r')
writer = open('test_output.txt','w')
try:
    lines = testFunc(reader)
    #lines.sort()
    for line in lines:
        writer.write(line)
    #print(lines)
finally:
    reader.close()
    writer.close()
