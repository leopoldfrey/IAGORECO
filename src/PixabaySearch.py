# coding: utf8
import sys, osc
from threading import Thread
import random
from requests import get

API_KEY = '11796917-495df626c35f7f8d0c3831455'

class Image():
    def __init__(self, api_key):
        self.api_key = api_key
        self.root_url = "https://pixabay.com/api/"

    def search(self,
               q='yellow flower',
               lang='en',
               id='',
               response_group='image_details',
               image_type='all',
               orientation='all',
               category='',
               min_width=0,
               min_height=0,
               editors_choice='false',
               safesearch='false',
               order='popular',
               page=1,
               per_page=20,
               callback='',
               pretty='false'):
        payload = {
            'key': self.api_key,
            'q': q,
            'lang': lang,
            'id': id,
            'response_group': response_group,
            'image_type': image_type,
            'orientation': orientation,
            'category': category,
            'min_width': min_width,
            'min_height': min_height,
            'editors_choice': editors_choice,
            'safesearch': safesearch,
            'order': order,
            'page': page,
            'per_page': per_page,
            'callback': callback,
            'pretty': pretty
        }

        resp = get(self.root_url, params=payload)

        if resp.status_code == 200:
            return resp.json()
        else:
            raise ValueError(resp.text)

class DownThread(Thread):
    def __init__(self, keyword, osc_client, mode='random'):
        Thread.__init__(self)
        self.keyword = keyword
        self.osc_client = osc_client
        self.mode=mode
        
    def run(self):
        image = Image(API_KEY)
        ims = image.search(q=self.keyword,
                           lang='fr',
                           response_group='high_resolution',
                           image_type='photo',
                           orientation='horizontal',
                           category='animals nature',
                           safesearch='true',
                           order='latest',
                           page=1,
                           per_page=100)

        n = ims["totalHits"]
        #print(n)
        if(n == 0):
            print("Searching for "+self.keyword + " - not found")
        else:
            mi = min(n, 100)
                
            #RANDOM IMAGES
            if(self.mode == 'random'):
                r = random.randint(0,mi)
                print("Searching for "+self.keyword + " + found : " + str(r) + " / " + str(mi))
                url = ims["hits"][r]['largeImageURL']
                self.osc_client.send('/keyword '+unicode(self.keyword).encode('utf-8'))
                self.osc_client.send('/result '+ str(r+1) + ' ' + str(mi))
                self.osc_client.send('/path '+unicode(url).encode('utf-8'))#image[0]).encode('utf-8'))
                
            #ALL IMAGES
            elif(self.mode == 'all'):
                print("Searching for "+self.keyword + " + found : " + str(mi))
                self.osc_client.send('/keyword '+unicode(self.keyword).encode('utf-8'))
                for x in range(0,mi):
                    url = ims["hits"][x]['largeImageURL']
                    self.osc_client.send('/result '+ str(x+1) + ' ' + str(mi))
                    self.osc_client.send('/path '+unicode(url).encode('utf-8'))
        
class PixabaSearch:
    
    def __init__(self, osc_server_port=9860, osc_client_host='127.0.0.1', osc_client_port=9861):
        self.osc_server_port = osc_server_port
        self.osc_client_host = osc_client_host
        self.osc_client_port = osc_client_port
        self.osc_client = osc.Client(osc_client_host, osc_client_port)
        self.osc_server = osc.Server(host='0.0.0.0', port=osc_server_port, callback=self.osc_server_message)
        self.osc_server.run(non_blocking=True)
        self.mode = 'random'
    
        print("PixabaySearch Ready")
            
    def osc_server_message(self, message):
        #print(message)
        
        osc = message.split(" ", 1);
        key = message.split(" ", 1)[0]
        if(len(osc) > 1):
            rest = message.split(" ", 1)[1]
        else:
            rest =''
        
        if key == '/exit':
            self.osc_server.shutdown()
            sys.exit(0)
        elif key == '/reset':
            self.osc_client.send("/pixabaysearch/reset")
        elif key == '/mode':
            self.mode = rest
            print "-mode " + self.mode
        elif key == '/search':
            self.search(rest)
        else:
            self.search(message)
    
    def search(self, message):
        message = message.strip('\'')
        message = message.replace(",", " ")
        message = message.replace('à', "a")
        message = message.replace("â", "a")
        message = message.replace("é", "e")
        message = message.replace("è", "e")
        message = message.replace("ê", "e")
        message = message.replace("ë", "e")
        message = message.replace("î", "i")
        message = message.replace("ï", "i")
        message = message.replace("ô", "o")
        message = message.replace("ö", "o")
        message = message.replace("ù", "u")
        message = message.replace("ü", "u")
        message = message.replace("ç", "c")
        message = message.replace(")", " ")
        message = message.replace(", ", " ")
        message = message.replace("… ", " ")
        message = message.replace('\xe2\x80\x99', "'")
        
        thd = DownThread(message, self.osc_client, self.mode);
        thd.start();
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        PixabaSearch();
    elif len(sys.argv) == 4:
        PixabaSearch(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port>')
