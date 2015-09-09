# socat tcp-connect:172.17.42.1:8122 tun:192.168.0.1/24,up
import random
from twisted.internet import reactor, protocol
import logging

P_FULLDROP = 10
P_HALFDROP = 10
P_CUTIT = 20

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def __init__(self,name,):
        """

        """
        self.dest=None
        self.name = name
        self.actionTable = {}

        i =0
        for _ in range(P_FULLDROP):
            self.actionTable[i] = self.fulldrop
            i+=1
        for _ in range(P_HALFDROP):
            self.actionTable[i] = self.halfdrop
            i+=1
        for _ in range(P_CUTIT):
            self.actionTable[i] = self.cutit
            i+=1
        while i < 100:
            self.actionTable[i] = self.passit
            i+=1

        self.log= logging.getLogger("ECHO:"+name)
    

    def cutit(self,data):
        self.log.info(" cut %s",len(data))
        cut = len(data)/2
        self.dest.transport.write(data[:cut])
        self.dest.transport.write(data[cut:])
    
    def halfdrop(self,data):
        self.log.info(" halfdrop %s",len(data))
        cut = len(data)/2
        self.dest.transport.write(data[:cut])

    def fulldrop(self,data):
        self.log.info(" fulldrop %s",len(data))
    
    def passit(self,data):
        self.log.info(" write %s",len(data))
        self.dest.transport.write(data)

    def dataReceived(self, data):
        "As soon as any data is received, write it back."

        if self.dest:
            number = random.randint(0,99)
            self.actionTable[number](data)
        else:
            self.log.debug("no dest")

def createServerEcho():
    global SRV
    global CLIENT
    SRV=Echo("SRV")
    print "create Server"
    SRV.dest=CLIENT
    if not CLIENT is None:
        CLIENT.dest= SRV
    return SRV

def createClientEcho():
    global SRV
    global CLIENT
    CLIENT= Echo("CLI")
    print "create Client"
    CLIENT.dest=SRV
    if not SRV is None:
        SRV.dest= CLIENT
    return CLIENT

SRV = None
CLIENT = None 

def main():
    factory = protocol.ServerFactory()
    factory.protocol = createServerEcho
    reactor.listenTCP(8122,factory,interface="",)
    
    factory = protocol.ServerFactory()
    factory.protocol = createClientEcho
    reactor.listenTCP(8123,factory,interface="",)

    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()


