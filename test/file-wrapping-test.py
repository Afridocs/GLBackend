


class specialFile(file):

    def __init__(self, key):
        self.realfile = open('/tmp/' + key, 'w+')
        print "init"

    def write(self, string):
        self.realfile.write('wrapping 1: ' + string + "\n")
        self.realfile.write('wrapping 2: ' + string + "\n")

    def close(self):
        self.realfile.close()
        print "closed"


x = specialFile('antani')
x.write('ciao')
x.write('mazurka')
x.close()
