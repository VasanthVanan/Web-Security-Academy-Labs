from urllib.parse import urlparse
from tabulate import tabulate
import requests
import sys

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

def validate_url(url):
    # This function validates the URL entered by the user
    parsed_url = urlparse(url)
    
    if parsed_url.scheme and parsed_url.netloc:
        return True
    return False

def append_colors(text, color):
    # This function appends color to the text entered by the user
    return "{}{}{}".format(color,text,textcolor.ENDC)

def get_input(data):
    # This function generates the table and gets the user input
    headers = [append_colors("Labs",textcolor.OKGREEN),append_colors("Title", textcolor.OKGREEN)]

    data = [
        [append_colors(item, textcolor.OKBLUE) for item in sublist]
        for sublist in data
    ]

    try:
        # get URL to test
        url = input(append_colors("\nEnter the URL to test: ",textcolor.WARNING))
  
    except (KeyboardInterrupt, Exception):
        sys.exit(append_colors("\nUnexpected error occurred\n",textcolor.DANGER))
        

    # validate URL
    if not validate_url(url):
        sys.exit(append_colors("Invalid URL: Check Properly\n", textcolor.DANGER))
        
    
    # Generate the table
    table = tabulate(data, headers, tablefmt="pretty")
    print("\n"+table)

    try:
        choice = input(append_colors("\nEnter your Lab (1-{}): ", textcolor.WARNING).format(len(data)))
        return [int(choice), url.rstrip('/')]
    except:
        sys.exit(append_colors("\nInvalid Input\n",textcolor.DANGER))

def http_request(base_url, path, data):
    # This is a common function used to send HTTP requests with customized payloads
    payload_data = data[0]
    headers_data = data[1] 
    try:
        response = requests.post(base_url + path, data=payload_data, headers=headers_data, timeout=3)
        return response

    except requests.exceptions.ConnectTimeout as e:
        return 1
    except requests.exceptions.RequestException as e:
        print(append_colors("\nError occurred: ",textcolor.DANGER))
        print(f"{str(e)}\n")
    except Exception as e:
        print(append_colors("\nUnexpected error occurred:",textcolor.DANGER))
        print(f"{str(e)}\n")

    return 0

def highlight_text(text, compare_list):
    # This function highlights the text entered by the user
    text_lines = text.split('\n')
    for i in text_lines:
        if any(x in i for x in compare_list):
            print(append_colors(i, textcolor.DANGER))
        else:
            print(i)