from __future__ import print_function, division
import sys, osc, os


class BotResponse(object):
    
    def __init__(self, osc_server_port=5005, osc_client_host='127.0.0.1', osc_client_port=5009):
        self.osc_server_port = osc_server_port
        self.osc_client_host = osc_client_host
        self.osc_client_port = osc_client_port
        self.osc_client = osc.Client(osc_client_host, osc_client_port)
        self.osc_server = osc.Server(host='0.0.0.0', port=osc_server_port, callback=self.osc_server_message)
        self.osc_server.run(non_blocking=True)
        
        self.osc_client.send("/botresponse/ready")
        
        #self.model = torch.load(model_filename, map_location=lambda storage, loc: storage, encoding='utf8')
        #if default_allowed_filename is None:
            #self.allowed = set(self.model.dictionary.idx2word)
        #else:
            #self.allowed = set(open(default_allowed_filename).read().split('\n'))
            #self.allowed.update('.,!:;')
            
        print("Ready For Getting Bot Response")


    def osc_server_message(self, message):
        print("message entrant {}".format(message))
        if message == '/result/botresponse':
            print('get: {}'.format(message))
            #result = self.generate(200, prime='<eos>', temperature=0.9)
            #thetext = ' '.join([x for x in result if x != '<eos>'])
            #thetext = ("   " + thetext + "   ").strip('<eos>')
            #thetext = thetext.replace("(", " ")
            #thetext = thetext.replace(")", " ")
            #thetext = thetext.strip(';')
            #print(thetext)
            #self.osc_client.send("/generator/result "+thetext);
        elif message == '/exit':
            self.osc_server.shutdown()
            sys.exit(0)


if __name__ == '__main__':
    BotResponse()
