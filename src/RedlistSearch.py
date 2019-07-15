#import sys, webbrowser, 
import sys, random
from threading import Thread
from requests import get
from pyosc import Server
from pyosc import Client

TOKEN = '9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee'        
        
def bool2int(b):
    if(b == True):
        return 1
    else:
        return 0       

class ApiThread(Thread):
    def __init__(self, osc_client, mode='SPECIES_CATEGORY', page=0, region='', iid='', category='', sname='', nresult=10, country=''):
        Thread.__init__(self)
        self.osc_client = osc_client
        self.mode = mode
        self.page = page
        self.region = region
        self.country = country
        self.iid = iid
        self.category = category
        self.sname = sname
        self.nresult = nresult
        self.params = {'token' : TOKEN }
        
    def run(self):
        if(self.mode == 'country'):
            #COUNTRY
            url = 'http://apiv3.iucnredlist.org/api/v3/country/list'
            print('COUNTRY URL '+ url + "?token=" + TOKEN)
            resp = get(url, self.params)
            if resp.status_code == 200:
                result = resp.json()
                count = result['count']
                self.osc_client.send('/country', 'clear')
                for x in range(0, count):
                    self.osc_client.send('/country', 'append '+result['results'][x]['isocode']+' ('+result['results'][x]['country'] + ')')
            else:
                raise ValueError(resp.text)
        
        elif(self.mode == 'region'):
            #REGION
            url = 'http://apiv3.iucnredlist.org/api/v3/region/list'
            print('REGION URL '+ url + "?token=" + TOKEN)
            resp = get(url, self.params)
            if resp.status_code == 200:
                result = resp.json()
                count = result['count']
                self.osc_client.send('/region', 'clear')
                for x in range(0, count):
                    self.osc_client.send('/region', 'append '+result['results'][x]['identifier']+' ('+result['results'][x]['name'] + ")")
            else:
                raise ValueError(resp.text)

        elif(self.mode == 'species_count'):
            #SPECIES COUNT
            url = 'http://apiv3.iucnredlist.org/api/v3/speciescount'
            print('SPECIES_COUNT URL '+ url+"?token=" + TOKEN)
            resp = get(url, self.params)
            if resp.status_code == 200:
                result = resp.json()
                self.osc_client.send('/speciescount', result['count'])
            else:
                raise ValueError(resp.text)
        
        #TODO OSC OUT    
        elif(self.mode == 'species_page'):
            #SPECIES / PAGE
            url = 'http://apiv3.iucnredlist.org/api/v3/species/page/'
            page = str(self.page)
            print('SPECIES_PAGE URL '+ url + page + "?token=" + TOKEN)
            resp = get(url + page, self.params)
            if resp.status_code == 200:
                result = resp.json()
                count = result['count']
                print("results " + str(count))
                #(10 random species)
                for x in range(0,min(count,self.nresult)):
                    r = random.randint(0,count)
                    res = result['result'][r]
                    self.osc_client.send('/species_page', str(res['taxonid']) + " \'" + res['scientific_name'] + "\'")
            else:
                raise ValueError(resp.text)
            
        elif(self.mode == 'species_region'):
            #REGIONAL SPECIES
            url = 'http://apiv3.iucnredlist.org/api/v3/species/region'
            page = '/page/'+str(self.page)
            region = '/'+self.region
            print('SPECIES_REGION URL '+ url + region + page + "?token=" + TOKEN)
            resp = get(url + region + page, self.params)
            if resp.status_code == 200:
                result = resp.json()
                count = result['count']
                print("results " + str(count))
                #(10 random species)
                for x in range(0,min(count,self.nresult)):
                    r = random.randint(0,count)
                    res = result['result'][r]
                    self.osc_client.send('/species_region', str(res['taxonid']) + " \'" + res['scientific_name'] + "\'")
            else:
                raise ValueError(resp.text)
        
        elif(self.mode == 'species_country'):
            #SPECIES_BY_COUNTRY
            url = 'http://apiv3.iucnredlist.org/api/v3/country/getspecies/'
            country = self.country
            print('SPECIES_COUNTRY URL '+ url + country + "?token=" + TOKEN)
            resp = get(url + country, self.params)
            if resp.status_code == 200:
                result = resp.json()
                count = result['count']
                print("results " + str(count))
                #(10 random species)
                for x in range(0,min(count,self.nresult)):
                    r = random.randint(0,count)
                    res = result['result'][r]
                    self.osc_client.send('/species_country', str(res['taxonid']) + " \'" + res['scientific_name'] + "\'")
            else:
                raise ValueError(resp.text)
        
            #:country?token='YOUR TOKEN'

        elif(self.mode == 'species_category'):
            #SPECIES BY CATEGORY "DD", "LC", "NT", "VU", "EN", "CR", "EW", "EX", "LRlc", "LRnt", "LRcd".
            url = 'http://apiv3.iucnredlist.org/api/v3/species/category/'
            category = 'CR'
            print('SPECIES_CATEGORY URL '+ url + category + "?token=" + TOKEN)
            resp = get(url + category, self.params)
            if resp.status_code == 200:
                result = resp.json()
                count = result['count']
                print("results " + str(count))
                #(10 random species)
                for x in range(0,min(count,self.nresult)):
                    r = random.randint(0,count)
                    res = result['result'][r]
                    self.osc_client.send('/species_category', str(res['taxonid']) + " \'" + res['scientific_name'] + "\'")
            else:
                raise ValueError(resp.text)
        
        elif(self.mode == 'species_name'):
            url = 'http://apiv3.iucnredlist.org/api/v3/species/'
            name = self.sname
            print('SPECIES_NAME URL '+ url + name + "?token=" + TOKEN)
            resp = get(url + name, self.params)
            if resp.status_code == 200:
                result = resp.json()
                if(len(result['result']) >= 1):
                    res = result['result'][0]
                    self.osc_client.send('/species/id', res['taxonid'])
                    self.osc_client.send('/species/scientific_name', str(res['scientific_name']))
                    self.osc_client.send('/species/common_name', str(res['main_common_name']))
                    self.osc_client.send('/species/taxonomy/kingdom', str(res['kingdom'].capitalize()))
                    self.osc_client.send('/species/taxonomy/phylum', str(res['phylum'].capitalize()))
                    self.osc_client.send('/species/taxonomy/class', str(res['class'].capitalize()))
                    self.osc_client.send('/species/taxonomy/order', str(res['order'].capitalize()))
                    self.osc_client.send('/species/taxonomy/family', str(res['family'].capitalize()))
                    self.osc_client.send('/species/taxonomy/genus', str(res['genus'].capitalize()))
                    self.osc_client.send('/species/category', str(res['category']))
                    self.osc_client.send('/species/population_trend', str(res['population_trend']))
                    self.osc_client.send('/species/marine', bool2int(res['marine_system']))
                    self.osc_client.send('/species/freshwater', bool2int(res['freshwater_system']))
                    self.osc_client.send('/species/terrestrial', bool2int(res['terrestrial_system']))
                    url2 = 'https://apiv3.iucnredlist.org/api/v3/weblink/'
                    #print(url2+res['scientific_name'] + "?token=" + TOKEN)
                    resp2 = get(url2 + res['scientific_name'], self.params)
                    if resp2.status_code == 200:
                        result2 = resp2.json()
                        self.osc_client.send('/species/link', str(result2['rlurl']))
                    else: 
                        raise ValueError(resp2.text)
                else:
                    print("no results")
    
            else:
                raise ValueError(resp.text)
          
        elif(self.mode == 'species_id'):
            url = 'http://apiv3.iucnredlist.org/api/v3/species/id/'
            iid = self.iid#'12392'
            print('SPECIES_ID URL '+ url + iid + "?token=" + TOKEN)
            resp = get(url + iid, self.params)
            if resp.status_code == 200:
                result = resp.json()
                if(len(result['result']) >= 1):
                    res= result['result'][0]
                    self.osc_client.send('/species/id', res['taxonid'])
                    self.osc_client.send('/species/scientific_name', str(res['scientific_name']))
                    self.osc_client.send('/species/common_name', str(res['main_common_name']))
                    self.osc_client.send('/species/taxonomy/kingdom', str(res['kingdom'].capitalize()))
                    self.osc_client.send('/species/taxonomy/phylum', str(res['phylum'].capitalize()))
                    self.osc_client.send('/species/taxonomy/class', str(res['class'].capitalize()))
                    self.osc_client.send('/species/taxonomy/order', str(res['order'].capitalize()))
                    self.osc_client.send('/species/taxonomy/family', str(res['family'].capitalize()))
                    self.osc_client.send('/species/taxonomy/genus', str(res['genus'].capitalize()))
                    self.osc_client.send('/species/category', str(res['category']))
                    self.osc_client.send('/species/population_trend', str(res['population_trend']))
                    self.osc_client.send('/species/marine', bool2int(res['marine_system']))
                    self.osc_client.send('/species/freshwater', bool2int(res['freshwater_system']))
                    self.osc_client.send('/species/terrestrial', bool2int(res['terrestrial_system']))
                    url2 = 'https://apiv3.iucnredlist.org/api/v3/weblink/'
                    #print(url2+res['scientific_name'] + "?token=" + TOKEN)
                    resp2 = get(url2 + res['scientific_name'], self.params)
                    if resp2.status_code == 200:
                        result2 = resp2.json()
                        self.osc_client.send('/species/link', str(result2['rlurl']))
                    else: 
                        raise ValueError(resp2.text)
                else:
                    print("no results")
    
            else:
                raise ValueError(resp.text)
            
        elif(self.mode == 'country_occurence'):
            #COUNTRY OCCURENCE
            '''url = 'http://apiv3.iucnredlist.org/api/v3/species/countries/id/'
            iid = str(self.iid)
            print('COUNTRY_OCCURENCE URL '+ url + iid + "?token=" + TOKEN)
            resp = get(url + iid, self.params)
            if resp.status_code == 200:
                result = resp.json()
                count = result['count']
                for k in range(0, count):
                    self.osc_client.send('/country_occurence', str(result['result'][k]['country']))
            else:
                raise ValueError(resp.text)
            #'''  
                      
        #COMMON_NAMES
        #/api/v3/species/common_names/:name?token='YOUR TOKEN'
        
        #THREATS
        #https://apiv3.iucnredlist.org/api/v3/threats/species/name/Loxodonta%20africana?token=
        #https://apiv3.iucnredlist.org/api/v3/threats/species/id/12392?token=
        
        #WEBLINK
        #https://apiv3.iucnredlist.org/api/v3/weblink/loxodonta%20africana
        #/api/v3/taxonredirect/:taxonID
        
    
class RedlistSearch:
    
    def __init__(self, osc_server_port=5860, osc_client_host='127.0.0.1', osc_client_port=5861):
        self.osc_client = Client(osc_client_host, osc_client_port)
        self.osc_server = Server('0.0.0.0', osc_server_port, self.callback)
        self.region = ''
        self.iid = '12392'
        self.category = ''
        self.country = 'FR'
        self.page = 0
        self.nresult = 10
        self.sname = 'loxodonta africana'
        self.mode = 'species_id'
         
        print("RedlistSearch Ready")
            
    def callback(self, address, *args):
        if(address == '/exit'):
            print("--- EXIT ---")
            self.osc_server.stop()
            sys.exit()
        elif(address == '/mode'):
            self.mode = str(args[0])
            print("-mode", self.mode)
        elif(address == '/region'):
            self.region = str(args[0])
            print("-region", self.region)
        elif(address == '/country'):
            self.country = str(args[0])
            print("-country", self.country)
        elif(address == '/id'):
            self.iid = str(args[0])
            print("-id", self.iid)
        elif(address == '/page'):
            self.page = args[0]
            print("-page", self.page)
        elif(address == '/category'):
            self.category = str(args[0])
            print("-category", self.category)
        elif(address == '/nresult'):
            self.nresult = args[0]
            print("-nresult", self.nresult)
        elif(address == '/name'):
            s = ""
            l = len(args)
            for x in range(0,l):
                s += str(args[x])
                if(x < (l-1)):
                    s += " "
            self.sname = str(s)
            print("-name", self.sname)
        elif(address == '/search'):
            self.search()
        else:
            print("callback : "+str(address))
            for x in range(0,len(args)):
                print("     " + str(args[x]))
    
    def search(self):
        thd = ApiThread(self.osc_client, mode=self.mode, page=self.page, region=self.region, iid=self.iid, category=self.category, sname=self.sname, nresult=self.nresult, country=self.country);
        thd.start();
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        RedlistSearch();
    elif len(sys.argv) == 4:
        RedlistSearch(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port>')
