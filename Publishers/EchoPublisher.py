
class EchoPublisher:
    def __init__(self, config):
        pass

    def refreshRate(self):
        return 5

    def publish(self, since, to, watt, temp):


        print "Watt : %i" % watt
        print "Temperature : %i" % temp
        return True
