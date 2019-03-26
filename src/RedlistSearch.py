# coding: utf8
import osc, random
from threading import Thread
from requests import get

TOKEN = '9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee'        
        
if __name__ == '__main__':
    
    params = {'token' : TOKEN }
    page = ''
    region = ''
    category = ''
    iid = ''
    
    #COUNTRY
    #url = 'http://apiv3.iucnredlist.org/api/v3/country/list'
    
    #REGION
    #url = 'http://apiv3.iucnredlist.org/api/v3/region/list'
    
    #SPECIES COUNT
    #url = 'http://apiv3.iucnredlist.org/api/v3/speciescount'
    
    #SPECIES / PAGE
    #url = 'http://apiv3.iucnredlist.org/api/v3/species/page/'
    #page = '2'
    
    #REGIONAL SPECIES
    #url = 'http://apiv3.iucnredlist.org/api/v3/species/region'
    #page = '/page/0'
    #region = '/europe'
    
    #SPECIES BY CATEGORY 
    # "DD", "LC", "NT", "VU", "EN", "CR", "EW", "EX", "LRlc", "LRnt", "LRcd".
    url = 'http://apiv3.iucnredlist.org/api/v3/species/category/'
    region = ''
    page = ''
    category = 'VU'
    
    #COUNTRY OCCURENCE
    #url = 'http://apiv3.iucnredlist.org/api/v3/species/countries/id/'
    #iid = '12392'
    
    #COMMON_NAMES
    #/api/v3/species/common_names/:name?token='YOUR TOKEN'
    
    #THREATS
    #https://apiv3.iucnredlist.org/api/v3/threats/species/name/Loxodonta%20africana?token=
    #https://apiv3.iucnredlist.org/api/v3/threats/species/id/12392?token=
    
    #WEBLINK
    #https://apiv3.iucnredlist.org/api/v3/weblink/loxodonta%20africana
    #/api/v3/taxonredirect/:taxonID
    
    print url + region + page + category + iid + "?token=" + TOKEN
    resp = get(url + region + page + category + iid, params)

    if resp.status_code == 200:
        
        '''
        #COUNTRY OCCURENCE
        result = resp.json()
        count = result['count']
        for k in range(0, count):
            print result['result'][k]['country']
        '''
    
        
        #SPECIES BY CATEGORY (1 random specy)
        result = resp.json()
        count = result['count']
        print "results " + str(count)
        cat = result['category']
        r = random.randint(0, count)
        res = result['result'][r]
        #print str(res['taxonid']) + " \'" + res['scientific_name'] + "\'"
        
        #get info via taxonid
        url2 = 'http://apiv3.iucnredlist.org/api/v3/species/id/'
        resp2 = get(url2 + str(res['taxonid']), params)
        if resp2.status_code == 200:
            result2 = resp2.json()
            res2= result2['result'][0]
            print "- id "+str(res2['taxonid'])
            print "  common_name: \'" + str(res2['main_common_name']) + "\'"
            print "  scientific_name: \'" + res2['scientific_name'] + "\'"
            print "  kingdom: " +res2['kingdom']
            print "  phylum: " + res2['phylum']
            print "  class: " + res2['class']
            print "  order: " + res2['order']
            print "  family: " + res2['family']
            print "  genus: " + res2['genus']
            print "  category: " + str(res2['category'])
            print "  population_trend: " + str(res2['population_trend'])
            print "  marine: " + str(res2['marine_system'])
            print "  freshwater: " + str(res2['freshwater_system'])
            print "  terrestrial: " + str(res2['terrestrial_system'])
            
            '''
            #SYNONYM
            url3 = 'http://apiv3.iucnredlist.org/api/v3/species/synonym/'
            resp3 = get(url3 + res2['scientific_name'], params)
            if resp3.status_code == 200:
                result3 = resp3.json()
                count = result3['count']
                for j in range(0, count):
                    print "    synonym: " + str(result3['result'][j]['synonym'])
            #else:
            #    raise ValueError(resp3.text)
            #'''
            
            #COUNTRY OCCURENCE
            #TODO à tester
            url4 = 'http://apiv3.iucnredlist.org/api/v3/species/countries/id/'
            resp4 = get(url4 + str(res2['taxonid']), params)
            if resp4.status_code == 200:
                result4 = resp4.json()
                count = result4['count']
                for k in range(0, count):
                    print "    country " + str(result4['result'][k]['country'])

        else:
            raise ValueError(resp2.text)
        
    
    
        '''
        #REGIONAL SPECIES (10 random species)
        result = resp.json()
        count = result['count']
        print "results " + str(count)
        for i in range(0,10):
            r = random.randint(0,count)
            res = result['result'][r]
            print str(res['taxonid']) + " " + res['kingdom_name'] + " " + res['phylum_name'] + " " + res['class_name'] + " " + res['order_name'] + " " + res['family_name'] + " " + res['genus_name'] + " \'" + res['scientific_name'] + "\'"
        #'''
        
        '''
        #SPECIES / PAGE (10 random species)
        result = resp.json()
        count = result['count']
        #print "results " + str(count) + " page " + str(result['page'])
        for i in range(0,10):
            r = random.randint(0,count)
            res = result['result'][r]
            print str(res['taxonid']) + " " + res['kingdom_name'] + " " + res['phylum_name'] + " " + res['class_name'] + " " + res['order_name'] + " " + res['family_name'] + " " + res['genus_name'] + " \'" + res['scientific_name'] + "\'"
        #'''
        
        '''
        #SPECIES COUNT
        result = resp.json()
        print "SPECIES COUNT " + str(result['count'])  
        #'''
            
        '''
        #COUNTRY
        result = resp.json()
        for x in range(0, count):
            #if result['results'][x]['isocode'] == 'FR':
            #    print result['results'][x]['country']
            print result['results'][x]['country'] + " = " + result['results'][x]['isocode']
        #'''
         
        '''
        #REGION
        result = resp.json()
        for x in range(0, count):
            print result['results'][x]['name'] + " = " + result['results'][x]['identifier']
        #'''
        
    else:
        raise ValueError(resp.text)
    '''if len(sys.argv) == 1:
        PixabaSearch();
    elif len(sys.argv) == 4:
        PixabaSearch(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        print('usage: %s <osc-server-port> <osc-client-host> <osc-client-port>')'''
