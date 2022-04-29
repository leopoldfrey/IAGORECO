# coding: utf8
import sys, osc, random
from requests import get
from threading import Thread

class InatImage():
    def __init__(self):
        self.root_url = "https://api.inaturalist.org/v1/search"

    def search(self,
               q='chat',
               sources='taxa',
               per_page='20',
               locale='fr'):
        
        payload = {
            'q': q,
            'sources': sources,
            'per_page': per_page,
            'locale': locale
        }

        #print self.root_url
        #print payload
        resp = get(self.root_url, params=payload)

        if resp.status_code == 200:
            return resp.json()
        else:
            raise ValueError(resp.text)
        
class InatThread(Thread):
    def __init__(self, keyword, osc_client, mode='random', size='medium_url'):
        Thread.__init__(self)
        self.keyword = keyword
        self.osc_client = osc_client
        self.mode=mode
        self.size=size
        
    def run(self):
        image = InatImage()
        ims = image.search(q=self.keyword,
                           locale='fr',
                           sources='taxa',
                           per_page=100)

        #print ims
        n = ims["total_results"]
        #print(n)
        if(n == 0):
            print("Searching for "+ self.keyword + " - not found")
        else:
            #RANDOM IMAGES
            if(self.mode == 'random'):
                i = len(ims['results'][0]["record"]["taxon_photos"])
                r = random.randint(0,i-1)
                print("Searching for "+ self.keyword + " + found : " + str(r) + " / " + str(i))
                url = ims["results"][0]["record"]["taxon_photos"][r]["photo"][self.size] # "square_url" "small_url" "medium_url" "large_url" "original_url"
                name = ims["results"][0]["record"]["name"]
                self.osc_client.send('/keyword '+unicode(self.keyword).encode('utf-8'))
                self.osc_client.send('/name '+ unicode(name).encode('utf-8'))
                self.osc_client.send('/result '+ str(r+1) + ' ' + str(i))
                self.osc_client.send('/path '+unicode(url).encode('utf-8'))
                
            #ALL IMAGES
            elif(self.mode == 'all'):
                i = len(ims['results'][0]["record"]["taxon_photos"])
                print("Searching for "+ self.keyword + " + found : " + str(i))
                name = ims["results"][0]["record"]["name"]
                self.osc_client.send('/keyword '+unicode(self.keyword).encode('utf-8'))
                self.osc_client.send('/name '+ unicode(name).encode('utf-8'))
                for x in range(0, i):
                    #print "search " +str(x) + " " + str(len(ims["results"][0]["record"]["taxon_photos"]))
                    url = ims["results"][0]["record"]["taxon_photos"][x]["photo"][self.size]
                    self.osc_client.send('/result '+ str(x+1) + ' ' + str(i))
                    self.osc_client.send('/path '+unicode(url).encode('utf-8'))
        
class InaturalistSearch:
    
    def __init__(self, osc_server_port=9880, osc_client_host='127.0.0.1', osc_client_port=9881):
        self.osc_server_port = osc_server_port
        self.osc_client_host = osc_client_host
        self.osc_client_port = osc_client_port
        self.osc_client = osc.Client(osc_client_host, osc_client_port)
        self.osc_server = osc.Server(host='0.0.0.0', port=osc_server_port, callback=self.osc_server_message)
        self.osc_server.run(non_blocking=True)
        self.mode = 'random'
        self.size = 'medium_url' # "square_url" "small_url" "medium_url" "large_url" "original_url"
    
        print("Inaturalist Search Ready")
            
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
            self.osc_client.send("/inaturalistsearch/reset")
        elif key == '/mode':
            self.mode = rest
            print "-mode "+self.mode
        elif key == '/size':
            self.size = rest
            print "-size "+self.size
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
        
        InatThread(message, self.osc_client, self.mode, self.size).start();
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        InaturalistSearch();
    elif len(sys.argv) == 4:
        InaturalistSearch(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port>')
