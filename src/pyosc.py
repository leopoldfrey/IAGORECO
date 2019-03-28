#from __future__ import print_function
import sys
from threading import Thread
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher

class Client:

    def __init__(self, host='127.0.0.1', port=1234):
        try:
            print('OSC: Connecting to client %s:%d' % (host, port))
            self.target = udp_client.SimpleUDPClient(host, port)
        except Exception as e:
            print(e)
            print('OSC: Could not connect to server %s:%d' % (host, port))

    def send(self, address, message):
        try:
            #print('OSC: sending ' + str(address) + ' _ ' + str(message))
            self.target.send_message(address, message)
        except Exception as e:
            print(e)
            print('OSC: failed to send message [%s] [%s]' % str(address), str(message))

class Server:

    def __init__(self, host='127.0.0.1', port=1234, callback=None):
        #, callback=self._callback):
        print('OSC: Creating server at %s:%d' % (host, port))
        dispat = dispatcher.Dispatcher()
        dispat.set_default_handler(callback)
        self.server = osc_server.ThreadingOSCUDPServer((host, port), dispat)
        self.server.block_on_close = False
        server_thread = Thread(target=self.server.serve_forever)
        server_thread.start()
        
    def stop(self):
        self.server.server_close()
        
'''
client = None

def setup(host, port):
    global client
    client = Client(host, port)
'''

if __name__ == '__main__':
    if len(sys.argv) > 3:
        client = Client(host=sys.argv[1], port=int(sys.argv[2]))
        client.send(' '.join(sys.argv[3:]))
    elif len(sys.argv) == 2:
        server = Server(port=int(sys.argv[1]))
        server.run()
    else:
        print('usage: client: %s <host> <port> <message> | server: %s <port>' % (sys.argv[0], sys.argv[0]))
