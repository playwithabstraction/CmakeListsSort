# ToDo: input-file via commandline-argument
# ToDo: option to override input-file
# ToDo: vor dem Check die Leerzeichen aus dem String entfernen
# ToDo: Duplikate entfernen

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
        #print(lineString)
        #if (lineString.startswith('target_sources(') or lineString.startswith('add_executable(')):
        if (self.isBlockStart(lineString)):
            self.outputLines.append(lineString)
            self.state='BlockState'
            self.blockLines=[]            
        #elif (lineString.startswith(')') or lineString.find('PRIVATE')>=0 or lineString.find('PUBLIC')>=0):
        elif (self.isBlockEnd(lineString)):
            #print(lineString)
            self.blockLines.sort();
            self.outputLines.extend(self.blockLines)
            self.blockLines=[]
            #print(self.blockLines)
            self.outputLines.append(lineString)
            if lineString.startswith(')'):
                self.state='CopyState'            
        else:
            if self.state=='BlockState':
                #print(lineString)
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
        #print(line)
        #writer.write(line)
        line = fileReader.readline()
    #lines.sort()
    #return lines
    return lineProcessor.outputLines

reader = open('test_input.txt', 'r')
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
