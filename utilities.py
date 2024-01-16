from urllib.parse import urlparse
from tabulate import tabulate
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
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return True
    return False

def append_colors(text, color):
    return "{}{}{}".format(color,text,textcolor.ENDC)

def get_input(data):

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
        return [int(choice), url]
    except:
        sys.exit(append_colors("\nInvalid Input\n",textcolor.DANGER))