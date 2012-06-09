import random
def get_stats():
    return {'accesses': random.randint(100,200),
            'downloads': random.randint(20,200)}

class Config(dict):
    node_info = {
          'name': "blue meth fighting in alberoque",
          'statistics': get_stats(), # XXX make this become a lazy property
                                     # something like this:
                                     # http://blog.pythonisito.com/2008/08/lazy-descriptors.html
          'node-properties': {'end2end_encryption': True,
                              'anonymous_receiver': True},
          'contexts': [
                        { 'name' : 'Heisenberg sightings',
                          'groups' : [
                                { 'id': 0, 'name': 'police', 'description': 'Our national strength',
                                  'lang': ['EN', 'ES'] },
                                { 'id': 1, 'name': 'vigilantes', 'description': 'Batman progeny',
                                  'lang': ['IT', 'PT', 'LT', 'EN', 'ES']
                                } ],
                          'fields': [ { 'name': 'headline', 'type':'text', 'Required': True },
                                      { 'name': 'photo', 'type':'img', 'Required':False },
                                      { 'name': 'description', 'type': 'txt', 'Required':True }, ]
                        },
                        {'name': 'Crystal Meth report',
                          'groups': [ { 0 : 'police' , 1 : 'journalists', 2 : 'Municipality'} ],
                          'fields': [ { 'name': 'headline', 'type':'text', 'Required': True },
                                      { 'name': 'proof', 'type':'file', 'Required':True },
                                      { 'name': 'description', 'type': 'txt', 'Required':True }, ]
                        }
                      ],
           'description': 'This node aggregate expert of the civil society in fighting the crystal meth, producted by the infamous Heisenberg',
           'public_site': 'http://fightmeth.net',
           'hidden_service': 'vbg7fb8yuvewb9vuww.onion',
          }

config = Config()
