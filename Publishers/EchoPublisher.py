import Publisher

class EchoPublisher (Publisher.Publisher):

    def refreshRate(self):
        return 5

    def publish(self, watt, temp):


        print "Watt : %i" % watt
        print "Temperature : %i" % temp
        return True
