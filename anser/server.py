import socket


class Anser(object):
    """
    A class that models an Anser app. A configurable UDP server with
    BSON messaging.

    While an Anser object is running on a specific port, each incoming
    UDP message may trigger one or more actions, according to specified
    criteria.

    """ 
    def __init__(self, name, debug=False):
        """
        Initializes just the basic stuff. Main data structures are
        initiliazed inside ``run`` method

        """
        self.name = name
        self.actions = []
        self.debug = debug

    def run(self, ip='127.0.0.1', port=8080,
            buffer_size=1024):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.socket = Anser._get_udp_socket()
        self.socket.bind((self.ip, self.port))
        self._listen()


    def _process(self, data, address):
        for action in self.actions:
            action(data, address)


    def _listen(self):
        if self.debug:
            print "Server listening at {0}.{1}".format(
                        self.ip,
                        self.port
                    )
        while True:
            data, address = self.socket.recvfrom(self.buffer_size)
            if self.debug:
                print "Message received:"
                print "Address: {0}".format(address)
                print "Data: " + data
            self._process(data, address)


    def add_action(self, action, category):
        self.actions.append(action)
        if self.debug:
            print "{0} action added".format(action.__name__)


    def action(self, category):
        def decorator(f):
            self.add_action(f, category)
            return f
        return decorator


    @staticmethod
    def _get_udp_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
