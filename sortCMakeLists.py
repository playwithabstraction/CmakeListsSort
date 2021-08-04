#!/usr/bin/python

# ToDo: vor dem Check die Leerzeichen aus dem String entfernen

import sys

def removeListDuplicatesAndSort(inputList):
    return sorted(set(inputList))


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
            self.outputLines.extend(removeListDuplicatesAndSort(self.blockLines))
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


def printUsage(progName):
    print "CMakeLists.txt source-file sorter v0.1.0"
    print "usage: " + progName + " <FileNameWithPath> [options]"
    print "--override 	overrides the input-file"
    return

if (len(sys.argv)<2 or len(sys.argv)>3):
    printUsage(sys.argv[0])
    exit()

if (len(sys.argv)==3 and sys.argv[2]!='--override'):
    printUsage(sys.argv[0])
    exit()

outputFile='output.txt'
if (len(sys.argv)==3 and sys.argv[2]=='--override'):
    outputFile=sys.argv[1]
reader = open(sys.argv[1], 'r')
try:
    lines = testFunc(reader)
    writer = open(outputFile,'w')
    for line in lines:
        writer.write(line)
finally:
    reader.close()
    writer.close()
    
