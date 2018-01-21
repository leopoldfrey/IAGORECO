from __future__ import print_function
import liblo, sys


class Client:

    def __init__(self, host='127.0.0.1', port=1234):
        try:
            print('OSC: connecting to client %s:%d' % (host, port))
            self.target = liblo.Address(host, port)
        except Exception as e:
            print(e)
            print('OSC: Could not connect to server %s:%d' % (host, port))

    def send(self, message):
        try:
            # print('OSC: sending message "%s"' % str(message))
            liblo.send(self.target, str(message))
        except Exception as e:
            print(e)
            print('OSC: failed to send message [%s]' % str(message))

    def send_action(self, action):
        # self.send('/action/%s' % (action.text))
        self.send('ACTION: %s' % (action.name))

    def send_words(self, start, words):
        # self.send('/words/%d/%s' % (start, words))
        self.send('/words %s' % words)

    def send_sentence(self, start, words):
        # self.send('/words/%d/%s' % (start, words))
        self.send('/sentence %s' % words)


class Server:

    def __init__(self, host='127.0.0.1', port=1234, callback=None):
        print('OSC: Creating server at %s:%d' % (host, port))
        self.server = liblo.Server(port)
        self.server.add_method(None, None, self.callback)
        self._callback = callback
        self.thread = None
        self.finished = False

    def callback(self, message):
        #print('OSC: Received [%s]' % message)
        if self._callback != None:
                self._callback(message)

    def run(self, non_blocking=False):
        if non_blocking:
            import threading
            print('OSC: starting thread')
            self.thread = threading.Thread(target=self._server_loop, args=())
            self.thread.start()
        else:
            self._server_loop()

    def _server_loop(self):
        print('OSC: Waiting for messages')
        while not self.finished:
            self.server.recv(100)
        self.server.free()

    def shutdown(self):
        self.finished = True
        # self.thread.join()


client = None


def setup(host, port):
    global client
    client = Client(host, port)


if __name__ == '__main__':
    if len(sys.argv) > 3:
        client = Client(host=sys.argv[1], port=int(sys.argv[2]))
        client.send(' '.join(sys.argv[3:]))
    elif len(sys.argv) == 2:
        server = Server(port=int(sys.argv[1]))
        server.run()
    else:
        print('usage: client: %s <host> <port> <message> | server: %s <port>' % (sys.argv[0], sys.argv[0]))
