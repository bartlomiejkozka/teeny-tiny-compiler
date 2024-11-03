class emitter:
    def __init__(self, outputPath=None):
        self.outputPath = outputPath
        self.code = ''
        self.header = ''

    def emit(self, code):
        self.code += code
    
    def emitLine(self, code):
        self.code += code + '\n'

    def headerLine(self, code):
        self.header += code + '\n'
    
    def writeFile(self):
        with open(self.outputPath, 'w') as file:     
            file.write(self.codeGetter())

    def codeGetter(self):
        return self.header + self.code

        

    