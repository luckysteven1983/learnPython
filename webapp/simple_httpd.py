
'''
from http.server import HTTPServer, CGIHTTPRequestHandler
##Above is for python3.x
'''
from CGIHTTPServer import CGIHTTPRequestHandler
from BaseHTTPServer import HTTPServer

port = 8080

httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()

