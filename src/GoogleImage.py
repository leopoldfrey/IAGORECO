# coding: utf8
import google_images_download   #importing the library
import sys, osc, random
from threading import Thread

#TODO DO NOT DOWNLOAD

class DownThread(Thread):
    def __init__(self, keyword, osc_client, mode='random', size='medium', color='none'):
        Thread.__init__(self)
        self.keyword = keyword
        self.osc_client = osc_client
        self.mode = mode
        self.size = size
        self.color = color
        
    def run(self):
        print("Searching for "+self.keyword)
        response = google_images_download.googleimagesdownload()   #class instantiation
        arguments = {"keywords":self.keyword,"limit":100,"print_urls":False,"print_paths":True, "no_directory":True, "no_download":True, "type":"photo", "format":"jpg"}
        arguments['size'] = self.size
        if(self.color != 'none'):
            arguments['color'] = self.color
        #"color_type":"black-and-white"} "usage_rights":"labeled-for-noncommercial-reuse-with-modification", "size": ">1024*768", "language":"French"   #creating list of arguments
        paths = response.download(arguments)   #passing the arguments to the function
        n = len(paths[self.keyword])
        if(n == 0):
            print("Searching for "+ self.keyword + " - not found")
        else:
            #RANDOM IMAGES
            if(self.mode == 'random'):
                r = random.randint(0,n-1)
                print("Searching for "+ self.keyword + " + found : " + str(r) + " / " + str(n))
                url = paths[self.keyword][r]
                self.osc_client.send('/keyword '+unicode(self.keyword).encode('utf-8'))
                self.osc_client.send('/result '+ str(r+1) + ' ' + str(n))
                self.osc_client.send('/path '+unicode(url).encode('utf-8'))
            
            #ALL IMAGES
            elif(self.mode == 'all'):
                print("Searching for "+self.keyword + " + found : " + str(n))
                self.osc_client.send('/keyword '+unicode(self.keyword).encode('utf-8'))
                for x in range(0,n):
                    url = paths[self.keyword][x]
                    self.osc_client.send('/result '+ str(x+1) + ' ' + str(n))
                    self.osc_client.send('/path '+unicode(url).encode('utf-8'))
        
class GoogleImage:
    
    def __init__(self, osc_server_port=8260, osc_client_host='127.0.0.1', osc_client_port=8261):
        self.osc_server_port = osc_server_port
        self.osc_client_host = osc_client_host
        self.osc_client_port = osc_client_port
        self.osc_client = osc.Client(osc_client_host, osc_client_port)
        self.osc_server = osc.Server(host='0.0.0.0', port=osc_server_port, callback=self.osc_server_message)
        self.osc_server.run(non_blocking=True)
        self.mode = 'random'
        self.size = 'large'
        self.color = 'none'
        
        print("GoogleImage Ready")
        
    def osc_server_message(self, message):
        #print(message)
        osc = message.split(" ", 1);
        key = message.split(" ", 1)[0]
        if(len(osc) > 1):
            rest = message.split(" ", 1)[1]
        else:
            rest =''
        
        #print key + " / " + rest   
        
        if key == '/exit':
            self.osc_server.shutdown()
            sys.exit(0)
        elif key == '/reset':
            self.osc_client.send("/googleimage/reset")
        elif key == '/mode':
            self.mode = rest
            print '-mode ' + self.mode
        elif key == '/size': #'large','medium','icon','>400*300','>640*480','>800*600','>1024*768','>2MP','>4MP','>6MP','>8MP','>10MP','>12MP','>15MP','>20MP','>40MP','>70MP'
            self.size = rest
            print '-size ' + self.size
        elif key == '/color':
            self.color = rest
            print '-color ' + self.color
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
        
        thd = DownThread(message, self.osc_client, self.mode, self.size, self.color);
        thd.start();
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        GoogleImage();
    elif len(sys.argv) == 4:
        GoogleImage(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port>')